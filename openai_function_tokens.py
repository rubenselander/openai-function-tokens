import tiktoken


# Function to format function definitions
def format_function_definitions(functions) -> str:
    lines = ["namespace functions {"]
    # lines = ["namespace functions {", ""]
    for f in functions:
        if f.get("description"):
            lines.append(f"// {f['description']}")
        if f["parameters"].get("properties"):
            temp_s = f"type {f['name']} = (_: " + "{{"
            lines.append(temp_s)
            lines.append(format_object_properties(f["parameters"], 0))
            lines.append("}) => any;")
        else:
            lines.append(f"type {f['name']} = () => any;")
        lines.append("")
    lines.append("} // namespace functions")
    return "\n".join(lines)


# Helper function to format object properties
def format_object_properties(parameters, indent: int) -> str:
    lines = []
    for name, param in parameters["properties"].items():
        if param.get("description") and indent < 2:
            lines.append(f"// {param['description']}")
        if parameters.get("required") and name in parameters["required"]:
            lines.append(f"{name}: {format_type(param, indent)},")
        else:
            lines.append(f"{name}?: {format_type(param, indent)},")

    return "\n".join([" " * indent + line for line in lines])


# Helper function to format a single property type
def format_type(param, indent: int) -> str:
    if param["type"] == "string":
        if param.get("enum"):
            return " | ".join([f'"{v}"' for v in param["enum"]])
        return "string"
    elif param["type"] == "number":
        if param.get("enum"):
            return " | ".join([str(v) for v in param["enum"]])
        return "number"
    elif param["type"] == "array":
        if param.get("items"):
            return f"{format_type(param['items'], indent)}[]"
        return "any[]"
    elif param["type"] == "boolean":
        return "boolean"
    elif param["type"] == "null":
        return "null"
    elif param["type"] == "object":
        return "{\n" + format_object_properties(param, indent + 2) + "\n}"


def functions_tokens_estimate(functions):
    promptDefinitions = format_function_definitions(functions)
    tokens = string_tokens(promptDefinitions)
    tokens += 9  # Add nine per completion
    return tokens


def message_tokens_estimate(message):
    """
    Estimate the number of tokens for a given message.

    Args:
    - message (dict): A dictionary representing a message with potential keys 'role', 'content', 'name', and 'function_call'.

    Returns:
    - int: An estimate of the number of tokens.
    """

    components = [
        message.get("role"),
        message.get("content"),
        message.get("name"),
        message.get("function_call", {}).get("name"),
        message.get("function_call", {}).get("arguments"),
    ]
    # Filter out None values
    components = [component for component in components if component]

    # Assuming string_tokens is a function that exists and computes tokens for a string
    tokens = sum([string_tokens(component) for component in components])

    tokens += 3  # Add three per message

    if message.get("name"):
        tokens += 1

    if message.get("role") == "function":
        tokens -= 2

    if message.get("function_call"):
        tokens += 3

    return tokens


def string_tokens(string, model="gpt-3.5-turbo-0613"):
    if model is None:
        encoding = tiktoken.get_encoding("cl100k_base")
    else:
        try:
            encoding = tiktoken.encoding_for_model(model)
        except KeyError:
            print("Warning: model not found. Using cl100k_base encoding.")
            encoding = tiktoken.get_encoding("cl100k_base")
    return len(encoding.encode(string))


def prompt_tokens_estimate(messages, functions=None, function_call=None):
    """
    Estimate the number of tokens for a given prompt with messages and functions.

    Args:
    - messages (list[dict]): A list of message dictionaries, where each message has 'role' and 'content' keys.
    - functions (list[dict], optional): A list of function dictionaries. Default is None.
    - function_call (str or dict, optional): A string ("none", "auto") or a dictionary with 'name' key. Default is None.

    Returns:
    - int: An estimate of the number of tokens.
    """

    # It appears that if functions are present, the first system message is padded with a trailing newline. This
    # was inferred by trying lots of combinations of messages and functions and seeing what the token counts were.
    padded_system = False
    tokens = 0
    for msg in messages:
        # If the message is from the system, functions are present, and system hasn't been padded yet
        if msg["role"] == "system" and functions and not padded_system:
            # Modify the content to add a newline
            modified_message = {"role": msg["role"], "content": msg["content"] + "\n"}
            tokens += message_tokens_estimate(modified_message)
            padded_system = True  # Update the padded system flag
        else:
            # If no modifications are required, just estimate the tokens for the original message
            tokens += message_tokens_estimate(msg)

    # Track if system was padded
    if functions and any(msg["role"] == "system" for msg in messages):
        padded_system = True

    # Each completion (vs message) seems to carry a 3-token overhead
    tokens += 3

    # If there are functions, add the function definitions as they count towards token usage
    if functions:
        tokens += functions_tokens_estimate(functions)

    # If there's a system message _and_ functions are present, subtract four tokens. I assume this is because
    # functions typically add a system message, but reuse the first one if it's already there. This offsets
    # the extra 9 tokens added by the function definitions.
    if functions and any(m["role"] == "system" for m in messages):
        tokens -= 4

    # If function_call is 'none', add one token.
    # If it's a FunctionCall object, add 4 + the number of tokens in the function name.
    # If it's undefined or 'auto', don't add anything.
    if function_call and function_call != "auto":
        tokens += (
            1 if function_call == "none" else string_tokens(function_call["name"]) + 4
        )

    return tokens

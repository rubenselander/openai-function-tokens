#Tiktoken needs to be installed before usage (pip install Tiktoken)
import tiktoken


def format_function_definitions(functions: list[dict]) -> str:
    """
    Generates TypeScript function type definitions.

    Args:
    - functions (list[dict]): List of dictionaries representing function definitions.

    Returns:
    - str: TypeScript function type definitions.
    """
    lines = ["namespace functions {"]

    for func in functions:
        if func.get("description"):
            lines.append(f"// {func['description']}")

        if func["parameters"].get("properties"):
            lines.append(f"type {func['name']} = (_: {{")
            lines.append(_format_object_properties(func["parameters"], 0))
            lines.append("}) => any;")
        else:
            lines.append(f"type {func['name']} = () => any;")

        lines.append("")

    lines.append("} // namespace functions")
    return "\n".join(lines)


def _format_object_properties(parameters: dict, indent: int) -> str:
    """
    Formats object properties for TypeScript type definitions.

    Args:
    - parameters (dict): Dictionary representing object parameters.
    - indent (int): Number of spaces for indentation.

    Returns:
    - str: Formatted object properties.
    """
    lines = []
    for name, param in parameters["properties"].items():
        if param.get("description") and indent < 2:
            lines.append(f"// {param['description']}")

        is_required = parameters.get("required") and name in parameters["required"]
        lines.append(
            f"{name}{'?:' if not is_required else ':'} {_format_type(param, indent)},"
        )

    return "\n".join([" " * indent + line for line in lines])


def _format_type(param: dict, indent: int) -> str:
    """
    Formats a single property type for TypeScript type definitions.

    Args:
    - param (dict): Dictionary representing a parameter.
    - indent (int): Number of spaces for indentation.

    Returns:
    - str: Formatted type for the given parameter.
    """
    type_ = param["type"]
    if type_ == "string":
        return (
            " | ".join([f'"{v}"' for v in param["enum"]])
            if param.get("enum")
            else "string"
        )
    elif type_ == "number":
        return (
            " | ".join([str(v) for v in param["enum"]])
            if param.get("enum")
            else "number"
        )
    elif type_ == "array":
        return (
            f"{_format_type(param['items'], indent)}[]"
            if param.get("items")
            else "any[]"
        )
    elif type_ == "boolean":
        return "boolean"
    elif type_ == "null":
        return "null"
    elif type_ == "object":
        return "{\n" + _format_object_properties(param, indent + 2) + "\n}"
    else:
        raise ValueError(f"Unsupported type: {type_}")


def _estimate_function_tokens(functions: list[dict]) -> int:
    """
    Estimates token count for a given list of functions.

    Args:
    - functions (list[dict]): List of dictionaries representing function definitions.

    Returns:
    - int: Estimated token count.
    """
    prompt_definitions = format_function_definitions(functions)
    tokens = _estimate_string_tokens(prompt_definitions)
    tokens += 9  # Add nine per completion
    return tokens


def _estimate_string_tokens(string: str, model: str = "gpt-3.5-turbo-0613") -> int:
    """
    Estimates token count for a given string based on a specified model.

    Args:
    - string (str): Input string.
    - model (str, optional): Model name. Default is "gpt-3.5-turbo-0613".

    Returns:
    - int: Estimated token count.
    """
    try:
        encoding = tiktoken.encoding_for_model(model)
    except KeyError:
        print("Warning: model not found. Using cl100k_base encoding.")
        encoding = tiktoken.get_encoding("cl100k_base")
    return len(encoding.encode(string))


def _estimate_message_tokens(message: dict) -> int:
    """
    Estimates token count for a given message.

    Args:
    - message (dict): Dictionary representing a message.

    Returns:
    - int: Estimated token count.
    """
    components = [
        message.get("role"),
        message.get("content"),
        message.get("name"),
        message.get("function_call", {}).get("name"),
        message.get("function_call", {}).get("arguments"),
    ]
    components = [
        component for component in components if component
    ]  # Filter out None values
    tokens = sum([_estimate_string_tokens(component) for component in components])

    tokens += 3  # Add three per message
    if message.get("name"):
        tokens += 1
    if message.get("role") == "function":
        tokens -= 2
    if message.get("function_call"):
        tokens += 3

    return tokens


def estimate_prompt_tokens(
    messages: list[dict], functions: list[dict] = None, function_call=None
) -> int:
    """
    Estimates token count for a given prompt with messages and functions.

    Args:
    - messages (list[dict]): List of dictionaries representing messages.
    - functions (list[dict], optional): List of dictionaries representing function definitions. Default is None.
    - function_call (str or dict, optional): Function call specification. Default is None.

    Returns:
    - int: Estimated token count.
    """
    padded_system = False
    tokens = 0

    for msg in messages:
        if msg["role"] == "system" and functions and not padded_system:
            modified_message = {"role": msg["role"], "content": msg["content"] + "\n"}
            tokens += _estimate_message_tokens(modified_message)
            padded_system = True  # Mark system as padded
        else:
            tokens += _estimate_message_tokens(msg)

    tokens += 3  # Each completion has a 3-token overhead
    if functions:
        tokens += _estimate_function_tokens(functions)

    if functions and any(m["role"] == "system" for m in messages):
        tokens -= 4  # Adjust for function definitions

    if function_call and function_call != "auto":
        tokens += (
            1
            if function_call == "none"
            else _estimate_string_tokens(function_call["name"]) + 4
        )

    return tokens

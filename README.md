
# OpenAI Function Tokens Estimator

Estimate OpenAI token usage for chat completions, including functions, with this Python utility!

This package is based upon `hmarr`'s [openai-chat-tokens](https://github.com/hmarr/openai-chat-tokens). As of right now (September 2023) there is no official documentation from openai on how to accurately predict the number of tokens from functions. This package solves that! Use it to get a very precise estimation of the token count for chat completions and better manage your OpenAI API usage.

Most often it is correct down to the token.

## Installation

1. **Install the Package via pip**

   ```console
   pip install openai_function_tokens
   ```

2. **Import the Estimation Function**

   ```python
   from openai_function_tokens import estimate_tokens
   ```

## Usage

To use the estimator, call the `estimate_tokens` function:

```python
estimate_tokens(messages, functions=None, function_call=None)
```

Pass in the `messages`, and optionally `functions` and `function_call`, to receive a precise token count.

## Acknowledgments

Credit to [hmarr](https://github.com/hmarr) for the original TypeScript tool. For a better understanding of token counting logic, check out his [blog post](https://hmarr.com/blog/counting-openai-tokens/).

## Further Reading

[Function Calling](https://platform.openai.com/docs/guides/gpt/function-calling)

[How to call functions with chat models](https://github.com/openai/openai-cookbook/blob/main/examples/How_to_call_functions_with_chat_models.ipynb)

[How to use functions with a knowledge base](https://github.com/openai/openai-cookbook/blob/main/examples/How_to_call_functions_for_knowledge_retrieval.ipynb)

[JSON Schema documentation](https://json-schema.org/understanding-json-schema/)

[Counting tokens (only messages)](https://json-schema.org/understanding-json-schema/)


## Contributing

Feedback, suggestions, and contributions are highly appreciated. Help make this tool even better!

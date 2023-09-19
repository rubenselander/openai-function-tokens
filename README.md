
# OpenAI Function Tokens

Predict the exact OpenAI token usage for openai functions!

This repository offers a Python implementation of `hmarr`'s [openai-chat-tokens](https://github.com/hmarr/openai-chat-tokens). With this tool, you can estimate the token count for a given chat completion (including the functions), helping you to efficiently manage your OpenAI usage.


## Quick Start

1. **Download the Repository**
   
   [Download the file](#) and place it in your project directory.
   
2. **Import the Function**

   ```python
   from openai_function_tokens import prompt_tokens_estimate
   ```

3. **Use the Estimator**

   Call the `prompt_tokens_estimate` function with the required parameters:

   ```python
   prompt_tokens_estimate(messages, functions=None, function_call=None)
   ```

   Provide the `messages`, and optionally `functions` and `function_call`, to get a precise token prediction before initiating a chat completion.

## Acknowledgments

Credit for the original TypeScript implementation goes to [hmarr](https://github.com/hmarr). You can learn more about the logic behind token counting in his [blog post](https://hmarr.com/blog/counting-openai-tokens/).

## Future Plans

If there's enough interest, a pip package version may be released in the future. Feedback and contributions are always welcome!

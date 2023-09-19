from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="openai-function-tokens",
    version="0.1.0",
    author="Reversehobo",
    author_email="info@nordicintel.com",
    description="A package to estimate token counts for messages AND functions in openai's chat completion API.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Reversehobo/openai-function-tokens",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "tiktoken",
    ],
    python_requires=">=3.6",
)

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="openai_function_tokens",
    version="0.1.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="A package to generate TypeScript function type definitions and estimate token counts.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/openai_function_tokens",  # replace with your repo URL
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

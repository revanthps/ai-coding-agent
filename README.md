
# ai-coding-agent

Lightweight AI coding agent utilities and examples — tools for reading files, running Python scripts, and writing files programmatically from a language model-driven agent.

## Overview

This project demonstrates a small framework that exposes filesystem and execution helper "tools" (via `langchain_core.tools`) which can be invoked by an LLM-driven agent to inspect, read, run, and write files inside a sandboxed working directory.

The repository also includes a tiny example application (a calculator) and simple test scripts that exercise the tools.

## Features

- Tools exposed for agent use:
	- List directory contents (`get_files_info`)
	- Read file contents (`get_file_content`)
	- Execute Python files (`run_python_file`)
	- Write files (`write_file`)
- Example chatbot runner that binds the tools to a `ChatHuggingFace` model (`main.py`).
- Small CLI calculator example in `calculator/`.

## Quickstart

Prerequisites

- Python 3.13+ (pyproject lists `requires-python = ">=3.13"`).
- Set environment variables (example uses a Hugging Face token):

```bash
export HF_TOKEN="<your_hf_token>"
```

Install dependencies (suggested via pip):

```bash
pip install -r requirements.txt || pip install google-genai==1.12.1 langchain-huggingface>=1.2.0 openai>=2.14.0 python-dotenv==1.1.0
```

Note: `pyproject.toml` lists the declared dependencies. You can adapt installation to your environment.

Running the chat agent (example)

```bash
python main.py "List files in the calculator folder"
```

The agent expects `HF_TOKEN` in the environment to call the configured Hugging Face endpoint.

Calculator example

```bash
python calculator/main.py "3 + 5"
```

This prints a JSON-like formatted result produced by the `calculator` package.

## Project Layout

- `main.py` — Example chat runner which binds tools to a `ChatHuggingFace` model and handles function/tool-call flow.
- `call_function.py` — Mapping and adapter to invoke the tool functions and return `ToolMessage` objects.
- `prompts.py` — System prompt used by the example agent.
- `functions/` — Tool implementations:
	- `get_file_content.py` — Read file content (with max chars and sandbox checks).
	- `get_files_info.py` — List files in a directory (size + is_dir info).
	- `run_python_file.py` — Execute Python files and capture stdout/stderr.
	- `write_file.py` — Write content to files inside the working directory safely.
- `calculator/` — Small example app demonstrating `run_python_file` and basic unit-like tests.
	- `calculator/main.py` — CLI entry for the calculator.
	- `calculator/pkg/calculator.py` — Calculator implementation.
	- `calculator/tests.py` — Basic exercise scripts for the tools.
- `tests_*.py` — Small test drivers that exercise the functions in `functions/`.

## Tools Behavior and Safety

All tools validate paths and confine operations to a provided `working_dir` to avoid arbitrary filesystem access. They return helpful error strings when an operation is disallowed or fails.

Examples of sandbox behavior:

- `get_file_content(working_dir, file_path)` checks that the resolved path is inside `working_dir` and truncates long files.
- `run_python_file(working_dir, file_path, args)` refuses to run files outside the working directory and returns captured stdout/stderr.

## Tests

The repository contains simple scripts to exercise each tool. You can run them directly, for example:

```bash
python tests_get_file_content.py
python tests_get_file_info.py
python tests_run_python_file.py
python tests_write_file.py
```

These scripts print tool results to stdout; they are lightweight sanity checks rather than a formal test suite.

## Development notes

- The example chat runner is configured to call a Hugging Face endpoint via `langchain_huggingface`. Replace or adapt the model configuration in `main.py` as needed.
- Tool functions use `langchain_core.tools.tool` to expose schemas and type hints; they return plain strings describing results or errors.







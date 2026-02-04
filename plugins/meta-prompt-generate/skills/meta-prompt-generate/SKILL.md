---
name: meta-prompt-generate
description: For creating prompt from scratch
---

# Introduction

`./meta-prompt-generate.py` is a script for generating prompt from scratch.

Below is it's usage:

```
usage: meta-prompt-generate.py [-h] -t TASK [-v VAR]

Generate prompt templates using Claude's meta-prompt technique.

options:
  -h, --help            show this help message and exit
  -t TASK, --task TASK  Task description for which to generate a prompt template
  -v VAR, --variable VAR
                        Input variable name (can be specified multiple times)

Environment variables:
  ANTHROPIC_AUTH_TOKEN   Required. Your Anthropic auth token.
  ANTHROPIC_BASE_URL  Optional. Custom base URL for the API.
  ANTHROPIC_MODEL     Optional. Model to use (default: claude-sonnet-4-5).

Examples:
  uv run --with anthropic meta-prompt-generate.py -t "Draft an email responding to a customer complaint"
  uv run --with anthropic meta-prompt-generate.py -t "Summarize a document" -v DOCUMENT -v MAX_LENGTH
```

# Instructions

Correctly invoke the script to generate prompt that user want.

---
name: self-improve
description: Custom memories management across claude code sessions that can be invoked manually.
---

This is a custom skill with two core functions: store and retrieve.

# Store

- Analyzes current Claude Code chat sessions following the instructions in ${CLAUDE_PLUGIN_ROOT}/skills/self-improve-report.md to generate a report
- In the report, for items worth saving for future use, use AskUserQuestionTool with multiple selections to prompt users to select the findings they want to store

# Retrieve

- It retrieves stored findings on demand—specifically those relevant to the current chat session—to help Claude Code perform better in the conversation.

# Use script to store/retrieve

Use ${CLAUDE_PLUGIN_ROOT}/skills/self-improve.py to store/retrieve. This is a cli script and the usage is as follows:

```
Usage: uv run --with chromadb --with typer self-improve.py [OPTIONS] COMMAND [ARGS]...

Store and retrieve strings via semantic search.

Options:
--install-completion          Install completion for the current shell.
--show-completion             Show completion for the current shell, to copy it or customize the installation.
--help                        Show this message and exit.

Commands:
add      Add strings to the database. Skips duplicates silently.
search   Search for related strings in the database.
```
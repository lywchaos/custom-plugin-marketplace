---
description: Review code for issues with extensible language support
argument-hint: "[language] [issue-type] [path]"
---

Interactive code review command that prompts for options and delegates to @code-reviewer agent.

## Instructions

### Step 1: Check for Arguments

If user provided arguments (`$ARGUMENTS` is not empty), parse them naturally and skip to Step 4.

Otherwise, proceed with interactive prompts.

### Step 2: Discover Available Options

1. List files in `${CLAUDE_PLUGIN_ROOT}/languages/` to find available languages
2. List files in `${CLAUDE_PLUGIN_ROOT}/issues/` to find available issue types

### Step 3: Ask User Questions

Use the AskUserQuestion tool with these questions:

```json
{
  "questions": [
    {
      "header": "Language",
      "question": "Which language should I focus on?",
      "multiSelect": false,
      "options": [
        {"label": "Auto-detect (Recommended)", "description": "Detect language from file extensions in scope"},
        {"label": "Python", "description": "Review only Python (.py) files"}
      ]
    },
    {
      "header": "Issue type",
      "question": "What types of issues should I check for?",
      "multiSelect": true,
      "options": [
        {"label": "All issues (Recommended)", "description": "Check for all available issue types"},
        {"label": "Deadcode", "description": "Find unused code, imports, and functions"}
      ]
    },
    {
      "header": "Scope",
      "question": "Which files should I review?",
      "multiSelect": false,
      "options": [
        {"label": "Git changes (Recommended)", "description": "Uncommitted changes + branch diff from main"},
        {"label": "Current directory", "description": "All supported files in current working directory"},
        {"label": "Entire repository", "description": "All supported files in the repository"}
      ]
    }
  ]
}
```

**Important**: Dynamically add options based on discovered languages and issues. The examples above show Python and Deadcode, but include any other discovered options.

### Step 4: Launch Code Reviewer

Pass the selected options to @code-reviewer agent:

- **Language**: The selected language or "auto-detect"
- **Issue types**: The selected issue type(s) or "all"
- **Scope**: The selected scope (git diff, directory path, or repo root)

The agent will perform the review and return its findings.

### Step 5: Present Results

**IMPORTANT**: When the code-reviewer agent returns its report, output the **full report verbatim** to the user. Do NOT summarize, condense, paraphrase, or omit any part of the agent's output. Preserve the exact markdown formatting including all severity headers, evidence bullets, location references, and suggestions. The user expects the complete structured report as-is.

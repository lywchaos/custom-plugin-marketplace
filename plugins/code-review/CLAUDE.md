# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

Extensible code review plugin with composable language and issue type support. Uses a composition pattern where language-specific instructions and issue-type instructions are combined at runtime.

## Architecture

```
commands/code-review.md    # Entry point - interactive prompts, delegates to agent
agents/code-reviewer.md    # Core logic - discovery, scoping, analysis, output format
languages/<lang>.md        # Non-obvious language-specific patterns
issues/<issue>.md          # Issue-type detection rules (categories, severity, evidence)
```

**Composition flow**: Command prompts user -> Agent discovers `languages/` and `issues/` files -> Agent reads and combines instructions -> Agent performs analysis

## Extending the Plugin

### Add a new language

Create `languages/<name>.md` with non-obvious language-specific patterns:
- False positive patterns (code that looks dead but isn't)
- Tracing strategies (where to look for hidden references)
- Import resolution quirks
- Metaprogramming awareness

**Avoid obvious content** like file extensions or basic syntax - the AI already knows these.

### Add a new issue type

Create `issues/<name>.md` with:
- Detection categories and what constitutes that issue
- Severity guidelines for each category
- Analysis process (symbol collection, reference search, evidence)
- Suppression comment patterns

New files are auto-discovered - no configuration needed.

## Key Patterns

- **Scope default**: `git diff` (uncommitted) + branch diff from main
- **Exclusions**: Test files, hidden dirs, node_modules, venvs
- **Suppression**: `# noqa: <issue>` or `# code-review: ignore`
- **Severity levels**: BLOCKER > CRITICAL > MAJOR > MINOR > TRIVIAL
- **Output**: Inline conversation, grouped by severity, with evidence

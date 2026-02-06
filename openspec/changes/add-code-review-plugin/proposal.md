# Change: Add extensible code-review plugin

## Why
Create a unified, extensible code review plugin that supports multiple languages and issue types through composable AI instruction files. This consolidates code analysis capabilities and establishes a scalable pattern for adding new review rules.

## What Changes
- **ADDED**: New `plugins/code-review/` plugin with composable architecture
- **ADDED**: Language instruction files under `languages/` (starting with Python)
- **ADDED**: Issue type instruction files under `issues/` (starting with deadcode)
- **ADDED**: `/code-review` slash command with natural language arguments
- **REMOVED**: `deadcode-inspector` agent from `plugins/code-simplify/` (migrated to code-review)

## Impact
- Affected specs: None (new capability)
- Affected code: `plugins/code-review/` (new), `plugins/code-simplify/agents/deadcode-inspector.md` (removed)
- Migration: Users invoking deadcode-inspector agent will need to use `/code-review deadcode` instead

<!-- OPENSPEC:START -->
# OpenSpec Instructions

These instructions are for AI assistants working in this project.

Always open `@/openspec/AGENTS.md` when the request:
- Mentions planning or proposals (words like proposal, spec, change, plan)
- Introduces new capabilities, breaking changes, architecture shifts, or big performance/security work
- Sounds ambiguous and you need the authoritative spec before coding

Use `@/openspec/AGENTS.md` to learn:
- How to create and apply change proposals
- Spec format and conventions
- Project structure and guidelines

Keep this managed block so 'openspec update' can refresh the instructions.

<!-- OPENSPEC:END -->

# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

This is a custom plugin marketplace for Claude Code. It contains a collection of plugins that extend Claude Code functionality.

## Repository Structure

```
.claude-plugin/marketplace.json  # Marketplace manifest - lists all plugins
plugins/<plugin-name>/           # Individual plugins
  .claude-plugin/plugin.json     # Plugin manifest (name, description, version, author)
  commands/*.md                  # Slash commands (markdown with YAML frontmatter)
  skills/<skill-name>/           # Skills with SKILL.md and supporting scripts
  agents/*.md                    # Agent definitions (markdown with YAML frontmatter)
  hooks/hooks.json               # Hook configurations
  .mcp.json                      # MCP server configuration (optional)
```

## Plugin Components

**New plugins must be registered** in `.claude-plugin/marketplace.json` to be installable.

**Commands** (`commands/*.md`): Frontmatter with `description` and optional `argument-hint`.

**Skills** (`skills/<name>/SKILL.md`): Frontmatter with `name` and `description`. Supporting scripts use `uv run --with <deps>` pattern.

**Agents** (`agents/*.md`): Frontmatter with `name` and `description`.

**Hooks** (`hooks/hooks.json`): Define hook type (Notification, Stop, etc.) and command to execute. Use `${CLAUDE_PLUGIN_ROOT}` for paths.

**MCP Servers** (`.mcp.json`): Define MCP server connections with type, url, and headers. Use `${ENV_VAR}` for secrets.

## Current Plugins

- **self-improve**: Custom memories management with store/retrieve via ChromaDB
- **meta-prompt-generate**: Generate prompts using Claude's meta-prompt technique
- **code-simplify**: Code simplification with code-simplifier agent
- **code-review**: Extensible code review with composable language/issue support (Python; deadcode, simplicity)
- **context7-mcp**: Context7 MCP server integration
- **thariq-interview**: Interactive plan interviewing
- **claude-code-notify**: Notification hooks for Claude Code events

## Pre-commit

Uses gitleaks for secret detection.

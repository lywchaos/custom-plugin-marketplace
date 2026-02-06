## Context

The user wants an extensible code review plugin that can:
1. Support multiple programming languages (starting with Python)
2. Support multiple issue types (starting with deadcode)
3. Be easily extended by adding markdown files without code changes

Current state: `code-simplify` plugin has a `deadcode-inspector` agent that will be migrated into this new plugin.

## Goals / Non-Goals

### Goals
- Single unified code-review entry point via `/code-review` command
- Composable architecture: `languages/*.md` + `issues/*.md` files combined at runtime
- File-based auto-discovery for new languages and issue types
- Natural language argument parsing (no rigid CLI syntax)
- Inline conversation output with severity-based grouping
- Default scope: git diff + branch diff from default branch

### Non-Goals
- External tool invocation (vulture, pylint, ruff) - reference only
- Automated fixing (suggestions only, no auto-apply)
- Report file generation (inline output only)
- Test file analysis (excluded from scope)

## Architecture Decisions

### Decision: Single agent with pluggable rules
**What**: One code-review command that dynamically loads and composes language + issue instruction files.
**Why**: Simpler invocation (`/code-review` instead of `/python-deadcode-review`), easier to understand, avoids agent explosion.
**Alternatives considered**:
- Separate agents per combination (rejected: maintenance burden, complex invocation)
- Layered base + adapters (rejected: unnecessary complexity for markdown-based rules)

### Decision: Composable language + issue files
**What**: Separate directories for `languages/` and `issues/` that get combined.
**Why**: Maximum reuse - Python instructions apply to all Python issue types, deadcode instructions apply to all languages.
**Structure**:
```
plugins/code-review/
  commands/code-review.md    # Entry point
  languages/
    python.md                # Python-specific context
  issues/
    deadcode.md              # Deadcode detection rules
```

### Decision: File-based auto-discovery
**What**: Drop a file in `languages/` or `issues/` and it's automatically available.
**Why**: Zero-config extension, no registry to maintain, consistent with plugin pattern.
**Trade-off**: No validation of file content until runtime.

### Decision: Natural language arguments
**What**: `/code-review python deadcode src/` or `/code-review review deadcode in my changed files` - AI parses intent.
**Why**: More flexible, user-friendly, aligns with Claude Code's conversational nature.
**Trade-off**: Less predictable than structured flags.

### Decision: Inline output with severity grouping
**What**: Print findings directly in conversation, grouped by severity (Blocker > Critical > Major > Minor > Trivial).
**Why**: Interactive flow, immediate discussion, no file management.

### Decision: Git-based default scope
**What**: Default to `git diff` (uncommitted changes) + diff between current branch and default branch.
**Why**: Focuses on active work, avoids reviewing unchanged code.

## Output Format

### Summary Section
```
## Code Review Summary
- **Files reviewed**: 5 files (src/auth.py, src/utils.py, ...)
- **Issues found**: 3 (1 Critical, 2 Minor)
- **Assessment**: Several unused functions detected in authentication module
```

### Finding Format (detailed with evidence)
```
### [CRITICAL] Unused function `validate_token`
**Location**: src/auth.py:42-58
**Evidence**:
- No references found in codebase (searched all .py files)
- Function was added in commit abc123 but never integrated
- Similar function `verify_token` exists and is used instead
**Suggestion**: Remove function or integrate into authentication flow
```

### No Issues Format
```
## Code Review Complete
No issues found. Reviewed 5 files covering 342 lines of Python code in scope.
```

## Severity Levels

| Level | Meaning | Example |
|-------|---------|---------|
| BLOCKER | Prevents deployment/merge | Syntax error, import of deleted module |
| CRITICAL | Must fix before release | Unused exported API, unreachable critical path |
| MAJOR | Should fix soon | Unused internal functions, dead branches |
| MINOR | Fix when convenient | Unused imports, commented-out code blocks |
| TRIVIAL | Style/cleanup | Unused variables in comprehensions |

## Suppression Mechanism

Inline comments to suppress findings:
```python
from typing import Optional  # noqa: deadcode
from deprecated_module import helper  # code-review: ignore

def unused_but_intentional():  # noqa: deadcode
    pass
```

## Risks / Trade-offs

- **Risk**: AI may miss dynamically-referenced code
  - Mitigation: Attempt deeper analysis of reflection patterns, flag uncertainty

- **Risk**: Natural language parsing may misinterpret user intent
  - Mitigation: Show interpretation in output ("Reviewing Python files for deadcode issues...")

- **Risk**: Large diffs may produce overwhelming output
  - Mitigation: Summary first, severity grouping, user can ask for specific file focus

## Migration Plan

1. Create code-review plugin with deadcode issue type
2. Verify functionality matches deadcode-inspector capabilities
3. Remove deadcode-inspector.md from code-simplify
4. Update any documentation referencing deadcode-inspector

## Open Questions

None - all clarified during interview.

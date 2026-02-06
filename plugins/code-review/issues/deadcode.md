# Deadcode Detection

This file provides instructions for detecting dead code, unused code, and backward-compatibility artifacts.

## What is Dead Code?

Dead code is code that:
- Is never referenced or invoked anywhere in the codebase
- Is unreachable due to control flow (after unconditional returns, breaks)
- Is guarded by conditions that are always false
- Has been replaced by newer implementations but not removed
- Is commented out but left in place
- Exists only for backward compatibility with deprecated features

## Detection Categories

### 1. Unused Imports
- Modules imported but no symbols used from them
- Specific symbols imported but never referenced
- Wildcard imports where most symbols are unused

**Severity**: MINOR

### 2. Unused Functions/Methods
- Functions defined but never called
- Methods that override nothing and are never invoked
- Helper functions whose callers were removed

**Severity**:
- MAJOR for internal functions
- CRITICAL for exported/public functions (may indicate broken API)

### 3. Unused Classes
- Classes defined but never instantiated or subclassed
- Exception classes never raised
- Dataclasses/models never used

**Severity**: MAJOR (CRITICAL if exported)

### 4. Unused Variables
- Variables assigned but never read
- Loop variables not used in loop body
- Exception variables in except blocks never used

**Severity**: MINOR (TRIVIAL for loop/exception variables)

### 5. Unreachable Code
- Code after unconditional return/raise/break/continue
- Code in branches that can never execute
- Code guarded by `if False:` or `if 0:`

**Severity**: MAJOR

### 6. Commented-Out Code
- Large blocks of commented code (not documentation)
- Commented function/class definitions
- "TODO: remove" or "deprecated" markers with actual code

**Severity**: MINOR

### 7. Backward-Compatibility Code
- Shims for old API versions
- Feature flags that are always true/false
- Version checks for unsupported versions
- Deprecated parameter handling

**Severity**: MAJOR (may be intentional - flag as uncertain if deprecation period unclear)

## Analysis Process

### Step 1: Symbol Collection
Collect all defined symbols in scope:
- Function definitions
- Class definitions
- Variable assignments
- Import statements

### Step 2: Reference Search
For each symbol, search for references:
- Direct calls/accesses
- Attribute access on objects
- Inheritance relationships
- Decorator usage
- Export lists (`__all__`)

Use Grep tool to search across the codebase for symbol usage.

### Step 3: Dynamic Usage Analysis
When you encounter dynamic patterns, trace them:
- Follow `getattr` calls to see what strings are used
- Check configuration files for string references
- Look for reflection patterns and metaprogramming
- Consider framework conventions (routes, signals, hooks)

If dynamic usage is possible but uncertain, classify as uncertain and note in evidence.

### Step 4: Evidence Collection
For each finding, gather concrete evidence:
- **No references found**: Show grep results confirming zero usage
- **Unreachable**: Show the control flow that makes it unreachable
- **Conditional**: Show the condition and why it's always false/true
- **Superseded**: Identify the replacement code

## Severity Guidelines

| Severity | Criteria |
|----------|----------|
| BLOCKER | Dead code causes import/compilation errors |
| CRITICAL | Unused exported APIs, unreachable critical business logic |
| MAJOR | Unused internal functions, dead feature branches, backward-compat code |
| MINOR | Unused imports, commented-out code blocks |
| TRIVIAL | Unused loop variables, exception aliases |

## Uncertainty Handling

When you cannot definitively determine if code is dead:
- Check for dynamic invocation patterns
- Look for framework-specific magic (decorators, naming conventions)
- Search for string-based references
- Check test files (even though excluded from review, they may reference code)

If still uncertain, report the finding but:
1. Classify as one level lower severity than otherwise
2. Add "UNCERTAIN" prefix to the description
3. Document why you're uncertain in evidence
4. Suggest manual verification

## Suppression

Skip findings for lines with these comments:
- `# noqa: deadcode`
- `# code-review: ignore`
- `// noqa: deadcode` (JS/TS)
- `// code-review: ignore`

Also consider these as intentional:
- `# TODO: remove after X` (flag but note timeline)
- `# deprecated` (flag as backward-compat)
- `# pragma: no cover` (may indicate intentional dead code for coverage)

# Simplicity

This file provides instructions for detecting code simplicity issues - unnecessary complexity, over-engineering, patterns that reduce maintainability and so on.

## What are Simplicity Issues?

Code that:
- Is more complex than necessary to achieve its goal
- Uses abstractions or patterns that add no clear value
- Prioritizes cleverness or brevity over readability
- Contains redundant logic that should be consolidated
- Has poor naming that obscures intent

## Detection Categories

### 1. Unnecessary Complexity

Deep nesting, convoluted control flow, or overly complex expressions.

**Examples**:
- Conditionals nested 3+ levels deep
- Boolean expressions with 4+ conditions
- Multiple early returns mixed with nested if/else
- Switch/case with fallthrough that's hard to follow

**Severity**: MAJOR

### 2. Over-Engineering

Premature abstractions or excessive indirection that adds no value.

**Examples**:
- Single-use utility functions that could be inlined
- Wrapper functions that just call another function
- Abstract base classes with only one implementation
- Configuration for values that never change
- Dependency injection where direct instantiation suffices
- Strategy/factory patterns for 2 simple cases

**Severity**: MAJOR

### 3. Redundant Code

Duplicate or verbose patterns that should be simplified.

**Examples**:
- Copy-pasted logic with minor variations
- Verbose null checks where language provides simpler alternatives
- Unnecessary intermediate variables that are used once
- Re-implementing standard library functionality
- Multiple functions that do nearly the same thing

**Severity**: MINOR

### 4. Poor Naming

Names that don't clearly convey purpose or are misleading.

**Examples**:
- Single-letter variables outside tight loops
- Generic names: `data`, `info`, `temp`, `result`, `handler`
- Misleading names: `isValid` that doesn't return boolean
- Inconsistent naming: mixing `getUserName` and `fetch_user_email`
- Abbreviations that aren't universally understood

**Severity**: MINOR

### 5. Overly Compact Code

Code that sacrifices readability for brevity.

**Examples**:
- Dense one-liners with multiple operations
- Chained method calls spanning 5+ operations
- Nested ternary operators
- Clever bitwise tricks where arithmetic is clearer
- Regex that should be broken into readable parts

**Severity**: MAJOR

## Analysis Process

### Step 1: Complexity Assessment

For each function/method:
- Count nesting depth (flag if > 3)
- Count cyclomatic complexity indicators (branches, loops)
- Check for long parameter lists (> 4 parameters)
- Look for functions longer than ~50 lines

### Step 2: Abstraction Analysis

Look for signs of over-engineering:
- Classes/functions used only once
- Layers that just pass through to another layer
- Interfaces with single implementations
- Configuration that's never configured differently

### Step 3: Duplication Detection

Search for:
- Similar code blocks in nearby locations
- Functions with overlapping functionality
- Repeated patterns that could be extracted

### Step 4: Naming Review

Check that names:
- Describe what, not how
- Are consistent with surrounding code
- Match the actual behavior
- Use domain terminology appropriately

## Severity Guidelines

| Severity | Criteria |
|----------|----------|
| BLOCKER | Complexity makes code unmaintainable or buggy |
| CRITICAL | Over-engineering that significantly impedes changes |
| MAJOR | Unnecessary complexity, overly compact code, premature abstractions |
| MINOR | Redundant code, poor naming, verbose patterns |
| TRIVIAL | Minor style inconsistencies |

## Key Principle

**Simplicity is not about fewer lines of code.** The goal is code that:
- Is easy to read and understand
- Is easy to modify without introducing bugs
- Does one thing well
- Uses the simplest approach that works

Explicit, readable code is better than clever, compact code.

## Suppression

Skip findings for lines with these comments:
- `# noqa: simplicity`
- `# code-review: ignore`
- `// noqa: simplicity`
- `// code-review: ignore`

Also consider as intentional:
- `# complexity justified: <reason>` - acknowledged necessary complexity
- Performance-critical code with documented benchmarks

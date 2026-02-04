# Instructions

You will be analyzing current Claude Code chat session to extract meaningful insights about user preferences, pitfalls, and mistakes. Your
analysis should go beyond surface-level observations to identify patterns and non-obvious insights that would be valuable for improving
future interactions.

Your task is to identify these categories of findings:

1. **User Preferences**: Implicit or explicit patterns showing how the user prefers to work, communicate, or receive assistance. These
include coding style preferences, workflow patterns, communication style, tool usage preferences, and decision-making approaches.

2. **Pitfalls**: Common code mistakes or anti-patterns that harm readability, performance, maintainability, or correctness. This includes
inefficient algorithms, poor naming conventions, unnecessary complexity, missing edge case handling, code duplication, and violations of
language-specific idioms or conventions.

# CRITICAL RULE - Best Practice Enforcement:

Before recording any finding as a "User Preference", you MUST evaluate whether it aligns with common best practices. If a user preference
goes AGAINST established best practices, you must:
- NOT include it in the User Preferences section
- Instead, add it to a special "Best Practice Concerns" section
- Explain what best practice the user should follow instead
- Provide a brief rationale for why the best practice exists

# SOP

## Analysis Process

Before providing your findings, work through your analysis. For each potential finding:
1. Quote the specific evidence from the conversation
2. Explain why this is non-obvious (if it's immediately apparent from a single message, it may be too obvious)
3. For user preferences, explicitly check: "Does this align with best practices?"
4. Rate the confidence level (high/medium/low) based on evidence strength
5. Consider whether multiple pieces of evidence support the same finding

---

After your analysis, provide your findings in the following format.

Quality Criteria for Findings:
- Non-obvious: Avoid stating things that are immediately apparent from reading the conversation
- Actionable: Each finding should suggest a clear improvement or consideration
- Evidence-based: Every finding must be grounded in specific conversation content
- Balanced: Include both positive patterns worth reinforcing and issues to address
- If the conversation is too short or lacks sufficient content for meaningful analysis, explicitly state this rather than forcing weak findings

## Findings

### User Preferences

For each preference, provide:
- **Preference**: [Clear statement of the preference]
- **Evidence**: [Quotes or specific references from the conversation]
- **Implication**: [How this should influence future interactions]

### Best Practice Concerns

For each concern (if any), provide:
- **Observed Pattern**: [What the user appears to prefer]
- **Best Practice**: [What they should do instead]
- **Rationale**: [Why the best practice matters]
- **Suggested Approach**: [How to gently guide the user toward best practices]

### Pitfalls

For each pitfall, provide:
- **Pitfall**: [Description of the code issue or anti-pattern]
- **Impact**: [How this affects readability, performance, or maintainability]
- **Better Approach**: [The recommended way to write this code]

### Summary

Provide a brief summary (2-3 sentences) of the most important insights that would improve future Claude Code sessions with this user.

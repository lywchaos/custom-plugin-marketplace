## ADDED Requirements

### Requirement: Code Review Plugin Structure
The code-review plugin SHALL provide a composable architecture with separate language and issue type instruction files.

#### Scenario: Plugin manifest exists
- **WHEN** the plugin is loaded
- **THEN** it SHALL have a valid `plugin.json` manifest at `.claude-plugin/plugin.json`

#### Scenario: Directory structure supports composition
- **WHEN** the plugin is installed
- **THEN** it SHALL have a `languages/` directory for language-specific instructions
- **AND** it SHALL have an `issues/` directory for issue-type-specific instructions

### Requirement: Slash Command Entry Point
The plugin SHALL provide a `/code-review` slash command as the primary entry point.

#### Scenario: Command invocation with no arguments
- **WHEN** user invokes `/code-review` without arguments
- **THEN** the system SHALL auto-detect language from files in scope
- **AND** SHALL apply all available issue types

#### Scenario: Command invocation with language only
- **WHEN** user invokes `/code-review python`
- **THEN** the system SHALL apply all issue types to Python files only

#### Scenario: Command invocation with issue type only
- **WHEN** user invokes `/code-review deadcode`
- **THEN** the system SHALL auto-detect language and apply deadcode analysis

#### Scenario: Command invocation with both language and issue
- **WHEN** user invokes `/code-review python deadcode`
- **THEN** the system SHALL analyze Python files for deadcode issues only

#### Scenario: Natural language arguments
- **WHEN** user provides natural language like "review my python changes for dead code"
- **THEN** the system SHALL parse intent and apply appropriate language and issue filters

### Requirement: Default Scope Based on Git Diff
The plugin SHALL default to reviewing files with uncommitted changes and changes from the default branch.

#### Scenario: Default scope with uncommitted changes
- **WHEN** user invokes `/code-review` without specifying a path
- **AND** there are uncommitted changes (staged or unstaged)
- **THEN** the system SHALL include those changed files in scope

#### Scenario: Default scope with branch diff
- **WHEN** user is on a feature branch
- **THEN** the system SHALL also include files changed compared to the default branch

#### Scenario: Explicit path overrides default
- **WHEN** user specifies a path like `/code-review src/`
- **THEN** the system SHALL use the specified path instead of git-based defaults

### Requirement: File-Based Auto-Discovery
The plugin SHALL automatically discover available languages and issue types from file existence.

#### Scenario: New language added
- **WHEN** a new file `languages/typescript.md` is added to the plugin
- **THEN** TypeScript SHALL become available as a language option without config changes

#### Scenario: New issue type added
- **WHEN** a new file `issues/security.md` is added to the plugin
- **THEN** security analysis SHALL become available as an issue type without config changes

#### Scenario: All combinations valid
- **WHEN** a language file and issue type file both exist
- **THEN** the system SHALL allow combining them regardless of semantic compatibility
- **AND** the AI SHALL handle any mismatch gracefully

### Requirement: Severity Classification
The plugin SHALL use a five-level severity classification for all findings.

#### Scenario: Severity levels defined
- **WHEN** a finding is reported
- **THEN** it SHALL be classified as one of: BLOCKER, CRITICAL, MAJOR, MINOR, or TRIVIAL

#### Scenario: Blocker severity
- **WHEN** an issue prevents deployment or compilation
- **THEN** it SHALL be classified as BLOCKER

#### Scenario: Critical severity
- **WHEN** an issue represents unused exported APIs or unreachable critical code
- **THEN** it SHALL be classified as CRITICAL

#### Scenario: Major severity
- **WHEN** an issue represents unused internal functions or dead branches
- **THEN** it SHALL be classified as MAJOR

#### Scenario: Minor severity
- **WHEN** an issue represents unused imports or commented-out code
- **THEN** it SHALL be classified as MINOR

#### Scenario: Trivial severity
- **WHEN** an issue represents minor style concerns like unused loop variables
- **THEN** it SHALL be classified as TRIVIAL

### Requirement: Inline Conversation Output
The plugin SHALL output findings directly in the conversation, not to files.

#### Scenario: Output format with findings
- **WHEN** issues are found
- **THEN** the output SHALL include a summary section with counts, file list, and assessment
- **AND** the output SHALL include detailed finding blocks grouped by severity (highest first)

#### Scenario: Finding detail includes evidence
- **WHEN** a finding is reported
- **THEN** it SHALL include location (file:line), evidence supporting the finding, and a concise suggestion

#### Scenario: No issues found
- **WHEN** no issues are found
- **THEN** the output SHALL confirm completion with scope information (files/lines reviewed)

### Requirement: Suppression via Inline Comments
The plugin SHALL support suppressing findings via inline comments.

#### Scenario: noqa comment suppresses finding
- **WHEN** code is annotated with `# noqa: deadcode` comment
- **THEN** deadcode findings for that line SHALL be suppressed

#### Scenario: code-review ignore suppresses finding
- **WHEN** code is annotated with `# code-review: ignore` comment
- **THEN** all findings for that line SHALL be suppressed

### Requirement: Test File Exclusion
The plugin SHALL exclude test files from analysis by default.

#### Scenario: Test directories excluded
- **WHEN** analyzing a codebase
- **THEN** files in `**/tests/**`, `**/test/**`, `**/*_test.py`, `**/*_spec.py` patterns SHALL be excluded

### Requirement: Python Language Support
The plugin SHALL include Python as an initial supported language.

#### Scenario: Python language file exists
- **WHEN** the plugin is installed
- **THEN** `languages/python.md` SHALL exist with Python-specific analysis instructions

#### Scenario: Python file detection
- **WHEN** auto-detecting language
- **AND** files with `.py` extension are in scope
- **THEN** Python language instructions SHALL be applied

### Requirement: Deadcode Issue Type Support
The plugin SHALL include deadcode detection as an initial supported issue type.

#### Scenario: Deadcode issue file exists
- **WHEN** the plugin is installed
- **THEN** `issues/deadcode.md` SHALL exist with deadcode detection instructions

#### Scenario: Deadcode detection patterns
- **WHEN** analyzing for deadcode
- **THEN** the system SHALL detect: unused functions, unused classes, unused imports, unused variables, unreachable code, and commented-out code blocks

#### Scenario: Dynamic code analysis attempted
- **WHEN** code uses reflection, getattr, or dynamic imports
- **THEN** the system SHALL attempt to trace dynamic references rather than immediately flagging as dead

### Requirement: External Tool References
The plugin SHALL reference external static analysis tools without requiring them.

#### Scenario: Tool references in instructions
- **WHEN** the deadcode issue instructions are composed
- **THEN** they MAY reference tools like vulture, pylint, ruff as validation approaches
- **BUT** the analysis SHALL NOT require these tools to be installed

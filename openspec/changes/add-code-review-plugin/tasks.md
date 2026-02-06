## 1. Plugin Structure
- [x] 1.1 Create `plugins/code-review/.claude-plugin/plugin.json` manifest
- [x] 1.2 Create `plugins/code-review/commands/code-review.md` slash command
- [x] 1.3 Create `plugins/code-review/languages/` directory structure
- [x] 1.4 Create `plugins/code-review/issues/` directory structure

## 2. Language Support (Python)
- [x] 2.1 Create `plugins/code-review/languages/python.md` with Python-specific analysis instructions

## 3. Issue Type Support (Deadcode)
- [x] 3.1 Create `plugins/code-review/issues/deadcode.md` with deadcode detection instructions
- [x] 3.2 Include severity classification (Blocker/Critical/Major/Minor/Trivial)
- [x] 3.3 Include suppression comment support (`# noqa: deadcode`, `# code-review: ignore`)

## 4. Migration
- [x] 4.1 Remove `plugins/code-simplify/agents/deadcode-inspector.md`
- [x] 4.2 Update `plugins/code-simplify/.claude-plugin/plugin.json` if needed (no changes needed - agents are auto-discovered)

## 5. Documentation
- [x] 5.1 Update marketplace CLAUDE.md with code-review plugin description

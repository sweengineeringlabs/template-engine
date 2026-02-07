# Documentation Compliance Checklist

**Audience**: Developers, architects, documentation maintainers

Use this checklist to audit any project against the [FRAMEWORK.md](FRAMEWORK.md) documentation standards. Run through each section and record pass/fail status. The checklist is ordered by priority: structural issues first, then content, then polish.

## How to Use

1. Copy this checklist into your project or open it side-by-side
2. Run the grep/find commands provided for automated checks
3. Mark each item and note any files that need fixing
4. Address failures in order (structure before content)

---

## 1. Directory Structure

### 1.1 Root documentation folder

| # | Check | Pass | Notes |
|---|-------|------|-------|
| 1 | Root docs folder is `docs/` (plural) | | |
| 2 | `docs/README.md` hub document exists | | |
| 3 | `docs/glossary.md` exists | | |

**Verify**:
```bash
# Must exist
ls docs/README.md docs/glossary.md

# Must NOT exist at root (should be docs/)
ls doc/ 2>/dev/null && echo "FAIL: root doc/ should be docs/"
```

### 1.2 Module/crate documentation folders

| # | Check | Pass | Notes |
|---|-------|------|-------|
| 4 | All module doc folders use `docs/` (plural) | | |
| 5 | Each module has a single `docs/` folder | | |

**Verify**:
```bash
# Find violations (should return nothing)
find crates/ modules/ packages/ -maxdepth 2 -type d -name "doc" 2>/dev/null

# Find split-personality modules (both doc/ and docs/)
for d in crates/*/; do
  [ -d "$d/doc" ] && [ -d "$d/docs" ] && echo "FAIL: $d has both doc/ and docs/"
done
```

### 1.3 Architecture compliance checklist

| # | Check | Pass | Notes |
|---|-------|------|-------|
| 6 | `docs/3-design/compliance/compliance_checklist.md` exists | | |
| 7 | Compliance checklist reflects current `architecture.md` rules | | |
| 8 | Every enforceable rule in `architecture.md` has a corresponding checkbox | | |

**Verify**:
```bash
# Must exist
ls docs/3-design/compliance/compliance_checklist.md

# Should reference architecture.md
grep -l 'architecture.md' docs/3-design/compliance/compliance_checklist.md
```

### 1.4 SDLC phase directories

| # | Check | Pass | Notes |
|---|-------|------|-------|
| 9 | Phase numbering is correct (see table below) | | |
| 10 | Phases appear in correct order (requirements before planning) | | |

Reference: `0-ideation/`, `1-requirements/`, `2-planning/`, `3-design/`, `4-development/`, `5-testing/`, `6-deployment/`, `7-operation/`

### 1.5 Subdirectory naming

| # | Check | Pass | Notes |
|---|-------|------|-------|
| 11 | ADRs in `3-design/adr/` with `NNN-title.md` format | | |
| 12 | Developer guides in `4-development/guide/` (singular) | | |
| 13 | UX/UI assets in `3-design/uxui/` | | |

**Verify**:
```bash
# Must NOT exist (plural guides/)
find . -type d -name "guides" -path "*/4-development/*" 2>/dev/null

# Must NOT exist (wrong order)
find . -type d -name "uiux" 2>/dev/null
```

---

## 2. File Naming

### 2.1 Git standard files (UPPERCASE)

| # | Check | Pass | Notes |
|---|-------|------|-------|
| 14 | `README.md` — UPPERCASE | | |
| 15 | `CONTRIBUTING.md` — UPPERCASE | | |
| 16 | `CHANGELOG.md` — UPPERCASE | | |
| 17 | `SECURITY.md` — UPPERCASE | | |
| 18 | `LICENSE` — UPPERCASE | | |
| 19 | `CODE_OF_CONDUCT.md` — UPPERCASE (if present) | | |
| 20 | `SUPPORT.md` — UPPERCASE (if present) | | |

### 2.2 Project documentation (lowercase-with-hyphens)

| # | Check | Pass | Notes |
|---|-------|------|-------|
| 21 | All filenames in `docs/` are lowercase (except README.md) | | |
| 22 | All filenames use hyphens as separators | | |
| 23 | All filenames are space-free | | |

**Verify**:
```bash
# Find UPPERCASE violations in docs/ (excluding README.md, git standard files)
find docs/ -name "*.md" | grep -E '/[A-Z]{2,}' | grep -v README | grep -v CHANGELOG | grep -v CONTRIBUTING | grep -v SECURITY | grep -v CODE_OF_CONDUCT | grep -v SUPPORT | grep -v LICENSE

# Find underscore violations
find docs/ -name "*_*" -name "*.md"

# Same checks in module docs
find crates/ -path "*/docs/*.md" -name "*_*" 2>/dev/null
find crates/ -path "*/docs/*.md" | grep -E '/[A-Z]{2,}' | grep -v README 2>/dev/null
```

---

## 3. Required Root Files

| # | Check | Pass | Notes |
|---|-------|------|-------|
| 24 | `README.md` exists at root | | |
| 25 | `CONTRIBUTING.md` exists at root | | |
| 26 | `CHANGELOG.md` exists at root | | |
| 27 | `SECURITY.md` exists at root | | |
| 28 | `LICENSE` exists at root | | |

**For open-source projects, also check**:
| # | Check | Pass | Notes |
|---|-------|------|-------|
| 29 | `CODE_OF_CONDUCT.md` exists | | |
| 30 | `SUPPORT.md` exists | | |
| 31 | `.github/ISSUE_TEMPLATE/` exists | | |
| 32 | `.github/PULL_REQUEST_TEMPLATE.md` exists | | |

**Verify**:
```bash
# Check all required files exist
for f in README.md CONTRIBUTING.md CHANGELOG.md SECURITY.md LICENSE; do
  [ -f "$f" ] && echo "PASS: $f" || echo "FAIL: $f missing"
done
```

---

## 4. Content Patterns

### 4.1 Audience declaration

| # | Check | Pass | Notes |
|---|-------|------|-------|
| 33 | Every `.md` file in `docs/` has `**Audience**:` declaration | | |
| 34 | Every module `docs/` README has `**Audience**:` declaration | | |

**Verify**:
```bash
# Find docs missing Audience declaration
for f in $(find docs/ -name "*.md"); do
  grep -qL '^\*\*Audience\*\*' "$f" && echo "MISSING: $f"
done
```

### 4.2 TLDR blockquote (200+ line docs only)

| # | Check | Pass | Notes |
|---|-------|------|-------|
| 35 | Docs with 200+ lines have `> **TLDR**:` blockquote | | |
| 36 | Docs under 200 lines omit TLDR | | |

**Verify**:
```bash
# Find 200+ line docs missing TLDR
for f in $(find docs/ -name "*.md"); do
  lines=$(wc -l < "$f")
  if [ "$lines" -ge 200 ]; then
    grep -qL '> \*\*TLDR\*\*' "$f" && echo "NEEDS TLDR ($lines lines): $f"
  fi
done

# Find short docs that have TLDR (should not)
for f in $(find docs/ -name "*.md"); do
  lines=$(wc -l < "$f")
  if [ "$lines" -lt 200 ]; then
    grep -ql '> \*\*TLDR\*\*' "$f" && echo "REMOVE TLDR ($lines lines): $f"
  fi
done
```

### 4.3 Glossary format

| # | Check | Pass | Notes |
|---|-------|------|-------|
| 37 | Terms use `**Term** - Definition.` format | | |
| 38 | Terms are alphabetized | | |
| 39 | Acronyms include expansion | | |

**Verify**:
```bash
# Check glossary uses correct format (should match, not `: ` definition lists)
grep -n '^\*\*' docs/glossary.md | head -10

# Check for wrong format (colon-space definition lists)
grep -n '^[A-Z].*: ' docs/glossary.md | head -10
```

---

## 5. Navigation Pattern

| # | Check | Pass | Notes |
|---|-------|------|-------|
| 40 | Root README links to `docs/README.md` (single entry point) | | |
| 41 | `docs/README.md` is a W3H hub with role-based navigation | | |
| 42 | `docs/README.md` links to all SDLC phase directories | | |
| 43 | Root README routes through hub (no deep links) | | |

**Verify**:
```bash
# Root README should have exactly one docs entry point
grep -c 'docs/README.md' README.md

# Root README should NOT deep-link into docs subdirectories
grep -E 'docs/[0-9]-' README.md | grep -v 'docs/README.md'
```

---

## 6. Cross-References

| # | Check | Pass | Notes |
|---|-------|------|-------|
| 44 | All markdown links resolve to existing files | | |
| 45 | All references use current paths | | |
| 46 | All references use `docs/` (plural) | | |
| 47 | All references use `guide/` (singular) | | |

**Verify**:
```bash
# Find stale doc/ references (should be docs/)
grep -rn '\bdoc/' docs/ --include="*.md" | grep -v 'docs/'

# Find stale guides/ references (should be guide/)
grep -rn 'guides/' docs/ --include="*.md"

# Find broken links (basic check for .md references)
grep -rohP '\[.*?\]\(((?!http)[^)]+\.md)\)' docs/ | sort -u | while read link; do
  target=$(echo "$link" | grep -oP '\(([^)]+)\)' | tr -d '()')
  [ ! -f "docs/$target" ] && echo "BROKEN: $link"
done
```

---

## 7. ADR Structure

| # | Check | Pass | Notes |
|---|-------|------|-------|
| 48 | ADR index exists at `docs/3-design/adr/README.md` | | |
| 49 | ADRs follow `NNN-title.md` naming (zero-padded) | | |
| 50 | ADR index lists all ADR files with status | | |

**Verify**:
```bash
# Check ADR index exists
ls docs/3-design/adr/README.md

# List ADRs and check naming
ls docs/3-design/adr/[0-9]*.md 2>/dev/null

# Check for non-conforming ADR names
find docs/3-design/adr/ -name "*.md" ! -name "README.md" | grep -v '^docs/3-design/adr/[0-9]'
```

---

## Quick Summary Table

Copy this table into your audit report:

| Category | Checks | Pass | Fail |
|----------|--------|------|------|
| Directory structure | 1-5 | | |
| Architecture compliance checklist | 6-8 | | |
| SDLC phase directories | 9-10 | | |
| Subdirectory naming | 11-13 | | |
| File naming | 14-23 | | |
| Required root files | 24-32 | | |
| Content patterns | 33-39 | | |
| Navigation pattern | 40-43 | | |
| Cross-references | 44-47 | | |
| ADR structure | 48-50 | | |
| **Total** | **50** | | |

---

## Rule Reference

| Rule | Source | Summary |
|------|--------|---------|
| Architecture compliance checklist required | FRAMEWORK.md directory structure + Phase 2 | `docs/3-design/compliance/compliance_checklist.md` must exist and reflect `architecture.md` |
| Module doc folders use `docs/` (plural) | FRAMEWORK.md directory structure + commit 59ab40d | Applies to root and all modules |
| Developer guides subfolder is `guide/` (singular) | FRAMEWORK.md L53 | `4-development/guide/` |
| UX/UI assets folder is `uxui/` | FRAMEWORK.md directory structure | `3-design/uxui/` |
| Git standard files are UPPERCASE | FRAMEWORK.md L84-99 | README, CONTRIBUTING, CHANGELOG, SECURITY, LICENSE |
| Project docs use lowercase-with-hyphens | FRAMEWORK.md L101-129 | All `.md` files inside `docs/` |
| All docs declare `**Audience**:` after H1 | FRAMEWORK.md W3H pattern | Target reader declaration |
| TLDR blockquote appears on 200+ line docs only | FRAMEWORK.md L465 | `> **TLDR**:` format |
| Glossary uses `**Term** - Definition.` format | FRAMEWORK.md L244-257 | Bold term, dash, definition |
| Root README routes through `docs/README.md` hub | FRAMEWORK.md L162-176 | Single entry point navigation |
| ADRs use `NNN-title.md` naming | FRAMEWORK.md L48-50 | Zero-padded number prefix |
| SDLC phases follow standard order | FRAMEWORK.md L16-29 | 0-ideation through 7-operation |

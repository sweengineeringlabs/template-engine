# Compliance Checklist

**Audience**: Developers, architects, code reviewers

Use this checklist during code review for any PR that touches the project's architectural boundaries. Every item must pass before merge. This checklist is **project-specific** -- it enforces the architecture defined in `docs/3-design/architecture.md`, not general documentation standards.

> For documentation compliance, see the framework-level [compliance-checklist.md](../../../../templates/compliance-checklist.md).

---

## How to Use

1. Derive checklist sections from your project's `docs/3-design/architecture.md`
2. Each architectural rule becomes a compliance section with checkable items
3. Run through this checklist on every PR that touches architectural boundaries
4. Automate what you can (grep patterns, build commands); manual-review the rest

---

## 1. Interface Compliance

Reference: `docs/3-design/architecture.md` -- "Program to an interface, not an implementation"

### 1.1 Dependency Direction

- [ ] No consumer code imports from `core/` directly (all access through SAF/public API)
- [ ] No upward dependencies (core does not depend on SAF, SPI does not depend on core)
- [ ] New dependencies follow the layer dependency rules documented in `architecture.md`

### 1.2 Interface Stability

- [ ] Public API changes are intentional and documented
- [ ] No implementation types leaked into public signatures
- [ ] Consumers depend on traits/interfaces, not concrete types, where the architecture requires it

**Verify**:
```bash
# Build catches dependency direction violations in multi-crate projects
{build_command}
```

---

## 2. {Architectural Concern 1}

Reference: `docs/3-design/{concern}.md`

> Replace this section with your project's first architectural concern.
> Examples: middleware rules, plugin boundaries, data flow constraints.

### 2.1 {Rule Category}

- [ ] {Check item derived from architecture doc}
- [ ] {Check item derived from architecture doc}
- [ ] {Check item derived from architecture doc}

### 2.2 {Rule Category}

- [ ] {Check item derived from architecture doc}
- [ ] {Check item derived from architecture doc}

**Verify**:
```bash
# {Description of what this checks}
{automated_check_command}
```

---

## 3. {Architectural Concern 2}

Reference: `docs/3-design/{concern}.md`

> Replace this section with your project's second architectural concern.
> Examples: security boundaries, API versioning rules, state management rules.

### 3.1 {Rule Category}

- [ ] {Check item derived from architecture doc}
- [ ] {Check item derived from architecture doc}

**Verify**:
```bash
# {Description of what this checks}
{automated_check_command}
```

---

## 4. Dependency Compliance

### 4.1 Version Alignment

- [ ] Core framework dependencies are version-aligned (no split versions of the same library)
- [ ] Workspace dependencies are defined in root config, not per-module
- [ ] No module pulls in a conflicting major version of a shared dependency

### 4.2 No Forbidden Patterns

- [ ] No patterns exist that the architecture explicitly bans (document and grep for them)

**Verify**:
```bash
# Search for forbidden patterns (customize per project)
# Example: grep -rn "impl Service" crates/ --include="*.rs"
{forbidden_pattern_grep}

# Build + test
{build_command}
{test_command}
```

---

## 5. Security Compliance

> Include if your architecture has security constraints. Remove if not applicable.

- [ ] No secrets in source code or configuration files committed to VCS
- [ ] Error responses do not leak internal details (no stack traces, no internal paths)
- [ ] Input validation occurs at system boundaries

---

## Quick Summary Table

Copy this table into your review comment:

| Category | Checks | Pass | Fail |
|----------|--------|------|------|
| Interface compliance | 1.1-1.2 | | |
| {Concern 1} | 2.1-2.2 | | |
| {Concern 2} | 3.1 | | |
| Dependency compliance | 4.1-4.2 | | |
| Security compliance | 5 | | |
| **Total** | | | |

---

## Automated Checks

```bash
# Build (catches dependency violations, type mismatches)
{build_command}

# Full test suite
{test_command}

# Search for forbidden patterns (customize these)
# grep -rn "{forbidden_pattern}" {source_dir}/ --include="*.{ext}"
```

---

## Customization Guide

This template provides the **structure**. The content must come from your project's architecture:

1. **Read** `docs/3-design/architecture.md` -- every rule there becomes a checklist item here
2. **Replace** placeholder sections (2, 3) with your actual architectural concerns
3. **Add sections** for each distinct area your architecture governs
4. **Add grep commands** for every pattern your architecture explicitly bans
5. **Remove** sections that don't apply (e.g. security section if architecture doesn't cover it)

The checklist is correct when: every enforceable rule in `architecture.md` has a corresponding checkbox here, and every checkbox has either an automated verification command or is marked for manual review.

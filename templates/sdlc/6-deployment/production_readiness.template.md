# {Project Name} — Production Readiness Review

**Audience**: Developers, architects, release managers

## TLDR

Production readiness checklist covering 14 areas across CI/CD, dependencies,
code quality, security, testing, observability, documentation, and release
automation. Each area is scored PASS / WARN / FAIL. All FAIL items must be
resolved before release; WARN items should have a tracking issue.

## Verdict: {READY | NOT READY}

| Area | Status | Notes |
|------|--------|-------|
| CI/CD Pipeline | {PASS/WARN/FAIL} | {notes} |
| Dependency Health | {PASS/WARN/FAIL} | {notes} |
| Static Analysis | {PASS/WARN/FAIL} | {notes} |
| Dependency Auditing | {PASS/WARN/FAIL} | {notes} |
| API Documentation | {PASS/WARN/FAIL} | {notes} |
| Runtime Safety | {PASS/WARN/FAIL} | {notes} |
| Package Metadata | {PASS/WARN/FAIL} | {notes} |
| README & Onboarding | {PASS/WARN/FAIL} | {notes} |
| Release Automation | {PASS/WARN/FAIL} | {notes} |
| Documentation Lint | {PASS/WARN/FAIL} | {notes} |
| Security | {PASS/WARN/FAIL} | {notes} |
| Test Coverage | {PASS/WARN/FAIL} | {notes} |
| Observability | {PASS/WARN/FAIL} | {notes} |
| Backwards Compatibility | {PASS/WARN/FAIL} | {notes} |

---

## 1. CI/CD Pipeline

**Criteria**: Automated pipeline runs on every push/PR.

- [ ] Test suite runs in CI (`cargo test` / `npm test` / equivalent)
- [ ] Linter runs in CI with warnings-as-errors
- [ ] Self-validation or compliance scan runs in CI (if applicable)
- [ ] Pipeline blocks merge on failure
- [ ] Matrix covers minimum supported version (MSRV / LTS)

**Status**: {PASS | WARN | FAIL}
**Evidence**: {link to workflow file or CI dashboard}

---

## 2. Dependency Health

**Criteria**: No deprecated, unmaintained, or yanked dependencies.

- [ ] No deprecated direct dependencies
- [ ] No unmaintained direct dependencies (>2 years without release)
- [ ] No yanked dependency versions in lockfile
- [ ] Unused dependencies removed

**Status**: {PASS | WARN | FAIL}
**Evidence**: {output of `cargo tree` / `npm audit` / equivalent}

---

## 3. Static Analysis

**Criteria**: Zero warnings from linter with strict settings.

- [ ] Linter passes with warnings-as-errors (`clippy -D warnings` / `eslint --max-warnings 0`)
- [ ] No suppressed warnings without justification (`#[allow(...)]` / `// eslint-disable`)
- [ ] Format check passes (`cargo fmt --check` / `prettier --check`)

**Status**: {PASS | WARN | FAIL}
**Evidence**: {linter output summary}

---

## 4. Dependency Auditing

**Criteria**: Known vulnerabilities are tracked and mitigated.

- [ ] Advisory database scan configured (`cargo-audit` / `cargo-deny` / `npm audit`)
- [ ] Scan runs in CI on every push
- [ ] License policy defined (allowed / denied licenses)
- [ ] No active advisories against direct dependencies

**Status**: {PASS | WARN | FAIL}
**Evidence**: {link to deny.toml / audit config, scan output}

---

## 5. API Documentation

**Criteria**: Public API is documented for library consumers.

- [ ] Crate-level / package-level documentation exists
- [ ] All public types, traits, and functions have doc comments
- [ ] Entry-point functions have usage examples
- [ ] Generated docs build without warnings (`cargo doc` / `typedoc`)

**Status**: {PASS | WARN | FAIL}
**Evidence**: {link to generated docs or doc build output}

---

## 6. Runtime Safety

**Criteria**: No avoidable runtime panics or unnecessary allocations in hot paths.

- [ ] No `unwrap()` / `expect()` on fallible operations in production code (or justified)
- [ ] Compile-once patterns used for regex / expensive initialization (`LazyLock` / `OnceLock` / equivalent)
- [ ] Error types are structured (no raw string errors in public API)
- [ ] Graceful degradation on malformed input

**Status**: {PASS | WARN | FAIL}
**Evidence**: {grep results for unwrap/expect in src/, regex initialization pattern}

---

## 7. Package Metadata

**Criteria**: Package is publishable with complete metadata.

- [ ] `repository` field set (link to source)
- [ ] `license` field set
- [ ] `authors` / `maintainers` field set
- [ ] `description` field set
- [ ] `keywords` / `categories` set (for registry discovery)
- [ ] Version follows semver

**Status**: {PASS | WARN | FAIL}
**Evidence**: {link to Cargo.toml / package.json metadata section}

---

## 8. README & Onboarding

**Criteria**: New users can install, run, and understand the project in < 5 minutes.

- [ ] README exists and is concise (< 100 lines for root, links to detailed docs)
- [ ] Quick start / installation instructions present
- [ ] Usage examples cover primary commands or API surface
- [ ] CI status badge displayed
- [ ] Link to CONTRIBUTING.md
- [ ] Exit codes or error behavior documented (for CLI tools)

**Status**: {PASS | WARN | FAIL}
**Evidence**: {link to README}

---

## 9. Release Automation

**Criteria**: Releases are reproducible and automated.

- [ ] Version bumps follow a defined process (manual semver or `release-plz` / `semantic-release`)
- [ ] Tag-triggered workflow builds release artifacts
- [ ] CHANGELOG is maintained (manual or auto-generated)
- [ ] Release artifacts are attached to GitHub release (binaries, checksums)
- [ ] Pre-release validation gate (all CI checks pass before publish)

**Status**: {PASS | WARN | FAIL}
**Evidence**: {link to release workflow, latest release page}

---

## 10. Documentation Lint

**Criteria**: Documentation coverage is enforced by tooling.

- [ ] Missing-docs lint enabled (`#![warn(missing_docs)]` / equivalent)
- [ ] New public API additions require documentation (enforced by CI)
- [ ] Doc tests compile and pass (if applicable)

**Status**: {PASS | WARN | FAIL}
**Evidence**: {compiler output showing zero missing-docs warnings}

---

## 11. Security

**Criteria**: Application defends against common attack vectors and manages secrets safely.

- [ ] No hardcoded secrets, tokens, or credentials in source code
- [ ] Secrets loaded from environment variables or a secrets manager
- [ ] `.env` and credential files listed in `.gitignore`
- [ ] User input validated and sanitized at system boundaries
- [ ] No known OWASP Top 10 vulnerabilities (injection, XSS, SSRF, etc.)
- [ ] Dependencies signed or checksummed (supply chain integrity)
- [ ] SECURITY.md documents vulnerability reporting process

**Status**: {PASS | WARN | FAIL}
**Evidence**: {grep for hardcoded secrets, input validation audit, SECURITY.md link}

---

## 12. Test Coverage

**Criteria**: Test suite provides confidence against regressions.

- [ ] Unit tests cover core logic and edge cases
- [ ] Integration tests verify component interactions
- [ ] E2E tests cover primary user workflows (if applicable)
- [ ] Coverage metric tracked (target: {X}% line coverage)
- [ ] No critical paths without test coverage
- [ ] Tests are deterministic (no flaky tests in CI history)
- [ ] Property-based or fuzz tests for parsing / serialization (if applicable)

**Status**: {PASS | WARN | FAIL}
**Evidence**: {test count, coverage report, CI test history}

---

## 13. Observability

**Criteria**: Production behavior is visible and diagnosable.

- [ ] Structured logging with consistent format (JSON / key-value)
- [ ] Log levels used correctly (error for failures, warn for degradation, info for operations, debug for troubleshooting)
- [ ] Errors include context (file path, input value, operation attempted)
- [ ] Metrics exported for key operations (if service: request rate, latency, error rate)
- [ ] Health check endpoint available (if service)
- [ ] Tracing or correlation IDs for request tracking (if service)

**Status**: {PASS | WARN | FAIL}
**Evidence**: {sample log output, metrics endpoint, health check URL}

---

## 14. Backwards Compatibility

**Criteria**: Users can upgrade without unexpected breakage.

- [ ] Public API follows semver (breaking changes = major bump)
- [ ] Deprecated items marked with `#[deprecated]` / `@deprecated` before removal
- [ ] Migration guide provided for breaking changes
- [ ] CLI flag changes are backwards-compatible or documented
- [ ] Config file format changes have fallback parsing for previous format
- [ ] CHANGELOG documents all breaking changes prominently

**Status**: {PASS | WARN | FAIL}
**Evidence**: {semver policy, deprecation annotations, CHANGELOG breaking section}

---

## Scoring

| Score | Meaning | Action |
|-------|---------|--------|
| **PASS** | Meets criteria fully | None |
| **WARN** | Partially met or minor gaps | Create tracking issue, non-blocking |
| **FAIL** | Not met, significant risk | Must resolve before release |

**Release gate**: 0 FAIL items. WARN items tracked in backlog.

## Sign-Off

| Role | Name | Date | Verdict |
|------|------|------|---------|
| {Developer} | {name} | {date} | {READY/NOT READY} |
| {Reviewer} | {name} | {date} | {READY/NOT READY} |

## Related Documents

- **Architecture**: [architecture.md](../3-design/architecture.md)
- **Deployment**: [deploy.md](deploy.md)
- **Backlog**: [backlog.md](../2-planning/backlog.md)
- **CI/CD**: [ci_cd.md](ci_cd.md)

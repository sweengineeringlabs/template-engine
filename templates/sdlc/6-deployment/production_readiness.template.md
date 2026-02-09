# {Project Name} — Production Readiness Review

**Audience**: Developers, architects, release managers

## TLDR

Production readiness checklist covering 14 areas across CI/CD, dependencies,
code quality, security, testing, observability, documentation, and release
automation. Each area is scored PASS / WARN / FAIL. All FAIL items must be
resolved before release; WARN items should have a tracking issue.

## Standards

This template aligns with three ISO/IEC standards:

| Standard | Scope | Template areas |
|----------|-------|----------------|
| **ISO/IEC 25010:2023** | Product quality model (SQuaRE) | #3 Static Analysis, #5 API Docs, #6 Runtime Safety, #8 README, #10 Doc Lint, #11 Security, #12 Test Coverage, #13 Observability, #14 Backwards Compatibility |
| **ISO/IEC/IEEE 12207:2017** | Software lifecycle processes | #1 CI/CD, #2 Dependency Health, #4 Auditing, #7 Metadata, #9 Release Automation |
| **ISO/IEC 25040:2024** | Quality evaluation process | Scoring methodology, evidence requirements, sign-off process |

### ISO/IEC 25010:2023 Quality Characteristics Mapping

| 25010 Characteristic | Sub-characteristics | Template Area |
|----------------------|--------------------|----|
| Functional suitability | Completeness, correctness, appropriateness | #12 Test Coverage |
| Performance efficiency | Time behaviour, resource utilisation, capacity | #6 Runtime Safety |
| Compatibility | Co-existence, interoperability | #14 Backwards Compatibility |
| Usability | Learnability, operability, user error protection | #8 README & Onboarding |
| Reliability | Availability, fault tolerance, recoverability | #12 Test Coverage, #13 Observability |
| Security | Confidentiality, integrity, non-repudiation, accountability, authenticity | #11 Security, #4 Dependency Auditing |
| Maintainability | Modularity, reusability, analysability, modifiability, testability | #3 Static Analysis, #5 API Docs, #10 Doc Lint |
| Portability | Adaptability, installability, replaceability | #1 CI/CD Pipeline, #7 Package Metadata |
| Safety | Operational constraint satisfaction, risk identification, fail safe | #6 Runtime Safety |

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

> **Standard**: ISO/IEC/IEEE 12207:2017 §6.3.1 (Infrastructure Management), ISO/IEC 25010:2023 Portability

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

> **Standard**: ISO/IEC/IEEE 12207:2017 §6.3.2 (Configuration Management)

**Criteria**: No deprecated, unmaintained, or yanked dependencies.

- [ ] No deprecated direct dependencies
- [ ] No unmaintained direct dependencies (>2 years without release)
- [ ] No yanked dependency versions in lockfile
- [ ] Unused dependencies removed

**Status**: {PASS | WARN | FAIL}
**Evidence**: {output of `cargo tree` / `npm audit` / equivalent}

---

## 3. Static Analysis

> **Standard**: ISO/IEC 25010:2023 Maintainability (analysability, modifiability)

**Criteria**: Zero warnings from linter with strict settings.

- [ ] Linter passes with warnings-as-errors (`clippy -D warnings` / `eslint --max-warnings 0`)
- [ ] No suppressed warnings without justification (`#[allow(...)]` / `// eslint-disable`)
- [ ] Format check passes (`cargo fmt --check` / `prettier --check`)

**Status**: {PASS | WARN | FAIL}
**Evidence**: {linter output summary}

---

## 4. Dependency Auditing

> **Standard**: ISO/IEC 25010:2023 Security (integrity, authenticity), ISO/IEC/IEEE 12207:2017 §6.3.5 (Quality Assurance)

**Criteria**: Known vulnerabilities are tracked and mitigated.

- [ ] Advisory database scan configured (`cargo-audit` / `cargo-deny` / `npm audit`)
- [ ] Scan runs in CI on every push
- [ ] License policy defined (allowed / denied licenses)
- [ ] No active advisories against direct dependencies

**Status**: {PASS | WARN | FAIL}
**Evidence**: {link to deny.toml / audit config, scan output}

---

## 5. API Documentation

> **Standard**: ISO/IEC 25010:2023 Maintainability (analysability), Usability (learnability)

**Criteria**: Public API is documented for library consumers.

- [ ] Crate-level / package-level documentation exists
- [ ] All public types, traits, and functions have doc comments
- [ ] Entry-point functions have usage examples
- [ ] Generated docs build without warnings (`cargo doc` / `typedoc`)

**Status**: {PASS | WARN | FAIL}
**Evidence**: {link to generated docs or doc build output}

---

## 6. Runtime Safety

> **Standard**: ISO/IEC 25010:2023 Performance Efficiency (time behaviour, resource utilisation), Safety (fail safe)

**Criteria**: No avoidable runtime panics or unnecessary allocations in hot paths.

- [ ] No `unwrap()` / `expect()` on fallible operations in production code (or justified)
- [ ] Compile-once patterns used for regex / expensive initialization (`LazyLock` / `OnceLock` / equivalent)
- [ ] Error types are structured (no raw string errors in public API)
- [ ] Graceful degradation on malformed input

**Status**: {PASS | WARN | FAIL}
**Evidence**: {grep results for unwrap/expect in src/, regex initialization pattern}

---

## 7. Package Metadata

> **Standard**: ISO/IEC/IEEE 12207:2017 §6.3.2 (Configuration Management), ISO/IEC 25010:2023 Portability (installability)

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

> **Standard**: ISO/IEC 25010:2023 Usability (learnability, operability, user error protection)

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

> **Standard**: ISO/IEC/IEEE 12207:2017 §6.3.4 (Release Management)

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

> **Standard**: ISO/IEC 25010:2023 Maintainability (analysability, testability)

**Criteria**: Documentation coverage is enforced by tooling.

- [ ] Missing-docs lint enabled (`#![warn(missing_docs)]` / equivalent)
- [ ] New public API additions require documentation (enforced by CI)
- [ ] Doc tests compile and pass (if applicable)

**Status**: {PASS | WARN | FAIL}
**Evidence**: {compiler output showing zero missing-docs warnings}

---

## 11. Security

> **Standard**: ISO/IEC 25010:2023 Security (confidentiality, integrity, non-repudiation, accountability, authenticity)

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

> **Standard**: ISO/IEC 25010:2023 Functional Suitability (completeness, correctness), Reliability (fault tolerance)

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

> **Standard**: ISO/IEC 25010:2023 Reliability (availability, recoverability), Maintainability (analysability)

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

> **Standard**: ISO/IEC 25010:2023 Compatibility (co-existence, interoperability), Portability (replaceability)

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

> **Standard**: ISO/IEC 25040:2024 — quality evaluation process (establish requirements, specify evaluation, design evaluation, execute evaluation, conclude evaluation)

| Score | Meaning | Action | 25040 Phase |
|-------|---------|--------|-------------|
| **PASS** | Meets criteria fully | None | Conclude: satisfactory |
| **WARN** | Partially met or minor gaps | Create tracking issue, non-blocking | Conclude: conditionally satisfactory |
| **FAIL** | Not met, significant risk | Must resolve before release | Execute: re-evaluate after remediation |

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

# {Project Name} Testing Strategy

## Version

| Field        | Value                     |
|--------------|---------------------------|
| Version      | {0.1.0}                   |
| Status       | {Draft | Approved | Superseded} |
| Last Updated | {YYYY-MM-DD}              |
| Owner        | {owner}                   |

## Overview

{1-2 paragraph description of the testing philosophy, goals, and how testing
integrates into the development workflow.}

## Test Pyramid

```
        /  E2E  \          ~{10}% of total tests
       /----------\
      / Integration \      ~{30}% of total tests
     /----------------\
    /      Unit        \   ~{60}% of total tests
   /____________________\
```

- **Unit**: isolated function and module tests, no I/O
- **Integration**: cross-module and crate-boundary tests, may use fixtures
- **E2E**: full-system scenarios exercised through public interfaces

## Test Categories

| Category | Scope | Tools | Location |
|----------|-------|-------|----------|
| Unit | Single function / module | {test framework} | `crates/*/src/**/*_test.rs` |
| Integration | Cross-crate boundaries | {test framework} | `crates/*/tests/` |
| E2E | Full pipeline | {e2e framework} | `tests/e2e/` |
| Snapshot | Output stability | {snapshot crate} | `crates/*/src/**/*.snap` |
| Fuzz | Input robustness | {fuzz tool} | `fuzz/` |

## Coverage Targets

| Component | Crate | Line Target | Branch Target |
|-----------|-------|-------------|---------------|
| {component-1} | `{crate-name}` | {80}% | {70}% |
| {component-2} | `{crate-name}` | {80}% | {70}% |
| {component-3} | `{crate-name}` | {80}% | {70}% |
| **Overall** | workspace | **{80}%** | **{70}%** |

## CI Pipeline

| Stage | Trigger | Steps | Timeout |
|-------|---------|-------|---------|
| Lint | Every push | `{lint-command}` | {5m} |
| Unit + Integration | Every push | `{test-command}` | {10m} |
| E2E | PR to `main` | `{e2e-command}` | {15m} |
| Coverage | PR to `main` | `{coverage-command}`, upload report | {10m} |
| Fuzz | Nightly / manual | `{fuzz-command}` | {30m} |

## Test Environment

| Environment | Purpose | Data Source | Reset Cadence |
|-------------|---------|-------------|---------------|
| Local | Developer iteration | fixtures / mocks | per run |
| CI | Automated validation | fixtures / snapshots | per pipeline |
| Staging | Pre-release verification | {sanitized prod data | synthetic} | {weekly} |

## Test Naming Conventions

- Unit tests: `test_{function_name}_{scenario}_{expected}`
- Integration tests: `test_{feature}_{interaction}_{expected}`
- E2E tests: `e2e_{workflow}_{expected}`

## Per-Component Test Plans

| Component | Crate | Test Plan |
|-----------|-------|-----------|
| {component-1} | `{crate-name}` | [{crate-name}.test](../../{crate-name}/docs/5-testing/{name}.test) |
| {component-2} | `{crate-name}` | [{crate-name}.test](../../{crate-name}/docs/5-testing/{name}.test) |
| {component-3} | `{crate-name}` | [{crate-name}.test](../../{crate-name}/docs/5-testing/{name}.test) |

## Related Documents

### Requirements
- [Business Requirements](../1-requirements/brd.spec)

### Design
- [System Architecture](../3-design/architecture.arch)

### Development
- [Developer Guide](../4-development/developer_guide.md)

### Deployment
- [CI/CD Pipeline](../6-deployment/ci_cd.md)

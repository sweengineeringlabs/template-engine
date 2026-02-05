# {Project Name} CI/CD Pipeline

## Version

| Field        | Value                     |
|--------------|---------------------------|
| Version      | {0.1.0}                   |
| Status       | {Draft | Approved | Superseded} |
| Last Updated | {YYYY-MM-DD}              |
| Owner        | {owner}                   |

## Overview

{1-2 paragraph description of the CI/CD philosophy, toolchain, and how
the pipeline connects to the development and release workflow.}

## Build Pipeline

| Stage | Runner | Steps | Artifacts |
|-------|--------|-------|-----------|
| Checkout | {CI platform} | clone, restore cache | - |
| Build | {CI platform} | `{build-command}` | `target/release/{binary}` |
| Lint | {CI platform} | `{lint-command}` | lint report |
| Audit | {CI platform} | `{audit-command}` | advisory report |

## Test Pipeline

| Stage | Trigger | Steps | Pass Criteria |
|-------|---------|-------|---------------|
| Unit + Integration | Every push | `{test-command}` | all green |
| E2E | PR to `main` | `{e2e-command}` | all green |
| Coverage Gate | PR to `main` | `{coverage-command}` | >= {80}% lines |
| Fuzz (optional) | Nightly / manual | `{fuzz-command}` | no crashes in {duration} |

## Release Process

- [ ] All CI checks green on `main`
- [ ] Version bumped in `{manifest-file}`
- [ ] Changelog updated in `{changelog-file}`
- [ ] Release tag created: `v{X.Y.Z}`
- [ ] Binaries built for all targets
- [ ] Packages published to {registry}
- [ ] Release notes drafted on {platform}

## Package Distribution

| Target | Format | Channel | Command |
|--------|--------|---------|---------|
| {x86_64-linux} | {tar.gz} | {GitHub Releases} | `{install-command}` |
| {x86_64-macos} | {tar.gz} | {GitHub Releases} | `{install-command}` |
| {x86_64-windows} | {zip} | {GitHub Releases} | `{install-command}` |
| {crates.io} | {crate} | {crates.io} | `cargo install {crate-name}` |
| {npm} | {npm package} | {npmjs.com} | `npm install {package-name}` |

## Environment Promotion

| Environment | Branch / Tag | Auto-Deploy | Approval Required |
|-------------|-------------|-------------|-------------------|
| Development | `main` | {yes} | no |
| Staging | `release/*` | {yes} | no |
| Production | `v*` tag | {no} | {yes - {approver role}} |

## Rollback Procedure

1. Identify the failing release version: `v{X.Y.Z}`
2. Revert to last known good tag: `v{X.Y.Z-1}`
3. Run `{rollback-command}`
4. Verify health checks pass (see [Ops Manual](../7-operation/ops_manual.md))
5. Open post-incident issue to investigate root cause

## Per-Component Deployment

| Component | Crate | Deployment Guide |
|-----------|-------|------------------|
| {component-1} | `{crate-name}` | [{crate-name}.deploy](../../{crate-name}/docs/6-deployment/{name}.deploy) |
| {component-2} | `{crate-name}` | [{crate-name}.deploy](../../{crate-name}/docs/6-deployment/{name}.deploy) |
| {component-3} | `{crate-name}` | [{crate-name}.deploy](../../{crate-name}/docs/6-deployment/{name}.deploy) |

## Related Documents

### Design
- [System Architecture](../3-design/architecture.arch)

### Development
- [Developer Guide](../4-development/developer_guide.md)

### Testing
- [Testing Strategy](../5-testing/testing_strategy.md)

### Operations
- [Ops Manual](../7-operation/ops_manual.md)

# {Project Name} Developer Guide

## Overview

{1-2 paragraph description of the project from a developer perspective.
Include the tech stack summary and link to the architecture document.}

## Prerequisites

| Tool | Minimum Version | Installation |
|------|----------------|--------------|
| {Rust} | {1.xx+} | [rustup.rs](https://rustup.rs) |
| {Node.js} | {vXX+} | [nodejs.org](https://nodejs.org) |
| {tool} | {version} | {link} |
| {tool} | {version} | {link} |

## Getting Started

### Clone

```sh
git clone {repo-url}
cd {repo-name}
```

### Build

```sh
{build-command}
```

### Test

```sh
{test-command}
```

### Run

```sh
{run-command}
```

## Repository Structure

```
{repo-name}/
  crates/
    {crate-1}/          # {description}
    {crate-2}/          # {description}
    {crate-3}/          # {description}
  docs/
    sdlc/               # SDLC documentation tree
  tests/
    e2e/                # End-to-end tests
  Cargo.toml            # Workspace manifest
```

## Development Workflow

1. Create a feature branch from `main`: `git checkout -b feat/{short-name}`
2. Implement changes with tests
3. Run `{lint-command}` and `{test-command}` locally
4. Open a pull request against `main`
5. Address review feedback, then merge

## Coding Standards

- {formatting tool and config, e.g. rustfmt with project .rustfmt.toml}
- {linting tool, e.g. clippy with deny warnings}
- {documentation expectations, e.g. public API doc-comments required}
- {commit message convention, e.g. Conventional Commits}
- {error handling convention}

## Per-Component Setup Guides

| Component | Crate | Setup Guide |
|-----------|-------|-------------|
| {component-1} | `{crate-name}` | [{crate-name}.setup](../../{crate-name}/docs/4-development/{name}.setup) |
| {component-2} | `{crate-name}` | [{crate-name}.setup](../../{crate-name}/docs/4-development/{name}.setup) |
| {component-3} | `{crate-name}` | [{crate-name}.setup](../../{crate-name}/docs/4-development/{name}.setup) |

## Related Documents

### Design
- [System Architecture](../3-design/architecture.arch)

### Testing
- [Testing Strategy](../5-testing/testing_strategy.md)

### Deployment
- [CI/CD Pipeline](../6-deployment/ci_cd.md)

### Operations
- [Ops Manual](../7-operation/ops_manual.md)

# {Module Name} Developer Guide

**FR:** [FR-{###}](../../../../docs/1-requirements/FR-{###}-{name}.md)

## Overview

Day-to-day development guide for working on {module-name}.

## Module Structure

```
{module-name}/
├── {module}-common/       # Shared types, errors
│   └── src/
├── {module}-spi/          # Extension traits
│   └── src/
├── {module}-api/          # Public traits
│   └── src/
├── {module}-core/         # Implementation
│   ├── src/
│   └── tests/
└── {module}/              # Facade, prelude
    └── src/
```

## Development Workflow

1. **Branch** from `main` using `feature/{short-description}`
2. **Implement** changes in the appropriate layer (see [Architecture](../3-design/architecture.md))
3. **Test** with `cargo test -p {module-name}`
4. **Lint** with `cargo clippy -p {module-name}`
5. **Submit** a pull request targeting `main`

## Key Conventions

### Code Style

- Follow Rust 2021 edition idioms
- Use `thiserror` for error types in `{module}-common`
- Expose public API through the facade prelude only
- Keep business logic in `{module}-core`; no logic in `{module}-api`

### Naming

| Item | Convention | Example |
|------|-----------|---------|
| Structs | PascalCase | `{Module}Config` |
| Traits | PascalCase | `{Module}Provider` |
| Functions | snake_case | `process_{entity}` |
| Constants | SCREAMING_SNAKE | `MAX_{ENTITY}_COUNT` |

### Error Handling

- Define error variants in `{module}-common/src/error.rs`
- Return `Result<T, {Module}Error>` from all fallible functions
- Use `?` propagation; avoid `.unwrap()` outside tests

## Common Tasks

### Adding a New Public Method

1. Declare the trait method in `{module}-api`
2. Implement in `{module}-core`
3. Re-export through the facade prelude
4. Add unit tests inline and integration tests in `{module}-core/tests/`

### Adding a New SPI Extension Point

1. Define the provider trait in `{module}-spi`
2. Provide a default implementation in `{module}-core` if applicable
3. Document the contract in the trait doc-comment

## See Also

- [Setup Guide](setup_guide.md)
- [Architecture](../3-design/architecture.md)
- [Testing Strategy](../5-testing/testing_strategy.md)
- [Overview](../README.md)

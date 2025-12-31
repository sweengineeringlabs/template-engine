# SEA Module Workflow

> **TLDR:** 5-layer module structure (common, spi, api, core, facade). Create layers, extract types, define traits, implement, add docs. See checklist at end.

## Table of Contents
- [Module Structure](#module-structure)
- [Layer Dependencies](#layer-dependencies)
- [Migration Steps](#migration-steps)
- [Compliance Checklist](#compliance-checklist)
- [Anti-Patterns](#anti-patterns)
- [Testing Strategy](#testing-strategy)

Detailed workflow for creating or migrating modules to SEA (Stratified Encapsulation Architecture) compliance.

## Module Structure

```
crates/{module-name}/
├── {module}-common/     # Shared types (DTOs, errors, constants)
├── {module}-spi/        # Service Provider Interface (extension traits)
├── {module}-api/        # Public API (consumer traits, registries)
├── {module}-core/       # Implementation (business logic)
├── {module}/            # Facade (re-exports, entry point)
├── README.md            # Lean quick reference
└── doc/
    ├── overview.md      # WHAT/HOW/WHY (required)
    └── 5-testing/       # Optional SDLC-specific docs
        └── strategy.md
```

## Layer Dependencies

| Layer | Purpose | Depends On |
|-------|---------|------------|
| `common` | Shared types, DTOs, error types | None |
| `spi` | Extension point traits for plugins | `common` |
| `api` | Public interface traits | `common`, `spi` |
| `core` | Concrete implementations | `common`, `spi`, `api` |
| `facade` | Re-exports, entry point | All layers |

## Migration Steps

### Step 1: Create Structure

```bash
cd crates
mkdir -p {module}/{module}-common/src
mkdir -p {module}/{module}-spi/src
mkdir -p {module}/{module}-api/src
mkdir -p {module}/{module}-core/src
mkdir -p {module}/{module}/src
mkdir -p {module}/doc
```

### Step 2: Extract to `{module}-common`

- Move DTOs, error types, constants
- No business logic
- Minimal dependencies (serde, thiserror)

### Step 3: Define `{module}-spi`

- Create traits for pluggable components
- Example: `trait LspProvider { ... }`

### Step 4: Define `{module}-api`

- Public traits consumers will use
- Registry interfaces for provider registration

### Step 5: Implement `{module}-core`

- Move all business logic
- Implement traits from `spi` and `api`
- Unit tests (with mocks) inline
- Integration tests in `tests/`

### Step 6: Create `{module}` Facade

- Re-export public types from all layers
- Convenience constructors
- Entry point for consumers

### Step 7: Update Workspace

```toml
# In workspace Cargo.toml
members = [
    "crates/{module}/{module}-common",
    "crates/{module}/{module}-spi",
    "crates/{module}/{module}-api",
    "crates/{module}/{module}-core",
    "crates/{module}/{module}",
]
```

### Step 8: Add Documentation

See: [Documentation Standard](./documentation-standard.md) for complete specification.

Required:
- `{module}/README.md` - lean quick reference (usage, API summary)
- `{module}/doc/overview.md` - WHAT/HOW/WHY sections

Optional:
- `{module}/doc/3-design/architecture.md` - detailed diagrams
- `{module}/doc/5-testing/strategy.md` - if extending base strategy

## Compliance Checklist

- [ ] All 5 layers exist (`common`, `spi`, `api`, `core`, facade)
- [ ] Layer dependencies flow correctly (no circular deps)
- [ ] No project-level `common/` or `util/` imports
- [ ] Unit tests use mocks
- [ ] Integration tests use real components
- [ ] `{module}/README.md` - lean quick reference (TLDR + TOC)
- [ ] `{module}/doc/overview.md` - WHAT/HOW/WHY sections
- [ ] Main `README.md` updated with module link (if SEA module)

## Anti-Patterns

Prohibited in swe-studio:

1. **No project-level `common/` or `util/` packages** - Use `{module}-common/`
2. **No cross-module shared utilities** - Duplication over coupling
3. **No mocking internals in integration tests** - Real components only

See:
- [No Common Crates](../3-design/no-common-packages.md)
- [No Util Modules](../3-design/no-util-classes.md)

## Testing Strategy

| Test Type | Mocking | Location |
|-----------|---------|----------|
| Unit | Mock all dependencies | `{module}-core/src/` (inline) |
| Integration | Real components only | `{module}-core/tests/` |
| E2E | Fixtures + real systems | `crates/{module}/tests/` |

See: [Base Testing Strategy](../5-testing/testing-strategy.md)

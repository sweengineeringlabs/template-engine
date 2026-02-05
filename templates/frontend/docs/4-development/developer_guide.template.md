# {Module Name} Developer Guide

**FR:** [FR-{###}](../../../../docs/1-requirements/FR-{###}-{name}.md)

## Overview

Day-to-day development guide for working on {module-name}.

## Module Structure

```
{module-name}/
├── src/
│   ├── components/        # React components
│   │   └── {Feature}/
│   ├── hooks/             # Custom hooks
│   ├── stores/            # Zustand stores
│   ├── utils/             # Utility functions
│   └── types/             # TypeScript type definitions
├── tests/
│   ├── unit/              # Unit and integration tests
│   └── e2e/               # End-to-end tests
└── public/                # Static assets
```

## Development Workflow

1. **Branch** from `main` using `feature/{short-description}`
2. **Implement** changes following the component/store architecture
3. **Test** with `bun test`
4. **Lint** with `bun run lint`
5. **Submit** a pull request targeting `main`

## Key Conventions

### Code Style

- Use functional components with hooks exclusively
- Co-locate component styles using CSS modules or Tailwind classes
- Keep state management in Zustand stores; avoid prop drilling beyond two levels
- Use TypeScript strict mode; avoid `any` type

### Naming

| Item | Convention | Example |
|------|-----------|---------|
| Components | PascalCase | `{ComponentName}.tsx` |
| Hooks | camelCase with `use` prefix | `use{Feature}.ts` |
| Stores | camelCase with `Store` suffix | `{feature}Store.ts` |
| Utilities | camelCase | `format{Entity}.ts` |
| Types | PascalCase | `{TypeName}.ts` |

### File Organization

- One component per file
- Test files adjacent in `__tests__/` directories
- Shared types in `src/types/`
- Re-export public API from barrel `index.ts` files

## Common Tasks

### Adding a New Component

1. Create `src/components/{Feature}/{ComponentName}.tsx`
2. Define props interface: `interface {ComponentName}Props { ... }`
3. Add unit test in `src/components/{Feature}/__tests__/{ComponentName}.test.tsx`
4. Export from the feature barrel file

### Adding a New Store

1. Create `src/stores/{feature}Store.ts`
2. Define the state interface and actions
3. Add unit test in `src/stores/__tests__/{feature}Store.test.ts`
4. Use in components via `use{Feature}Store()`

## See Also

- [Setup Guide](setup_guide.md)
- [Architecture](../3-design/architecture.md)
- [Testing Strategy](../5-testing/testing_strategy.md)
- [Overview](../README.md)

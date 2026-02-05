# {Module Name} Setup Guide

**FR:** [FR-{###}](../../../../docs/1-requirements/FR-{###}-{name}.md)

## Prerequisites

| Requirement | Minimum Version | Check Command |
|-------------|-----------------|---------------|
| Node.js | {node_version} | `node --version` |
| Bun | {bun_version} | `bun --version` |
| {dependency} | {version} | `{check_command}` |

## Repository Setup

### Clone and Navigate

```bash
git clone {repository_url}
cd {repository_root}/{module-name}
```

### Install Dependencies

```bash
# Install all dependencies
bun install
```

## Build

```bash
# Development build
bun run dev

# Production build
bun run build

# Preview production build
bun run preview
```

## Test

```bash
# Run all unit tests
bun test

# Run specific test file
bun test src/stores/__tests__/{feature}Store.test.ts

# Run E2E tests
bun run test:e2e

# Run specific E2E test
bun run test:e2e tests/e2e/{feature}/

# Watch mode
bun test --watch
```

## Lint and Format

```bash
# Check lint
bun run lint

# Fix lint issues
bun run lint:fix

# Check formatting
bun run format:check

# Apply formatting
bun run format
```

## Environment Variables

| Variable | Purpose | Default |
|----------|---------|---------|
| `VITE_{MODULE}_API_URL` | API base URL | `http://localhost:{port}` |
| `VITE_{MODULE}_DEBUG` | Enable debug mode | `false` |
| `{VARIABLE}` | {description} | `{default}` |

Create a `.env.local` file for local overrides (not committed to version control).

## IDE Setup

### VS Code

Recommended extensions:
- `dbaeumer.vscode-eslint` - ESLint integration
- `esbenp.prettier-vscode` - Code formatting
- `bradlc.vscode-tailwindcss` - Tailwind CSS IntelliSense

### WebStorm

- Enable ESLint integration under Settings > Languages > JavaScript > ESLint
- Configure Prettier as default formatter

## Troubleshooting

| Issue | Solution |
|-------|----------|
| `bun install` fails | Delete `node_modules/` and `bun.lockb`, then retry |
| Dev server port conflict | Set `VITE_PORT={port}` in `.env.local` |
| TypeScript errors after pull | Run `bun install` to sync dependencies |

## See Also

- [Developer Guide](developer_guide.md)
- [Configuration](../6-deployment/configuration.md)
- [Overview](../README.md)

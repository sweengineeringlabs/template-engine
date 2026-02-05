# {Module Name} Setup Guide

**FR:** [FR-{###}](../../../../docs/1-requirements/FR-{###}-{name}.md)

## Prerequisites

| Requirement | Minimum Version | Check Command |
|-------------|-----------------|---------------|
| Rust toolchain | {rust_version} | `rustc --version` |
| Cargo | {cargo_version} | `cargo --version` |
| {dependency} | {version} | `{check_command}` |

## Repository Setup

### Clone and Navigate

```bash
git clone {repository_url}
cd {repository_root}/{module-name}
```

### Install Dependencies

```bash
# Install Rust toolchain (if needed)
rustup install {rust_version}
rustup default {rust_version}

# Fetch crate dependencies
cargo fetch
```

## Build

```bash
# Debug build
cargo build -p {module-name}

# Release build
cargo build -p {module-name} --release

# Build all sub-crates individually
cargo build -p {module}-common
cargo build -p {module}-spi
cargo build -p {module}-api
cargo build -p {module}-core
```

## Test

```bash
# Run all tests
cargo test -p {module-name}

# Unit tests only
cargo test -p {module-name}-core --lib

# Integration tests only
cargo test -p {module-name}-core --test integration

# With output
cargo test -p {module-name} -- --nocapture
```

## Lint and Format

```bash
# Check formatting
cargo fmt -p {module-name} -- --check

# Apply formatting
cargo fmt -p {module-name}

# Lint
cargo clippy -p {module-name} -- -D warnings
```

## Environment Variables

| Variable | Purpose | Default |
|----------|---------|---------|
| `{MODULE}_LOG_LEVEL` | Logging verbosity | `info` |
| `{MODULE}_CONFIG_PATH` | Path to config file | `config.toml` |
| `{MODULE}_{OPTION}` | {description} | `{default}` |

## IDE Setup

### VS Code

Recommended extensions:
- `rust-analyzer` - Language server
- `Even Better TOML` - Cargo.toml support
- `CodeLLDB` - Debugging

### IntelliJ / CLion

- Install the Rust plugin
- Set the toolchain to `{rust_version}`
- Configure Cargo to use workspace root

## Troubleshooting

| Issue | Solution |
|-------|----------|
| `cargo build` fails with missing dependency | Run `cargo fetch` then retry |
| Tests hang or timeout | Check for blocking I/O in async tests |
| Clippy warnings on CI but not locally | Ensure you use the same Rust version as CI |

## See Also

- [Developer Guide](developer_guide.md)
- [Configuration](../6-deployment/configuration.md)
- [Overview](../README.md)

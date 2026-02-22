# {Module Name} Filesystem Paths

> **TLDR:** XDG Base Directory compliant file storage locations for configuration, data, state, and cache.

**Audience**: Developers, DevOps, Users

**WHAT**: Standardized filesystem paths for application files
**WHY**: Cross-platform compatibility, user expectations, avoid polluting home directory
**HOW**: Follow XDG Base Directory Specification with graceful fallbacks

---

## Table of Contents

- [XDG Base Directory Specification](#xdg-base-directory-specification)
- [Path Summary](#path-summary)
- [Implementation](#implementation)
- [Migration](#migration)
- [Platform Notes](#platform-notes)

---

## XDG Base Directory Specification

The [XDG Base Directory Specification](https://specifications.freedesktop.org/basedir-spec/basedir-spec-latest.html) is a freedesktop.org standard defining where applications should store files on Linux/Unix systems.

| Variable | Default | Purpose | Example Files |
|----------|---------|---------|---------------|
| `XDG_CONFIG_HOME` | `~/.config` | User configuration | `config.toml`, `settings.yaml` |
| `XDG_DATA_HOME` | `~/.local/share` | User data | databases, workspace files |
| `XDG_STATE_HOME` | `~/.local/state` | User state | logs, history, undo files |
| `XDG_CACHE_HOME` | `~/.cache` | Non-essential cache | temp files, downloaded assets |
| `XDG_RUNTIME_DIR` | `/run/user/$UID` | Runtime files | sockets, locks, PIDs |

### Benefits

- **Separation of concerns**: Config vs data vs cache
- **Backup-friendly**: Config files separate from cache
- **Clean home directory**: No dotfile pollution (`~/.app_*`)
- **User expectations**: Matches modern Linux application behavior
- **Portability**: Environment variables allow customization

---

## Path Summary

| Category | Path | Contents |
|----------|------|----------|
| **Config** | `~/.config/{module}/` | `config.toml`, user settings |
| **Data** | `~/.local/share/{module}/` | databases, workspace, user files |
| **State** | `~/.local/state/{module}/` | history, logs, session state |
| **Cache** | `~/.cache/{module}/` | temp files, regeneratable data |

### Example: {Module}

```
~/.config/{module}/
├── config.toml          # User configuration
├── agents.yaml          # Optional: agent definitions
└── plugins/             # Optional: plugin configs

~/.local/share/{module}/
├── workspace/           # Default workspace directory
├── data/                # Application data files
└── docs/                # Reference documentation

~/.local/state/{module}/
├── history              # Command/action history
├── logs/                # Application logs
└── sessions/            # Session state files

~/.cache/{module}/
├── downloads/           # Cached downloads
└── index/               # Search indices, embeddings
```

---

## Implementation

### Rust

```rust
use std::path::PathBuf;

/// Returns XDG-compliant config directory: ~/.config/{app}/
pub fn config_dir(app: &str) -> PathBuf {
    dirs::config_dir()
        .unwrap_or_else(|| dirs::home_dir().unwrap().join(".config"))
        .join(app)
}

/// Returns XDG-compliant data directory: ~/.local/share/{app}/
pub fn data_dir(app: &str) -> PathBuf {
    dirs::data_dir()
        .unwrap_or_else(|| dirs::home_dir().unwrap().join(".local/share"))
        .join(app)
}

/// Returns XDG-compliant state directory: ~/.local/state/{app}/
pub fn state_dir(app: &str) -> PathBuf {
    // Note: dirs crate may not have state_dir on all versions
    dirs::home_dir()
        .map(|h| h.join(".local/state"))
        .unwrap_or_else(|| PathBuf::from("/tmp"))
        .join(app)
}

/// Returns XDG-compliant cache directory: ~/.cache/{app}/
pub fn cache_dir(app: &str) -> PathBuf {
    dirs::cache_dir()
        .unwrap_or_else(|| dirs::home_dir().unwrap().join(".cache"))
        .join(app)
}
```

### Python

```python
import os
from pathlib import Path

def config_dir(app: str) -> Path:
    """Returns XDG-compliant config directory."""
    base = os.environ.get('XDG_CONFIG_HOME', Path.home() / '.config')
    return Path(base) / app

def data_dir(app: str) -> Path:
    """Returns XDG-compliant data directory."""
    base = os.environ.get('XDG_DATA_HOME', Path.home() / '.local/share')
    return Path(base) / app

def state_dir(app: str) -> Path:
    """Returns XDG-compliant state directory."""
    base = os.environ.get('XDG_STATE_HOME', Path.home() / '.local/state')
    return Path(base) / app

def cache_dir(app: str) -> Path:
    """Returns XDG-compliant cache directory."""
    base = os.environ.get('XDG_CACHE_HOME', Path.home() / '.cache')
    return Path(base) / app
```

### TypeScript/Node.js

```typescript
import * as os from 'os';
import * as path from 'path';

function configDir(app: string): string {
  const base = process.env.XDG_CONFIG_HOME || path.join(os.homedir(), '.config');
  return path.join(base, app);
}

function dataDir(app: string): string {
  const base = process.env.XDG_DATA_HOME || path.join(os.homedir(), '.local/share');
  return path.join(base, app);
}

function stateDir(app: string): string {
  const base = process.env.XDG_STATE_HOME || path.join(os.homedir(), '.local/state');
  return path.join(base, app);
}

function cacheDir(app: string): string {
  const base = process.env.XDG_CACHE_HOME || path.join(os.homedir(), '.cache');
  return path.join(base, app);
}
```

---

## Migration

When moving from legacy paths (e.g., `~/.{app}_history`) to XDG paths:

### Auto-Migration Pattern

```rust
// On startup, migrate legacy files to XDG location
let xdg_path = state_dir("myapp").join("history");
let legacy_path = dirs::home_dir().unwrap().join(".myapp_history");

// Create XDG directory
std::fs::create_dir_all(xdg_path.parent().unwrap())?;

// Migrate if legacy exists and XDG doesn't
if legacy_path.exists() && !xdg_path.exists() {
    std::fs::rename(&legacy_path, &xdg_path)?;
    eprintln!("Migrated {} to {}", legacy_path.display(), xdg_path.display());
}
```

### Migration Checklist

- [ ] Identify all legacy file locations
- [ ] Map each to appropriate XDG category (config/data/state/cache)
- [ ] Implement auto-migration on startup
- [ ] Update documentation with new paths
- [ ] Add migration note to release notes/changelog
- [ ] Test migration on fresh install (no legacy files)
- [ ] Test migration from legacy install

---

## Platform Notes

### Linux / WSL2

XDG is native. Use environment variables or defaults.

### macOS

macOS has its own conventions but XDG works:
- Config: `~/Library/Application Support/{app}/` (native) or `~/.config/{app}/` (XDG)
- Cache: `~/Library/Caches/{app}/` (native) or `~/.cache/{app}/` (XDG)

The `dirs` crate handles this automatically.

### Windows

Windows uses `%APPDATA%` and `%LOCALAPPDATA%`:
- Config: `%APPDATA%\{app}\` → `C:\Users\{user}\AppData\Roaming\{app}\`
- Cache: `%LOCALAPPDATA%\{app}\` → `C:\Users\{user}\AppData\Local\{app}\`

XDG paths also work on Windows (created under `%USERPROFILE%`):
- `~/.config/{app}/` → `C:\Users\{user}\.config\{app}\`
- `~/.local/share/{app}/` → `C:\Users\{user}\.local\share\{app}\`

---

## Environment Variable Override

Allow users to override paths via environment variables:

| Variable | Purpose | Example |
|----------|---------|---------|
| `{MODULE}_CONFIG_DIR` | Override config directory | `/etc/myapp` |
| `{MODULE}_DATA_DIR` | Override data directory | `/var/lib/myapp` |
| `{MODULE}_STATE_DIR` | Override state directory | `/var/log/myapp` |
| `{MODULE}_CACHE_DIR` | Override cache directory | `/tmp/myapp` |

### Precedence

1. Module-specific env var (`{MODULE}_CONFIG_DIR`)
2. XDG env var (`XDG_CONFIG_HOME`)
3. XDG default (`~/.config/`)

---

## Uninstall / Cleanup

Document cleanup paths for users:

```bash
# Linux / macOS
rm -rf ~/.config/{module}
rm -rf ~/.local/share/{module}
rm -rf ~/.local/state/{module}
rm -rf ~/.cache/{module}

# Legacy (if migrated)
rm -f ~/.{module}_history
rm -f ~/.{module}rc
```

```powershell
# Windows
Remove-Item -Recurse "$env:USERPROFILE\.config\{module}"
Remove-Item -Recurse "$env:USERPROFILE\.local\share\{module}"
Remove-Item -Recurse "$env:USERPROFILE\.local\state\{module}"
Remove-Item -Recurse "$env:USERPROFILE\.cache\{module}"
```

---

## Template Customization Guide

1. Replace `{module}` with your application name (lowercase)
2. Replace `{Module}` with your application name (PascalCase)
3. Replace `{MODULE}` with your application name (UPPERCASE)
4. Remove unused XDG categories (e.g., if no cache needed)
5. Add application-specific subdirectories
6. Update implementation examples for your language

---

## See Also

- [Configuration](../6-deployment/configuration.template.md) — config structure and options
- [Operations Manual](ops_manual.template.md) — operational procedures
- [XDG Base Directory Specification](https://specifications.freedesktop.org/basedir-spec/basedir-spec-latest.html) — official spec

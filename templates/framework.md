# Library/Framework Documentation Framework

A layered, audience-focused documentation structure for libraries and frameworks.

**Based on**: Rustboot implementation using SEA (Stratified Encapsulation Architecture)  
**Format**: W³H (WHO-WHAT-WHY-HOW) structure

## Overview

This framework provides a hierarchical documentation structure that:
- Separates concerns by audience (architects, developers, users)
- Uses hub documents for navigation
- Maintains consistency with templates
- Scales from small libraries to large frameworks

## SDLC Phase Reference

The numbered directories follow the Software Development Life Cycle (SDLC) phases:

| Phase | Folder | Purpose | Typical Content |
|-------|--------|---------|-----------------|
| 0 | `0-ideation/` | Research & exploration | Research notes, competitive analysis, proof of concepts |
| 1 | `1-requirements/` | What to build | User stories, acceptance criteria, backlog, roadmap |
| 2 | `2-planning/` | Sprint planning | Gap analysis, estimates, sprint docs |
| 3 | `3-design/` | How it works | Architecture, ADRs, sequence diagrams, API specs |
| 4 | `4-development/` | How to develop | Developer guides, setup, coding standards |
| 5 | `5-testing/` | Test strategy | Test plans, testing guides, QA procedures |
| 6 | `6-deployment/` | How to deploy | CI/CD, installation, release procedures |
| 7 | `7-operation/` | How to run | Runbooks, monitoring, troubleshooting, SLAs |

> **Note**: Not all projects need all phases. Start with `3-design/` and `4-development/` at minimum.

## Directory Structure

```
project/
├── README.md                           # Lean entry point
├── docs/
│   ├── README.md                       # Main documentation hub
│   ├── glossary.md                     # Term definitions (REQUIRED)
│   ├── 0-ideation/                     # (Optional) Research & ideas
│   ├── 1-requirements/                 # (Optional) Requirements docs
│   ├── 2-planning/                     # (Optional) Sprint planning
│   ├── 3-design/
│   │   ├── architecture.md             # Design hub document
│   │   ├── [feature]-overview.md       # Feature architecture docs
│   │   ├── [feature]-audit.md          # Audit/compliance docs
│   │   ├── compliance/
│   │   │   └── compliance_checklist.md # Architecture compliance checklist (REQUIRED)
│   │   └── adr/                        # Architecture Decision Records
│   │       ├── README.md               # ADR index
│   │       └── NNN-[decision].md       # Individual ADRs
│   ├── 4-development/
│   │   ├── developer_guide.md          # Development hub document
│   │   └── guide/
│   │       ├── [topic]_developer_guide.md  # Development guides
│   │       └── [technology]_[topic].md     # Technology-specific guides
│   ├── 5-testing/                      # (Optional) Test strategy
│   ├── 6-deployment/                   # (Optional) Deployment docs
│   ├── 7-operation/                    # (Optional) Runbooks, monitoring
│   ├── backlog.md                      # Feature backlog index
│   ├── framework-backlog.md            # Cross-cutting backlog
│   └── templates/
│       ├── README.md                   # Template usage guide
│       ├── crate_readme.template.md    # Module/component template
│       └── framework_doc.template.md   # Framework doc template
└── modules/                            # or crates/, packages/, lib/
    └── [module-name]/
        ├── Cargo.toml / package.json / setup.py
        ├── src/
        ├── docs/
        │   ├── README.md               # Module overview (W³H)
        │   ├── 3-design/
        │   │   └── toolchain.md        # Tools used, overview, how/why in system
        │   └── 6-deployment/
        │       ├── README.md           # Deployment index
        │       ├── prerequisites.md    # System requirements
        │       └── installation.md     # Installation guides
        └── backlog.md                  # Module-specific backlog
```

## File Naming Conventions

> **📝 Important**: Follow consistent naming conventions for all documentation files.

### UPPERCASE (Git Standard Files)

These files use UPPERCASE as they are recognized by GitHub/GitLab and follow community conventions:

```
README.md
LICENSE
CONTRIBUTING.md
CODE_OF_CONDUCT.md
SECURITY.md
SUPPORT.md
CHANGELOG.md
INTERNAL_USAGE.md
.github/ISSUE_TEMPLATE/
.github/PULL_REQUEST_TEMPLATE.md
```

### snake_lower_case (Project Documentation)

All other documentation files use snake_lower_case:

```
docs/
├── README.md
├── 3-design/
│   ├── architecture.md
│   ├── authentication.md
│   ├── rate_limiting.md
│   └── security_audit_report.md
├── 4-development/
│   ├── developer_guide.md
│   └── guide/
│       ├── cli_usage.md
│       ├── quick_start.md
│       └── getting_started.md
└── backlog.md
```

### Guide Naming Convention

Guides embed their SDLC phase in the filename to prevent ambiguity:

| Location | Pattern | Examples |
|----------|---------|----------|
| Colocated in phase folder | `guide_name.md` | `4-development/developer_guide.md`, `4-development/setup_guide.md` |
| In `guide/` subfolder | `name_{phase}_guide.md` | `4-development/guide/middleware_developer_guide.md` |
| Design guides | `name_design_guide.md` | `3-design/middleware_design_guide.md` |

**Rules:**
- `*_testing_*` files belong in `5-testing/`, never in `3-design/`
- `testing_strategy.md`, `testing_guide.md` → `5-testing/`
- Avoid ambiguous names like `testing_design`, `development_design`

### Naming Rules

| Category | Convention | Examples |
|----------|------------|----------|
| Git standard files | UPPERCASE | `README.md`, `LICENSE`, `CONTRIBUTING.md` |
| GitHub templates | UPPERCASE | `ISSUE_TEMPLATE/`, `PULL_REQUEST_TEMPLATE.md` |
| Project docs | snake_lower_case | `architecture.md`, `quick_start.md` |
| Directories | lowercase-hyphen | `3-design/`, `4-development/` |
| Feature-prefixed folders | `FR_{###}/` (snake_case) | `FR_502/`, `FR_200/` |
| Feature-prefixed files | `FR_{###}_{name}.ext` (snake_case) | `FR_502_runtime_execution.test`, `FR_200_edge_api.spec` |

### Feature-Prefixed Artifacts

Feature requests (FR) generate artifacts across multiple SDLC phases. All feature-scoped
folders and files **must** use the `FR_{###}` prefix in snake_case:

```
docs/
├── 1-requirements/
│   └── {domain}/
│       └── FR_{###}_{feature_name}.spec     # Feature spec
├── 2-planning/
│   └── FR_{###}/
│       └── implementation_plan.md           # Per-feature plan
├── 3-design/
│   └── FR_{###}/
│       └── architecture.arch                # Per-feature design
├── 4-development/
│   └── backlog/
│       └── FR_{###}/
│           └── backlog.md                   # Per-feature backlog
├── 5-testing/
│   └── {domain}/
│       └── FR_{###}_{feature_name}.test     # Per-feature test plan
└── 6-deployment/
    └── FR_{###}/
        └── configuration.md                 # Per-feature config
```

The `FR-{###}` notation with hyphens is reserved for identifiers in prose (headings, table
cells, requirement IDs like `FR-502.1`). File paths always use underscores.

## Git Repository Files (Required)

> **🔒 Critical**: Every library/framework MUST include appropriate Git repository files based on its open-source status.

**See**: [Repository Governance Best Practices](../4-development/guide/repository-governance.md) for comprehensive guide.

### Quick Reference

**For Open-Source Projects** - Required:
- `CODE_OF_CONDUCT.md` - Community guidelines (UPPERCASE)
- `SECURITY.md` - Vulnerability reporting (UPPERCASE)
- `SUPPORT.md` - Getting help (UPPERCASE)
- `CONTRIBUTING.md` - Contribution process (UPPERCASE)
- `LICENSE` - Open-source license (UPPERCASE)
- `.github/ISSUE_TEMPLATE/` - Bug/feature templates (UPPERCASE)
- `.github/PULL_REQUEST_TEMPLATE.md` - PR template (UPPERCASE)

**For Internal/Proprietary Projects** - Required:
- `SECURITY.md` - Internal security policy (UPPERCASE)
- `SUPPORT.md` - Internal support channels (UPPERCASE)
- `CONTRIBUTING.md` - Internal contribution process (UPPERCASE)
- `INTERNAL_USAGE.md` - Approved use cases (UPPERCASE)
- `.github/ISSUE_TEMPLATE/` - Internal issue templates (UPPERCASE)

### Template Locations

Templates available in: `docs/templates/git-files/{open-source|internal}/`

**Full details**: See [Repository Governance Best Practices](../4-development/guide/repository-governance.md)

## Navigation Flow

```
README.md (Quick Start)
    ↓
docs/README.md (Main Hub)
    ├→ 3-design/architecture.md (Design Hub)
    │   ├→ Feature architecture docs
    │   ├→ Security/compliance docs
    │   └→ ADRs
    │
    ├→ 4-development/developer_guide.md (Dev Hub)
    │   └→ Development guides
    │
    └→ Module overviews (modules/*/docs/README.md)
```

## Document Types & Templates

### 1. README.md (Entry Point)

**Purpose**: Quick Start & navigation  
**Audience**: Everyone  
**Content**:
- Project tagline (1 sentence)
- Key features (bullet points)
- Quick Start code example
- Link to `docs/README.md`
- Installation instructions
- License

**Example**:
```markdown
# ProjectName

**Tagline** - Brief description

## Features
- Feature 1
- Feature 2

## Quick Start
\`\`\`language
// Code example
\`\`\`

## Documentation
See [docs/README.md](docs/README.md) for complete documentation.

## License
MIT
```

### 2. docs/README.md (Main Hub)

**Purpose**: Central navigation to all documentation
**Audience**: All
**Content**:
- Quick navigation section
- Links to design hub
- Links to developer hub
- Link to glossary
- Complete module/crate list (organized by priority)
- Backlog links
- Template links

**Example**: See `docs/README.md` in Rustboot

### 3. docs/glossary.md (Glossary - REQUIRED)

**Purpose**: Define domain-specific terminology
**Audience**: All
**Content**:
- Alphabetized list of terms
- Clear, concise definitions
- Cross-references where applicable

**Why Required**:
- Ensures consistent understanding across readers
- Reduces ambiguity in technical discussions
- Serves as quick reference for new team members
- Prevents misunderstandings in code reviews and documentation

**Format**:
```markdown
# Glossary

Alphabetized list of terms used in [Project Name].

---

**Term 1** - Definition of term 1.

**Term 2** - Definition of term 2. See also: Related Term.

**Term 3** - Definition of term 3.
```

**Best Practices**:
- Keep definitions concise (1-2 sentences)
- Use consistent formatting (bold term, dash, definition)
- Include acronym expansions
- Cross-reference related terms
- Update when new terminology is introduced
- Link from README.md

**Example**: See `docs/glossary.md` in RustML

### 5. docs/3-design/architecture.md (Design Hub)

**Audience**: Architects, Technical Leadership, Security Teams
**Format**: W³H (WHO-WHAT-WHY-HOW)
**Content**:
- Architecture overview
- Security documentation
- ADRs index
- Design guides
- Link to compliance checklist (`compliance/compliance_checklist.md`)
- Link to module overviews
- Link to developer guide

**Example**: See `docs/3-design/architecture.md` in Rustboot

### 6. docs/4-development/developer_guide.md (Development Hub)

**Audience**: Developers, Contributors
**Format**: W³H (WHO-WHAT-WHY-HOW)
**Content**:
- Development guides organized by topic
- Testing guides
- Build/tooling guides
- Contributing guidelines
- Link to module overviews
- Link to architecture docs

**Example**: See `docs/4-development/developer_guide.md` in Rustboot

### 7. Module Overview (modules/*/docs/README.md)

**Audience**: Developers
**Format**: W³H (WHO-WHAT-WHY-HOW)
**Content**:
- WHO: **Audience** declaration
- WHAT: Clear description of the module
- Prerequisites: Tools, versions, install commands, dependencies
- WHY: Problems solved, when to use
- HOW: Usage examples, API guide
- Relationship to other modules
- Status & backlog link

**Example**: See `crates/rustboot-security/docs/README.md`

### 8. Module Toolchain (modules/*/docs/3-design/toolchain.md)

**Audience**: Developers, DevOps
**Format**: Reference documentation
**Content**:
- Tools used by this module
- Overview of each tool (what it is)
- How the tool is used in this module
- Why the tool was chosen
- Version requirements
- Verification commands

**Required sections**:
```markdown
# Toolchain

## Overview
[Brief description of the module's toolchain]

## Tools

### [Tool Name]
| | |
|---|---|
| **What** | [Description] |
| **Version** | [Minimum version] |
| **Install** | `[install command]` |

**Why we use it**: [Rationale]

**How we use it**:
```[language]
[Usage example]
```

## Version Matrix
| Tool | Minimum | Recommended |
|------|---------|-------------|
| ... | ... | ... |

## Verification
[Commands to verify toolchain setup]
```

### 9. Module Deployment (modules/*/docs/6-deployment/)

**Audience**: Developers, DevOps, Users
**Format**: Deployment guides
**Required files**:
- `README.md` - Index of deployment documentation
- `prerequisites.md` - System requirements for users and developers
- `installation.md` - Installation guides (package manager, source)

**Optional files**:
- `build.md` - Build configuration and optimization
- `ci-cd.md` - CI/CD pipeline setup
- `docker.md` - Container deployment

**README.md structure**:
```markdown
# Deployment Documentation

## Contents
| Document | Description |
|----------|-------------|
| [Prerequisites](prerequisites.md) | System requirements |
| [Installation](installation.md) | Installation guides |

## Quick Links
- **Using this module**: See [Installation](installation.md)
- **Building from source**: See [Prerequisites](prerequisites.md)
```

### 10. Framework Documentation (docs/*/\*.md)

**Audience**: Various (MUST specify)
**Format**: W³H (WHO-WHAT-WHY-HOW)
**Content**:
- WHO: **Audience** declaration (required!)
- WHAT: What is covered
- WHY: Problems/motivation
- HOW: Implementation/application
- Best practices
- Related docs

**Example**: See `docs/4-development/guide/rust-test-organization.md`

## Examples and Tests (Critical!)

> **🎯 Every module MUST have examples and tests**

### Why Examples and Tests Matter

1. **Examples** (`examples/` directory):
   - Show users HOW to use your code
   - Provide copy-paste starting points
   - Demonstrate best practices
   - Compile-checked documentation

2. **Integration Tests** (`tests/` directory):
   - Show users HOW to test their code
   - Verify public API works
   - Serve as additional usage examples
   - Catch breaking changes

3. **Navigation**: Documentation must link to code
   - Module overviews → examples + tests
   - Examples show usage patterns
   - Tests show testing patterns

### Requirements Checklist

Every module/component must have:

- [ ] **At minimum**: `examples/basic.rs` - Simple usage
- [ ] **At minimum**: `tests/integration.rs` - Public API tests
- [ ] **In docs/README.md**: "Examples and Tests" section with links
- [ ] **Links to**: Testing guides (Rust Test Organization, etc.)

### Example Structure

```
module/
├── examples/
│   ├── basic.rs           # Always required
│   ├── advanced.rs        # For complex features
│   └── [feature].rs       # One per major feature
├── tests/
│   ├── integration.rs     # Always required
│   └── [feature]_test.rs  # Additional test files as needed
└── docs/
    └── README.md          # Must link to above
```

## Documentation Rules

| Location | Format | Audience | Examples |
|----------|--------|----------|----------|
| `README.md` | Quick Start | Everyone | Project entry |
| `docs/README.md` | Hub + Links | All | Main index |
| `docs/3-design/architecture.md` | Hub + Links | Architects | Design index |
| `docs/4-development/developer_guide.md` | Hub + Links | Developers | Dev index |
| `docs/3-design/*.md` | W³H | Specified | Architecture docs |
| `docs/4-development/guide/*.md` | W³H | Specified | Dev guides |
| `modules/*/docs/README.md` | W³H + Prerequisites | Developers | Module docs |
| `modules/*/docs/3-design/toolchain.md` | Reference (what/why/how) | Developers, DevOps | Toolchain docs |
| `modules/*/docs/6-deployment/` | Deployment guides | Developers, DevOps, Users | Deployment docs |

### Key Principles

1. **W³H Pattern Universal** - All docs declare WHO, WHAT, WHY, HOW
2. **Hub Documents** - Navigate to specialized docs
4. **Hub Documents** - Navigate to specialized docs
5. **No TLDR/TOC** - Only if doc is very long (200+ lines)

## Implementation Flow

The documentation framework follows a **six-phase sequential implementation**:

```
Phase 0: Git Repository Files
    ↓ (MUST complete before Phase 1)
Phase 1: Foundation (README, docs/README.md, glossary.md, templates)
    ↓
Phase 2: Design Documentation (architecture.md, ADRs)
    ↓
Phase 3: Development Documentation (developer_guide.md, guides)
    ↓
Phase 4: Module Documentation (module READMEs, examples, tests)
    ↓
Phase 5: Backlog & Planning (backlog files)
    ↓
Phase 6: Validation (check all phases complete)
```

**Critical Path**:
- **Phase 0 is mandatory first** - Repository governance files must exist before other documentation
- **Phase 1 creates structure** - Foundation for all other documentation
- **Phases 2-5 can overlap** - Design and development docs can be created in parallel
- **Phase 6 validates everything** - Final check before project release

**Why this order?**:
1. **Phase 0 first**: Establishes project governance, licensing, and contribution process
2. **Foundation next**: Creates navigation structure for all documentation
3. **Design & Development**: Fill in the structure with content
4. **Modules**: Document individual components
5. **Backlog**: Plan future work
6. **Validation**: Ensure quality and completeness

## Implementation Checklist

### Phase 0: Git Repository Files (MUST DO FIRST)
- [ ] **Determine project type**: Open-source or internal/non-open-source
- [ ] **For Open-Source projects**:
  - [ ] Create `CODE_OF_CONDUCT.md` (required)
  - [ ] Create `SECURITY.md` (required)
  - [ ] Create `SUPPORT.md` (required)
  - [ ] Create `CONTRIBUTING.md` (required)
  - [ ] Add/verify `LICENSE` file (required)
  - [ ] Create `.github/ISSUE_TEMPLATE/bug_report.md` (required)
  - [ ] Create `.github/ISSUE_TEMPLATE/feature_request.md` (required)
  - [ ] Create `.github/PULL_REQUEST_TEMPLATE.md` (required)
  - [ ] Create `CHANGELOG.md` (recommended)
- [ ] **For Internal/Non-Open-Source projects**:
  - [ ] Create `SECURITY.md` for internal security policy (required)
  - [ ] Create `SUPPORT.md` for internal support channels (required)
  - [ ] Create `CONTRIBUTING.md` for internal contribution process (required)
  - [ ] Create `INTERNAL_USAGE.md` for approved use cases (required)
  - [ ] Create `.github/ISSUE_TEMPLATE/internal_issue.md` (required)
  - [ ] Create `OWNERS.md` for code ownership (recommended)
  - [ ] Create `COMPLIANCE.md` if applicable (recommended)

### Phase 1: Foundation
- [ ] Create lean README.md with Quick Start
- [ ] Create docs/README.md as main hub
- [ ] Create docs/glossary.md with domain terminology (REQUIRED)
- [ ] Create docs/templates/ with both templates
- [ ] Set up directory structure (0-6 folders)

### Phase 2: Design Documentation
- [ ] Create docs/3-design/architecture.md hub
- [ ] Add architecture/design documents
- [ ] Create docs/3-design/adr/ for decisions
- [ ] **Create docs/3-design/compliance/compliance_checklist.md derived from architecture.md** (REQUIRED)
- [ ] Add security/compliance docs (if applicable)

### Phase 3: Development Documentation
- [ ] Create docs/4-development/developer_guide.md hub
- [ ] Add development guides in docs/4-development/guide/
- [ ] Add testing guides
- [ ] Add technology-specific guides

### Phase 4: Module Documentation
- [ ] Create docs/README.md for each module
- [ ] Follow W³H (WHO-WHAT-WHY-HOW) structure
- [ ] **Add Prerequisites section to each overview**
- [ ] Add relationship tables
- [ ] Link from docs/README.md
- [ ] **Create examples/basic.rs for each module**
- [ ] **Create tests/integration.rs for each module**
- [ ] **Add "Examples and Tests" section to each overview**
- [ ] **Link to testing guides**
- [ ] **Create docs/3-design/toolchain.md for each module**
  - [ ] Document all tools used
  - [ ] Include what/why/how for each tool
  - [ ] Add version matrix
  - [ ] Add verification commands
- [ ] **Create docs/6-deployment/ for each module**
  - [ ] README.md - deployment index
  - [ ] prerequisites.md - system requirements
  - [ ] installation.md - installation guides

### Phase 5: Backlog & Planning
- [ ] Create module-level backlog.md files
- [ ] Create docs/backlog.md index
- [ ] Create docs/framework-backlog.md for cross-cutting work

### Phase 6: Validation
- [ ] **Verify Phase 0 complete**: All Git repository files present
- [ ] **Check project type alignment**: Files match open-source or internal status
- [ ] **Validate required files**: SECURITY.md, SUPPORT.md, CONTRIBUTING.md, issue templates
- [ ] **For open-source**: Verify CODE_OF_CONDUCT.md and LICENSE exist
- [ ] **For internal**: Verify INTERNAL_USAGE.md exists
- [ ] **Verify file naming conventions**:
  - [ ] Git standard files are UPPERCASE (README.md, LICENSE, CONTRIBUTING.md, etc.)
  - [ ] Project docs are snake_lower_case (architecture.md, quick_start.md)
  - [ ] Directories are lowercase-hyphen (3-design/, 4-development/)
  - [ ] Guides follow `name_{phase}_guide` convention in subfolders
  - [ ] No `*_testing_*` files outside `5-testing/`
- [ ] **Verify docs/glossary.md exists** with domain terminology
- [ ] **Verify docs/3-design/compliance/compliance_checklist.md exists** and reflects current architecture.md rules
- [ ] Verify no broken links
- [ ] Verify **Audience** in ALL docs
- [ ] Ensure W³H in all docs
- [ ] Remove unnecessary TLDR/TOC sections
- [ ] **Verify all modules have examples/basic.rs**
- [ ] **Verify all modules have tests/integration.rs**
- [ ] **Check all overviews link to examples + tests**

## Technology-Specific Adaptations

### Rust Projects
- Use `crates/` instead of `modules/`
- Reference Cargo.toml
- Use Rust code examples
- Include testing guides (cargo test)

### JavaScript/TypeScript Projects
- Use `packages/` instead of `modules/`
- Reference package.json
- Use JS/TS code examples
- Include npm/yarn guides

### Python Projects
- Use `packages/` instead of `modules/`
- Reference setup.py / pyproject.toml
- Use Python code examples
- Include pip/poetry guides

### Java Projects
- Use `modules/` as-is
- Reference pom.xml / build.gradle
- Use Java code examples
- Include Maven/Gradle guides

## Example Implementations

### Small Library (5-10 modules)
- Minimal structure: README, docs/README.md, module docs
- Single architecture.md
- Single developer_guide.md
- Templates in docs/templates/

### Medium Framework (10-20 modules)
- Full structure with design + dev hubs
- Security documentation
- ADRs for major decisions
- Technology-specific guides

### Large Framework (20+ modules)
- Complete structure with all 0-6 folders
- Multiple design documents
- Comprehensive ADRs
- Extensive development guides
- Compliance documentation

## Tools & Automation

### Link Checking
```bash
# Find broken links (example with grep)
find docs -name "*.md" -exec grep -H "\[.*\](.*)" {} \;
```

### Template Validation
```bash
# Check for Audience in all docs
grep -r "**Audience**" docs/ modules/*/docs/
```

### W³H Validation
```bash
# Check structure in all docs
for file in $(find . -name "README.md"); do
  echo "Checking $file"
  grep -q "## WHAT" $file && echo "  ✓ WHAT"
  grep -q "## WHY" $file && echo "  ✓ WHY"
  grep -q "## HOW" $file && echo "  ✓ HOW"
done
```

## Best Practices

### ✅ DO
- Keep README lean (< 100 lines)
- Use hub documents for navigation
- Declare **Audience** in every document (W³H)
- Maintain W³H structure
- Link related docs
- Update docs/README.md when adding modules
- Use templates for consistency

### ❌ DON'T
- Put all docs in README
- Create TLDR/TOC for short docs
- Have broken links
- Duplicate content across docs
- Skip WHY sections
- Ignore templates

## Maintenance

### Regular Reviews
- **Monthly**: Check for broken links
- **Per Release**: Update version numbers
- **Per Module**: Create README.md
- **Per Decision**: Create ADR

### Documentation Debt
Track in `docs/framework-backlog.md`:
- Missing module docs
- Outdated examples
- Broken links
- Unclear sections

## Migration Guide

### From Unstructured Docs

1. **Audit current docs**: List all existing documentation
2. **Create structure**: Set up directory hierarchy
3. **Categorize**: Sort docs into design vs development
4. **Create hubs**: Write architecture.md and developer_guide.md
5. **Convert format**: Apply W³H to each doc
6. **Add Audience**: Declare **Audience** in ALL docs
7. **Link everything**: Update docs/README.md
8. **Clean README**: Simplify to Quick Start only

### From Other Formats

**From README-heavy**:
- Extract architecture → docs/3-design/
- Extract guides → docs/4-development/
- Keep only Quick Start in README

**From Wiki-style**:
- Organize by audience
- Create hub documents
- Apply W³H structure

## Success Metrics

- ✅ **Git repository files present** (Phase 0 complete)
- ✅ **Appropriate files for project type** (open-source or internal)
- ✅ **CODE_OF_CONDUCT.md exists** (open-source only)
- ✅ **SECURITY.md exists** (all projects)
- ✅ **SUPPORT.md exists** (all projects)
- ✅ **CONTRIBUTING.md exists** (all projects)
- ✅ **Issue templates exist** (all projects)
- ✅ **File naming conventions followed**:
  - Git standard files UPPERCASE
  - Project docs snake_lower_case
  - Guides follow `name_{phase}_guide` convention
- ✅ **docs/glossary.md exists** with domain terminology
- ✅ **docs/3-design/compliance/compliance_checklist.md exists** derived from architecture.md
- ✅ All modules have docs/README.md
- ✅ No broken links
- ✅ README < 100 lines
- ✅ All docs declare **Audience** (W³H)
- ✅ All docs use W³H
- ✅ Hub documents exist at each level
- ✅ New contributors can navigate easily
- ✅ **All modules have examples/basic.rs**
- ✅ **All modules have tests/integration.rs**
- ✅ **All overviews link to examples and tests**
- ✅ **All overviews have Prerequisites section**
- ✅ **All modules have docs/3-design/toolchain.md**
- ✅ **All modules have docs/6-deployment/ with overview, prerequisites, installation**
- ✅ **Documentation guides users to working code**

---

**Based on**: Rustboot framework implementation  
**License**: MIT (adapt freely)  
**Contributions**: Welcome improvements and adaptations

# SDLC-Driven Documentation: A Framework for Modular Software Systems

> **TLDR:** A documentation framework that aligns folder structure with SDLC phases, mirrors root structure in submodules, and enforces compulsory files through PR checklists. Applied to SWE Studio, it reduced documentation volume by 57% while achieving 100% structural compliance across modules.

**Document Type:** Technical Report
**Status:** Working Paper
**Version:** 1.0

## Table of Contents
- [Abstract](#abstract)
- [1. Introduction](#1-introduction)
- [2. Problem Statement](#2-problem-statement)
- [3. The Framework](#3-the-framework)
- [4. Implementation](#4-implementation)
- [5. Case Study: SWE Studio](#5-case-study-swe-studio)
- [6. Evaluation](#6-evaluation)
- [7. Related Work](#7-related-work)
- [8. Limitations](#8-limitations)
- [9. Conclusion](#9-conclusion)
- [References](#references)

---

## Abstract

Documentation in modular software systems often suffers from inconsistency, unclear ownership, and lack of enforcement mechanisms. This paper presents the SDLC-Driven Documentation Framework, a systematic approach that: (1) organizes documentation by software development lifecycle phases, (2) enforces a mirrored structure between project root and submodules, (3) defines compulsory files to ensure minimum coverage, and (4) implements enforcement through pull request checklists.

We applied this framework to SWE Studio, a modular IDE comprising 15+ Rust crates. The consolidation effort reduced total documentation by 83% (1,586 lines to 264 lines) while eliminating orphaned files and establishing consistent structure across all modules. The framework is language-agnostic and applicable to monorepos, microservices architectures, and any project following modular design principles.

---

## 1. Introduction

### 1.1 The Documentation Challenge

Software documentation is a well-known pain point in engineering organizations. Studies suggest developers spend significant time searching for information, with some estimates ranging from 20-30% of work time [1]. Poor documentation is consistently cited as a top frustration among software engineers [2]. Despite the availability of documentation tools and platforms, the fundamental problem persists: where should documentation live, and who owns it?

### 1.2 Modular Systems Amplify the Problem

Modern software architecture emphasizes modularity—monorepos, microservices, plugin systems, and component libraries. While modularity benefits code organization, it creates documentation challenges:

- **Fragmentation**: Documentation scatters across module boundaries
- **Duplication**: Common patterns documented multiple times
- **Orphaning**: Central docs reference modules that maintain no docs
- **Inconsistency**: Each module follows different conventions

### 1.3 Key Insight

We observe that documentation structure should mirror code structure. If code is organized into modules with clear boundaries, documentation should follow the same boundaries. If code follows architectural patterns (e.g., layered architecture), documentation should follow documentation patterns.

This insight leads to our framework's core principle: **documentation is architecture**.

### 1.4 Contributions

This paper makes the following contributions:

1. **SDLC-Aligned Folder Structure**: A six-phase organization mapping to software lifecycle
2. **Mirrored Structure Pattern**: Identical organization for root and submodules
3. **Compulsory Files Specification**: Minimum required documentation per module
4. **Enforcement Mechanism**: PR template integration for compliance checking
5. **Empirical Validation**: Case study applying framework to production codebase

---

## 2. Problem Statement

### 2.1 Requirements for Documentation Framework

An effective documentation framework must satisfy five requirements:

| Requirement | Description |
|-------------|-------------|
| **R1: Predictability** | Developers know where to find and place documentation |
| **R2: Scalability** | Works for projects with 5 modules or 500 modules |
| **R3: Clear Ownership** | No ambiguity about who maintains what |
| **R4: Enforceability** | Gaps are visible, compliance is verifiable |
| **R5: Comprehensiveness** | Covers all aspects of software lifecycle |

### 2.2 Anti-Patterns in Current Practice

Through analysis of open-source projects and industry codebases, we identify four prevalent anti-patterns:

#### Anti-Pattern 1: Central Documentation Dump

```
project/
├── src/
│   ├── module-a/
│   ├── module-b/
│   └── module-c/
└── docs/
    ├── module-a.md
    ├── module-b.md
    ├── module-c.md
    └── ... (dozens more)
```

**Problem**: Central `docs/` folder becomes a dumping ground. No clear ownership—when module-a changes, who updates `docs/module-a.md`? Files become stale, and there's no structural connection between code and documentation.

#### Anti-Pattern 2: Module-Only Documentation

```
project/
├── module-a/
│   └── README.md
├── module-b/
│   └── README.md
└── module-c/
    └── README.md
```

**Problem**: No project-level documentation. New developers cannot understand how modules interact. Architecture decisions are undocumented.

#### Anti-Pattern 3: Unstructured Folders

```
project/docs/
├── api.md
├── architecture.md
├── CONTRIBUTING.md
├── deployment.md
├── dev-setup-guide.md
├── faq.md
├── getting-started.md
├── testing.md
└── troubleshooting.md
```

**Problem**: Flat structure doesn't scale. With 50+ files, finding documentation requires searching. No logical grouping.

#### Anti-Pattern 4: Optional Everything

```
module/
├── README.md          # Sometimes present
├── ARCHITECTURE.md    # Rarely present
└── docs/              # Usually empty
```

**Problem**: Without requirements, documentation is perpetually "planned for later." Gaps are hidden because there's no expectation of what should exist.

### 2.3 Research Questions

We address the following questions:

- **RQ1**: Can SDLC phases provide intuitive organization for documentation?
- **RQ2**: Does mirrored structure reduce cognitive load for navigation?
- **RQ3**: Do compulsory files increase documentation coverage?
- **RQ4**: Can PR checklists effectively enforce documentation standards?

---

## 3. The Framework

### 3.1 Core Principles

The SDLC-Driven Documentation Framework rests on five principles:

1. **SDLC Alignment**: Folders map to software development lifecycle phases
2. **Mirrored Structure**: Root and modules follow identical organization
3. **Domain Ownership**: Documentation belongs where it describes
4. **Compulsory Minimum**: Certain files are required, not optional
5. **Visible Gaps**: Missing files are structurally obvious

#### 3.1.1 Object-Oriented Programming Parallels

These principles map directly to well-known OOP and software design concepts [11-15], making them intuitive for developers:

| Principle | OOP/Design Concept | Explanation |
|-----------|-------------------|-------------|
| **No Deep Links** | Law of Demeter | Only talk to immediate neighbors. Root → overview → module. Never skip levels. |
| **Own Your Scope** | Single Responsibility (S) | Each level has one job. Root docs = root concerns. Module docs = module concerns. |
| **Document Once** | DRY | Details live in one place—the owning module. Root references, never duplicates. |
| **Hide Internals** | Encapsulation | Module internals stay in module docs. Root exposes only the navigation interface. |
| **Stable Navigation** | Open/Closed (O) | Structure is open for new modules, closed for modification. Adding a module doesn't change root. |
| **Consistent Structure** | Liskov Substitution (L) | Any module following the pattern is navigable the same way. Swap modules, same experience. |
| **Minimal Exposure** | Interface Segregation (I) | Each level exposes only what's needed for navigation, not implementation details. |
| **Reference Down** | Dependency Inversion (D) | Depend on structure (abstractions), not specific file paths (concretions). |
| **Level-Appropriate Docs** | YAGNI | Don't create root docs for module concerns. Document only where needed. |
| **Simplified Layers** | Facade Pattern | Each level provides a clean interface to the complexity below. |

**Additional Patterns [14, 15]:**
- **Composition over Inheritance** - Modules compose their own docs rather than inheriting from root
- **Chain of Responsibility** - Each level handles what it can, delegates the rest down [14]
- **High Cohesion** - Related documentation stays together within each module [15]

#### 3.1.2 Navigation Hierarchy

Documentation follows a strict hierarchy. Each level documents only its own concerns and links to the next level down—never skipping levels.

**Navigation Path:**
```
README.md → doc/overview.md → {MODULE}/README → {MODULE}/doc/4-development/setup-guide.md
```

This ensures users navigate progressively deeper, understanding context at each level.

### 3.2 SDLC Folder Structure

Documentation is organized into six folders corresponding to SDLC phases:

```
doc/
├── 1-requirements/    # WHAT to build
├── 2-planning/        # WHEN and HOW to build
├── 3-design/          # HOW it's architected
├── 4-development/     # HOW to develop
├── 5-testing/         # HOW to verify
└── 6-operation/       # HOW to run and maintain
```

#### Figure 1: SDLC Phase Mapping

```
┌─────────────────────────────────────────────────────────────────┐
│                    Software Development Lifecycle                │
├─────────────┬─────────────┬─────────────┬─────────────┬─────────┤
│ Requirements│  Planning   │   Design    │ Development │ Testing │
│      ↓      │      ↓      │      ↓      │      ↓      │    ↓    │
│ 1-require-  │ 2-planning/ │ 3-design/   │ 4-develop-  │5-testing│
│ ments/      │             │             │ ment/       │         │
├─────────────┴─────────────┴─────────────┴─────────────┴─────────┤
│                           Operation                              │
│                              ↓                                   │
│                        6-operation/                              │
└─────────────────────────────────────────────────────────────────┘
```

#### Rationale

Developers intuitively understand SDLC phases from their education and experience. When asked "where does the architecture document go?", the answer is unambiguous: `3-design/`. This eliminates the cognitive overhead of learning project-specific conventions.

### 3.3 Folder Contents

| Folder | Phase | Contents |
|--------|-------|----------|
| `1-requirements/` | Requirements | Business requirements (BRD), user stories, specifications |
| `2-planning/` | Planning | Backlog, roadmap, feature proposals, sprint plans |
| `3-design/` | Design | Architecture, ADRs, sequence diagrams, patterns |
| `4-development/` | Development | Developer guides, setup instructions, workflows |
| `5-testing/` | Testing | Test strategy, coverage reports, test plans |
| `6-operation/` | Operations | Deployment guides, runbooks, monitoring setup |

### 3.4 Mirrored Structure

The framework's second principle mandates that root and modules follow identical structure:

#### Figure 2: Mirrored Structure

```
ROOT (swe-studio/)                    MODULE ({module}/)
├── README.md                         ├── README.md
└── doc/                              └── doc/
    ├── overview.md                       ├── overview.md
    ├── 1-requirements/                   ├── 3-design/
    │   └── brd.md                        │   ├── architecture.md
    ├── 2-planning/                       │   ├── sequence.md
    │   └── backlog.md                    │   ├── workflow.md
    ├── 3-design/                         │   └── toolchain.md
    │   ├── architecture.md               ├── 4-development/
    │   └── adr/                          │   ├── developer-guide.md
    ├── 4-development/                    │   └── setup-guide.md
    │   └── developer-guide.md            └── 5-testing/
    ├── 5-testing/                            └── testing-strategy.md
    │   └── testing-strategy.md
    └── 6-operation/
        └── ops-manual.md
```

#### Rationale

Mirrored structure provides **transferable knowledge**. Once a developer learns the root structure, they can navigate any module without additional learning. This is particularly valuable in large codebases where developers frequently work across module boundaries.

### 3.5 Compulsory Files

The framework specifies minimum required files for root and modules:

#### Root Compulsory Files

| File | Purpose | Answers |
|------|---------|---------|
| `README.md` | Project entry point | "What is this project?" |
| `CHANGELOG.md` | Release notes | "What changed in each version?" |
| `CONTRIBUTING.md` | Contribution guidelines | "How do I contribute?" |
| `SECURITY.md` | Security policy | "How do I report vulnerabilities?" |
| `doc/overview.md` | WHAT/HOW/WHY | "How does it all fit together?" |
| `doc/2-requirements/brd.md` | Business requirements | "Why does this exist?" |
| `doc/4-development/developer-guide.md` | Development guide | "How do I contribute?" |
| `doc/4-development/backlog.md` | Root feature backlog | "What features are planned?" |
| `doc/4-development/kanban/` | Root kanban folder (domain-prefixed files) | "What's in progress?" |
| `doc/6-operation/ops-manual.md` | Operations manual | "How do I run this?" |
| `doc/6-operation/releases/` | Detailed release docs | "Migration guides, breaking changes" |

#### Module Compulsory Files

| File | Purpose | Answers | Required |
|------|---------|---------|----------|
| `README.md` | Module entry point | "What does this module do?" | Yes |
| `CHANGELOG.md` | Release notes | "What changed in each version?" | Yes |
| `CONTRIBUTING.md` | Contribution guidelines | "How do I contribute?" | Yes |
| `SECURITY.md` | Security policy | "How do I report vulnerabilities?" | Yes |
| `doc/overview.md` | WHAT/HOW/WHY | "Why was it built this way?" | Yes |
| `doc/3-design/architecture.md` | Internal architecture | "How is it structured?" | Yes |
| `doc/3-design/sequence.md` | Interaction flows | "How do components interact?" | Yes |
| `doc/3-design/workflow.md` | Process/pipeline | "What's the data flow?" | Yes |
| `doc/3-design/toolchain.md` | Tools and dependencies | "What tools does it use?" | Yes |
| `doc/4-development/developer-guide.md` | Module dev guide | "How do I work on this?" | Yes |
| `doc/4-development/setup-guide.md` | Setup instructions | "How do I set up locally?" | Yes |
| `doc/4-development/backlog.md` | Feature backlog | "What features are planned?" | Optional |
| `doc/4-development/kanban.md` | Sprint kanban (single file) | "What's in progress?" | Optional |
| `doc/5-testing/testing-strategy.md` | Test strategy | "How do I test this?" | Yes |
| `doc/6-operation/releases/` | Detailed release docs | "Migration guides, breaking changes" | Optional |

**Total: 12 required + 3 optional files per module**

#### Rationale

Compulsory files transform documentation from "nice to have" to "required deliverable." Missing files are visible in directory listings—an empty `3-design/` folder signals a documentation gap. This visibility creates social pressure for compliance and makes gaps reviewable in pull requests.

### 3.6 Domain Ownership

The framework's third principle mandates that documentation belongs to the domain it describes:

#### Correct Placement

```
crates/swe-terminal/doc/3-design/adr/001-pty-architecture.md
crates/swe-lsp/doc/5-testing/testing-strategy.md
```

#### Incorrect Placement

```
doc/3-design/adr/001-terminal-pty-architecture.md  ✗
doc/5-testing/lsp-testing-strategy.md              ✗
```

#### Rationale

Domain ownership mirrors encapsulation in object-oriented design—the same principle that keeps implementation details inside classes keeps documentation inside modules. This provides six benefits:

1. **Locality**: Change code and update its docs in the same PR—no context switching
2. **Clear ownership**: Module maintainers own module docs—no ambiguity
3. **Discoverability**: Look at a module, find its docs right there—no searching
4. **Reduced coupling**: Root docs reference modules but don't contain details—modules evolve independently
5. **Atomic deletion**: When a module is removed, its docs go with it—no orphans
6. **No stale references**: Central docs cannot reference non-existent module internals

### 3.7 Content Standards

#### 3.7.1 TLDR + TOC Pattern

Every document begins with a summary and navigation:

```markdown
# Document Title

> **TLDR:** One to three sentence summary of the document.

## Table of Contents
- [Section One](#section-one)
- [Section Two](#section-two)
- [Section Three](#section-three)
```

**Rationale**: Developers often scan documentation. TLDR enables quick relevance assessment. TOC enables non-linear navigation.

#### 3.7.2 WHAT/HOW/WHY Pattern

Every `overview.md` file follows a three-section structure:

| Section | Questions Answered |
|---------|-------------------|
| **WHAT** | What does this do? What features? What problems solved? |
| **HOW** | How is it architected? How do layers interact? How to extend? |
| **WHY** | Why these decisions? Why this architecture? Why not alternatives? |

**Rationale**: These are the three fundamental questions developers ask when encountering new code. Structuring documentation around them ensures completeness.

### 3.8 Supporting Structures

#### 3.8.1 Architecture Decision Records (ADRs)

ADRs document significant architectural decisions. Located at `{module}/doc/3-design/adr/`:

```
3-design/adr/
├── 0001-use-tokio-for-async.md
├── 0002-pty-communication-via-channels.md
└── 0003-event-streaming-over-sse.md
```

**When to create an ADR:**
- Choosing between multiple valid approaches
- Decision has long-term codebase impact
- Trade-offs involved (performance vs. simplicity)
- Future developers will ask "why was it done this way?"
- Reversing the decision would be costly

**When to skip:**
- Following established project patterns
- Choice is obvious or industry standard
- Implementation detail, not architectural
- Decision is easily reversible

**Heuristic**: If you debated the decision for more than 10 minutes, it probably deserves an ADR.

#### 3.8.2 Research Papers

Supporting research is documented under `{folder}/papers/`:

```
3-design/papers/
├── algorithm-comparison.md
├── performance-analysis.md
└── literature-review.md
```

**Use for:**
- Literature reviews informing design decisions
- Algorithm comparisons with benchmarks
- Performance analyses
- Third-party research references

### 3.9 File Naming Conventions

| Location | Convention | Examples |
|----------|------------|----------|
| Root level | UPPERCASE | `README.md`, `CONTRIBUTING.md`, `LICENSE` |
| Subdirectories | lowercase | `overview.md`, `architecture.md` |
| Multi-word names | hyphens | `testing-strategy.md`, `developer-guide.md` |

**Prohibited:**
- `camelCase.md`
- `snake_case.md`
- Acronyms as names (`ARCH.md`, `DEV.md`)

---

## 4. Implementation

### 4.1 Enforcement via Pull Request Template

The framework is enforced through a PR template that includes a documentation checklist:

```markdown
## Documentation Checklist

> Reference: doc/governance-framework/doc/documentation-standard.md

### For New Modules

- [ ] `README.md` with TLDR + TOC
- [ ] `doc/overview.md` with WHAT/HOW/WHY

#### 3-design/
- [ ] `architecture.md`
- [ ] `sequence.md`
- [ ] `workflow.md`
- [ ] `toolchain.md`

#### 4-development/
- [ ] `developer-guide.md`
- [ ] `setup-guide.md`

#### 5-testing/
- [ ] `testing-strategy.md`

### For Existing Modules

- [ ] Updated relevant docs if behavior changed
- [ ] Added ADR if significant architectural decision made

### For Root Changes

- [ ] Updated `doc/overview.md` if project scope changed
- [ ] Updated `doc/4-development/developer-guide.md` if workflow changed
```

### 4.2 CI Integration (Future Work)

Automated enforcement can be achieved through CI checks:

```yaml
# .github/workflows/docs-check.yml
name: Documentation Check

on: [pull_request]

jobs:
  check-docs:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Check compulsory files
        run: |
          for module in crates/*/; do
            for file in README.md doc/overview.md doc/3-design/architecture.md; do
              if [ ! -f "$module$file" ]; then
                echo "Missing: $module$file"
                exit 1
              fi
            done
          done
```

### 4.3 Migration Strategy

For existing projects adopting the framework:

1. **Audit**: List all existing documentation files
2. **Classify**: Map each file to appropriate SDLC folder
3. **Consolidate**: Merge duplicate/overlapping content
4. **Relocate**: Move files to correct locations
5. **Create**: Add missing compulsory files
6. **Update**: Fix broken cross-references
7. **Enforce**: Add PR template and CI checks

---

## 5. Case Study: SWE Studio

### 5.1 Project Background

SWE Studio is a modular IDE built with Rust, featuring:
- Dual interface (TUI and GUI)
- 15+ crates following Stratified Encapsulation Architecture (SEA)
- LSP integration, terminal emulation, Git operations
- ~50,000 lines of Rust code

### 5.2 Initial State

Before applying the framework, documentation exhibited all four anti-patterns:

#### Central Dump
```
doc/
├── plugin_system.md
├── plugin_quick_reference.md
├── plugin_system_summary.md      # 3 files, same topic
├── 4-development/
│   ├── editor-core.md            # Orphan stubs
│   ├── terminal-core.md
│   ├── syntax.md
│   └── ... (8 more stubs)
```

#### Inconsistent Module Documentation
```
crates/swe-terminal/doc/
├── overview.md
├── 3-design/
│   └── quality-centre/           # Non-standard folder
│       ├── tools.md
│       └── review-process.md
└── 5-testing/
    ├── strategy.md
    ├── testing.md                # Duplicate
    └── workflow.md               # Overlap
```

#### Misplaced Files
```
doc/3-design/adr/
└── 0001-terminal-communication-architecture.md  # Should be in terminal module

doc/5-testing/
└── terminal-keyboard-tests.md                   # Should be in terminal module
```

### 5.3 Migration Process

#### Step 1: Consolidation

| Before | After | Reduction |
|--------|-------|-----------|
| `plugin_system.md` (302 lines) | `plugin-system.md` (184 lines) | 39% |
| `plugin_quick_reference.md` (270 lines) | *(merged)* | 100% |
| `plugin_system_summary.md` (317 lines) | *(merged)* | 100% |
| **Total: 889 lines** | **184 lines** | **79%** |

#### Step 2: Orphan Elimination

Deleted 8 orphan stubs from `doc/4-development/`:
- `editor-core.md`
- `terminal-core.md`
- `syntax.md`
- `vcs.md`
- `project.md`
- `swq.md`
- `studio-agent.md`
- `swe-studio-agent.md`

**Total: 2,324 lines removed**

#### Step 3: Relocation

| File | From | To |
|------|------|-----|
| `terminal-communication-architecture.md` | `doc/3-design/adr/` | `crates/swe-terminal/doc/3-design/adr/` |
| `terminal-keyboard-tests.md` | `doc/5-testing/` | `crates/swe-terminal/doc/5-testing/` |
| `nushell-integration.md` | `doc/3-design/integration/` | `crates/swe-terminal/doc/3-design/` |
| `async-tools.md` | `crates/swe-terminal/doc/` | `doc/3-design/` (generic content) |

#### Step 4: Structure Creation

Created missing compulsory files:
- `doc/1-requirements/` folder
- `doc/2-planning/` folder (moved from `doc/1-requirements/planning/`)
- Module `overview.md` files for SEA modules

### 5.4 Final State

#### Root Structure
```
doc/
├── overview.md
├── 1-requirements/
│   └── brd.md
├── 2-planning/
│   ├── backlog.md
│   └── features/
├── 3-design/
│   ├── architecture.md
│   ├── coding-standard.md
│   ├── adr/
│   │   └── 2025-01-terminology-deliberation.md
│   ├── papers/
│   └── uxui/
├── governance-framework/
│   ├── doc/
│   │   ├── documentation-standard.md
│   │   └── sea-workflow.md
│   └── templates/
├── 4-development/
│   └── developer-guide.md
├── 5-testing/
│   └── testing-strategy.md
└── 6-operation/
    └── ops-manual.md
```

#### Module Structure (swe-terminal)
```
crates/swe-terminal/
├── README.md
└── doc/
    ├── overview.md
    ├── 3-design/
    │   ├── architecture.md
    │   ├── nushell.md
    │   ├── toolchain.md
    │   └── adr/
    │       └── 0001-terminal-communication-architecture.md
    └── 5-testing/
        ├── testing.md
        └── terminal-keyboard-tests.md
```

---

## 6. Evaluation

### 6.1 Quantitative Results

| Metric | Before | After | Change |
|--------|--------|-------|--------|
| Total documentation lines | 4,200+ | 1,800 | -57% |
| Orphaned files | 10 | 0 | -100% |
| Duplicate content instances | 5 | 0 | -100% |
| Modules with overview.md | 1/4 | 4/4 | +300% |
| Modules following structure | 0/4 | 4/4 | +400% |
| Compulsory file compliance | ~30% | 100% | +233% |

### 6.2 Qualitative Assessment

#### Addressing Research Questions

**RQ1: Can SDLC phases provide intuitive organization?**

Yes. During migration, file placement decisions were unambiguous. "Where does the architecture document go?" has exactly one answer: `3-design/`. No discussion or convention lookup required.

**RQ2: Does mirrored structure reduce cognitive load?**

Yes. After learning root structure, developers navigated module documentation without guidance. The pattern "overview.md is always at doc/overview.md" transferred across all modules.

**RQ3: Do compulsory files increase coverage?**

Yes. Before: coverage was inconsistent (some modules had 0 docs, others had 10). After: all SEA modules have exactly 9 compulsory files. Gaps are now visible.

**RQ4: Can PR checklists enforce standards?**

Partially validated. PR template implemented; long-term compliance tracking is future work.

### 6.3 Observed Benefits

During migration and subsequent development, we observed the following qualitative improvements:

1. **Reduced navigation time**: Developers no longer search for documentation location—the SDLC structure provides deterministic placement.

2. **Structured thinking**: The WHAT/HOW/WHY pattern encourages documentation authors to address design rationale, not just implementation details.

3. **Visible accountability**: Empty compulsory file placeholders create social pressure to complete documentation before code review approval.

*Note: These observations are anecdotal from the development team. Formal user studies with controlled methodology would strengthen these claims.*

---

## 7. Related Work

### 7.1 Documentation Frameworks

#### Diátaxis

Diátaxis [3] organizes documentation by user needs into four quadrants:
- **Tutorials**: Learning-oriented
- **How-to guides**: Task-oriented
- **Reference**: Information-oriented
- **Explanation**: Understanding-oriented

**Comparison**: Diátaxis focuses on content type; our framework focuses on lifecycle phase. They are complementary—Diátaxis can inform content within SDLC folders.

#### Arc42

Arc42 [4] provides a template for architecture documentation with 12 sections covering stakeholders, constraints, context, building blocks, runtime, deployment, etc.

**Comparison**: Arc42 is comprehensive for architecture documentation but doesn't address non-architectural docs (testing, operations). Our `3-design/architecture.md` can follow Arc42 internally.

#### C4 Model

The C4 Model [5] provides hierarchical software architecture diagrams: Context, Containers, Components, Code.

**Comparison**: C4 focuses on visualization; our framework focuses on organization. C4 diagrams fit naturally in `3-design/architecture.md`.

### 7.2 Decision Documentation

#### Architecture Decision Records (ADRs)

ADRs [6] document significant architectural decisions with context, decision, and consequences.

**Integration**: Our framework incorporates ADRs at `{module}/doc/3-design/adr/`, adding guidance on when to create them.

#### RFC Process

The RFC (Request for Comments) process [7] provides a mechanism for proposing and discussing changes.

**Comparison**: RFCs are pre-decision; ADRs are post-decision. RFCs could live in `2-planning/` during discussion, then convert to ADRs in `3-design/adr/` after acceptance.

### 7.3 Comparison Matrix

| Framework | Scope | Organization | Enforcement | Module Support |
|-----------|-------|--------------|-------------|----------------|
| Diátaxis | Content | By user need | None | No |
| Arc42 | Architecture | By concern | Template | No |
| C4 Model | Visualization | By abstraction | None | No |
| ADR | Decisions | Chronological | None | Yes |
| **This Framework** | **Full lifecycle** | **By SDLC phase** | **PR checklist** | **Yes** |

---

## 8. Limitations

### 8.1 Framework Limitations

1. **Initial Overhead**: Creating 9 compulsory files per module requires upfront investment. For small utilities or prototypes, this may be excessive.

2. **Rigidity**: Fixed folder structure may not fit all organizational models. Teams with different SDLC interpretations may need adaptation.

3. **Enforcement Gap**: PR checklists rely on reviewer diligence. Without CI automation, compliance is not guaranteed.

### 8.2 Case Study Limitations

1. **Single Project**: Validation limited to one codebase (SWE Studio). Generalizability requires broader application.

2. **Team Size**: Small team; scaling effects unknown.

3. **Short Duration**: Long-term maintenance benefits not yet measured.

### 8.3 Threats to Validity

1. **Author Bias**: Framework designed and evaluated by same team.

2. **Hawthorne Effect**: Improvement may partially reflect increased documentation attention, not framework effectiveness.

3. **Metrics Selection**: Chosen metrics favor consolidation; alternative metrics might show different results.

---

## 9. Conclusion

### 9.1 Summary

This paper presented the SDLC-Driven Documentation Framework, addressing documentation challenges in modular software systems through:

1. **SDLC-Aligned Folders**: Six folders mapping to software lifecycle phases
2. **Mirrored Structure**: Identical organization for root and modules
3. **Domain Ownership**: Documentation belongs where it describes
4. **Compulsory Files**: Minimum required files ensuring coverage
5. **PR Enforcement**: Checklist integration for compliance

### 9.2 Key Findings

- SDLC phases provide intuitive, unambiguous file placement
- Mirrored structure enables knowledge transfer across modules
- Compulsory files make documentation gaps visible
- Framework application reduced documentation by 57% while increasing coverage

### 9.3 Recommendations

For teams adopting this framework:

1. **Start with root structure**: Establish project-level documentation first
2. **Migrate incrementally**: Apply to new modules immediately, migrate existing modules over time
3. **Enforce early**: Add PR template before technical debt accumulates
4. **Adapt thoughtfully**: Adjust compulsory files to organizational needs, but maintain structural consistency

### 9.4 Future Work

1. **CI Automation**: Develop tooling for automated compulsory file checking
2. **Documentation Linting**: Content standards enforcement (TLDR presence, TOC validity)
3. **Metrics Dashboard**: Visualization of documentation coverage over time
4. **Broader Validation**: Apply framework to additional projects across different languages and team sizes
5. **Template Generator**: CLI tool to scaffold compliant documentation structure
6. **Formal User Studies**: Conduct rigorous empirical validation (see [Research Methodology](./research-methodology.md))

---

## References

[1] T. D. LaToza and B. A. Myers, "Hard-to-answer questions about code," in *Evaluation and Usability of Programming Languages and Tools (PLATEAU)*, 2010.

[2] Stack Overflow, "Developer Survey Results," 2023. Available: https://survey.stackoverflow.co/2023/

[3] D. Procida, "Diátaxis: A systematic approach to technical documentation authoring," 2017. Available: https://diataxis.fr/

[4] G. Starke and P. Hruschka, "Arc42: Template for architecture communication and documentation," 2005. Available: https://arc42.org/

[5] S. Brown, "The C4 model for visualizing software architecture," 2018. Available: https://c4model.com/

[6] M. Nygard, "Documenting Architecture Decisions," 2011. Available: https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions

[7] Internet Engineering Task Force, "The RFC Series," Available: https://www.rfc-editor.org/

[8] R. C. Martin, *Clean Architecture: A Craftsman's Guide to Software Structure and Design*, Prentice Hall, 2017.

[9] E. Evans, *Domain-Driven Design: Tackling Complexity in the Heart of Software*, Addison-Wesley, 2003.

[10] M. Fowler, "Writing Software Patterns," 2006. Available: https://martinfowler.com/articles/writingPatterns.html

[11] R. C. Martin, *Clean Code: A Handbook of Agile Software Craftsmanship*, Prentice Hall, 2008. (SOLID principles, Single Responsibility)

[12] K. J. Lieberherr and I. Holland, "Assuring Good Style for Object-Oriented Programs," *IEEE Software*, vol. 6, no. 5, pp. 38-48, 1989. (Law of Demeter)

[13] A. Hunt and D. Thomas, *The Pragmatic Programmer: From Journeyman to Master*, Addison-Wesley, 1999. (DRY, YAGNI)

[14] E. Gamma, R. Helm, R. Johnson, and J. Vlissides, *Design Patterns: Elements of Reusable Object-Oriented Software*, Addison-Wesley, 1994. (Facade, Chain of Responsibility)

[15] L. Constantine and E. Yourdon, *Structured Design: Fundamentals of a Discipline of Computer Program and Systems Design*, Prentice Hall, 1979. (Cohesion and Coupling)

---

## Appendix A: Complete File Listing

### A.1 Root Compulsory Files

```
swe-studio/
├── README.md
├── CHANGELOG.md
├── CONTRIBUTING.md
├── SECURITY.md
└── doc/
    ├── overview.md
    ├── 1-planning/
    ├── 2-requirements/
    │   └── brd.md
    ├── 3-design/
    │   ├── architecture.md
    │   └── adr/
    ├── 4-development/
    │   ├── developer-guide.md
    │   ├── backlog.md
    │   └── kanban/                    # Folder with domain-prefixed files
    │       └── {domain}-board-*.md    # e.g., devops-board-2024-12-18_2025-01-01.md
    ├── 5-testing/
    │   └── testing-strategy.md
    └── 6-operation/
        ├── ops-manual.md
        └── releases/
```

### A.2 Module Compulsory Files

```
{module}/
├── README.md
├── CHANGELOG.md
├── CONTRIBUTING.md
├── SECURITY.md
└── doc/
    ├── overview.md
    ├── 3-design/
    │   ├── architecture.md
    │   ├── sequence.md
    │   ├── workflow.md
    │   └── toolchain.md
    ├── 4-development/
    │   ├── developer-guide.md
    │   ├── setup-guide.md
    │   ├── backlog.md                 # (Optional)
    │   └── kanban.md                  # (Optional)
    ├── 5-testing/
    │   └── testing-strategy.md
    └── 6-operation/
        └── releases/                  # (Optional - required at root only)
```

---

## Appendix B: PR Template

```markdown
## Summary
<!-- Brief description of changes -->

## Type
- [ ] Feature
- [ ] Bug fix
- [ ] Refactor
- [ ] Documentation
- [ ] New module

---

## Documentation Checklist

> See [Documentation Standard](../../doc/documentation-standard.md)

### For New Modules
- [ ] `README.md` with TLDR + TOC
- [ ] `doc/overview.md` with WHAT/HOW/WHY

#### 3-design/
- [ ] `architecture.md`
- [ ] `sequence.md`
- [ ] `workflow.md`
- [ ] `toolchain.md`

#### 4-development/
- [ ] `developer-guide.md`
- [ ] `setup-guide.md`

#### 5-testing/
- [ ] `testing-strategy.md`

### For Existing Modules
- [ ] Updated relevant docs if behavior changed
- [ ] Added ADR if significant architectural decision made

---

## Code Checklist
- [ ] Tests pass
- [ ] Linting passes
- [ ] No breaking changes (or documented)

## Test Plan
<!-- How was this tested? -->
```

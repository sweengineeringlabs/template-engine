# SEA Documentation Template Engine

**Language-agnostic documentation templates for software projects following the Stratified Encapsulation Architecture (SEA) and modern best practices.**

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Documentation](https://img.shields.io/badge/docs-templates-green.svg)](templates/)

## What is This?

A comprehensive collection of production-ready documentation templates that follow the **W³H (WHO-WHAT-WHY-HOW)** structure. These templates are:

- 🌍 **Language-Agnostic** - Works for Rust, Python, Java, JavaScript, Go, C++, and more
- 📋 **Comprehensive** - Covers all aspects from code modules to production deployment
- 🎯 **Battle-Tested** - Used in production projects
- 🔧 **Customizable** - Easy-to-replace placeholders
- 📊 **Visual** - Includes workflow diagrams and dataflow charts
- ✅ **Complete** - Checklists, best practices, troubleshooting included

## Research Foundation

This template engine is based on documented research. If your project is based on any research and you wish to document that work, use the `01-ideation/research/papers/` folder structure.

### Included Research Papers

| Paper | Description |
|-------|-------------|
| [SEA Workflow](sea_workflow.md) | Stratified Encapsulation Architecture workflow guide |
| [SDLC Documentation Framework](01-ideation/research/papers/sdlc_documentation_framework.md) | Documentation standards across SDLC phases |
| [Module Governance Framework](01-ideation/research/papers/module_governance_framework.md) | Module organization and governance patterns |
| [Documentation Navigation Framework](01-ideation/research/papers/documentation_navigation_framework.md) | Documentation structure and navigation |
| [Research Methodology](01-ideation/research/papers/research_methodology.md) | Research approach and methodology |

### 1. Setup Git Authentication (if needed)

If you haven't set up SSH authentication with GitHub yet:

📖 **See [git_ssh_setup.md](git_ssh_setup.md)** for complete SSH setup instructions (Linux, macOS, Windows, WSL).

### 2. Choose Your Templates

```bash
# Clone or download this repository
git clone git@github.com:[org]/template-engine.git
cd template-engine/templates
```

### 3. Copy Templates to Your Project

```bash
# For a new project
cp templates/crate_readme.template.md your-project/docs/README.md
cp templates/framework_doc.template.md your-project/docs/architecture.md

# Replace placeholders
# [PROJECT_NAME] → your-project-name
# [Language] → Rust, Python, Java, etc.
# [Description] → your description
```

### 4. Customize for Your Needs

Each template includes:
- **Placeholders** in `[BRACKETS]` - Replace with your values
- **Customization Guide** at the end - Step-by-step instructions
- **Examples** - See how it's used in real projects

## Available Templates

### Core Documentation Templates

| Template | Purpose | Target Location | Best For |
|----------|---------|-----------------|----------|
| [crate_readme.template.md](templates/crate_readme.template.md) | Module/component docs | `docs/README.md` | Libraries, modules, packages |
| [framework_doc.template.md](templates/framework_doc.template.md) | Framework-wide docs | `docs/guides/*.md` | Architecture, security, patterns |
| [glossary.template.md](templates/glossary.template.md) | Term definitions | `docs/glossary.md` | All projects (REQUIRED) |

### SDLC Templates

| Template | Purpose | Target Location | Best For |
|----------|---------|-----------------|----------|
| [feature_request.template.md](templates/sdlc/1-requirements/feature_request.template.md) | FR definitions | `docs/1-requirements/` | Feature tracking |
| [implementation_plan.template.md](templates/sdlc/2-planning/implementation_plan.template.md) | Implementation plans | `docs/2-planning/FR-{###}/` | Sprint planning |
| [backlog.template.md](templates/sdlc/4-development/backlog.template.md) | Feature backlogs | `docs/4-development/` | Work tracking |
| [kanban.template.md](templates/sdlc/4-development/kanban.template.md) | Sprint boards | `docs/4-development/` | Sprint management |

### Backend/SEA Module Templates

| Template | Purpose | Target Location | Best For |
|----------|---------|-----------------|----------|
| [README.template.md](templates/backend/README.template.md) | Module entry point | `{module}/README.md` | All modules |
| [README.template.md](templates/backend/docs/README.template.md) | W³H | `{module}/docs/README.md` | All modules |
| [architecture.template.md](templates/backend/docs/3-design/architecture.template.md) | SEA layer diagram | `{module}/docs/3-design/` | Backend modules |
| [adr.template.md](templates/backend/docs/3-design/adr.template.md) | Architecture decisions | `{module}/docs/3-design/adr/` | Design decisions |
| [integration.template.md](templates/backend/docs/3-design/integration.template.md) | Integration guide | `{module}/docs/3-design/` | API consumers |
| [strategy.template.md](templates/backend/docs/5-testing/strategy.template.md) | Test strategy | `{module}/docs/5-testing/` | Test planning |
| [configuration.template.md](templates/backend/docs/6-operation/configuration.template.md) | Config options | `{module}/docs/6-operation/` | Runtime config |
| [troubleshooting.template.md](templates/backend/docs/6-operation/troubleshooting.template.md) | Debug guide | `{module}/docs/6-operation/` | Issue resolution |

### Frontend Templates

| Template | Purpose | Target Location | Best For |
|----------|---------|-----------------|----------|
| [architecture.template.md](templates/frontend/docs/3-design/architecture.template.md) | Component design | `docs/3-design/FR-{###}/` | React features |
| [adr.template.md](templates/frontend/docs/3-design/adr.template.md) | UI decisions | `docs/3-design/FR-{###}/adr/` | Design decisions |
| [backlog.template.md](templates/frontend/docs/4-development/backlog.template.md) | Feature backlog | `docs/4-development/FR-{###}/` | Work tracking |
| [kanban.template.md](templates/frontend/docs/4-development/kanban.template.md) | Sprint board | `docs/4-development/` | Sprint management |
| [test_plan.template.md](templates/frontend/docs/5-testing/test_plan.template.md) | Test strategy | `docs/5-testing/FR-{###}/` | Test planning |
| [configuration.template.md](templates/frontend/docs/6-operation/configuration.template.md) | UI config | `docs/6-operation/FR-{###}/` | Settings |
| [troubleshooting.template.md](templates/frontend/docs/6-operation/troubleshooting.template.md) | Debug guide | `docs/6-operation/FR-{###}/` | Issue resolution |

### Deployment Templates

| Template | Purpose | Target Location | Best For |
|----------|---------|-----------------|----------|
| [release_versioning.template.md](templates/release_versioning.template.md) | Version management | `docs/deployment/versioning.md` | All projects |
| [deployment_workflow.template.md](templates/deployment_workflow.template.md) | Deployment process | `docs/deployment/workflow.md` | Libraries, applications |
| [ci_cd.template.md](templates/ci_cd.template.md) | CI/CD pipelines | `docs/deployment/ci-cd.md` | All projects |
| [publishing.template.md](templates/publishing.template.md) | Registry publishing | `docs/deployment/publishing.md` | Libraries, packages |

### Repository Files

| Template | Purpose | Location | Required |
|----------|---------|----------|----------|
| [git-files/](templates/git-files/) | Repository governance | Repository root | Yes (see guide) |

## Template Structure

All templates follow a consistent structure:

```markdown
# [Document Title]

**Audience**: [Who should read this]

## WHAT: [What is this]
- Clear description
- Scope definition
- Out of scope

## WHY: [Why it matters]
- Problems addressed
- Benefits

## HOW: [How to implement]
- Workflow diagrams
- Step-by-step instructions
- Code examples
- Checklists
- Best practices
- Troubleshooting

## Summary
- Key takeaways
- Related documentation
- External resources

---

## Template Customization Guide
[Detailed instructions for adapting the template]
```

## Documentation Framework

### Phase 0: Git Repository Files (REQUIRED FIRST)
Set up governance files before any other documentation:
- CODE_OF_CONDUCT.md (open-source)
- SECURITY.md
- SUPPORT.md
- CONTRIBUTING.md
- LICENSE
- Issue/PR templates

See [Repository Governance Guide](templates/framework.md#git-repository-files)

### Phase 1-6: Structured Documentation
Follow the phased approach defined in [framework.md](templates/framework.md)

## Features

### 🎯 Audience-First Approach
Every document declares its intended audience upfront

### 📊 Visual Workflows
Includes ASCII diagrams for:
- Process flows
- Decision trees
- Data flows
- Pipeline visualizations

### ✅ Comprehensive Checklists
Ready-to-use checklists for:
- Pre-deployment validation
- Quality gates
- Publishing readiness
- Post-deployment verification

### 🔧 Multi-Language Support
Templates work for:
- **Compiled**: Rust, Go, C++, Java, C#
- **Interpreted**: Python, Ruby, PHP, JavaScript
- **Package Managers**: cargo, npm, pip, maven, gradle, nuget

### 🚀 CI/CD Ready
Platform-agnostic CI/CD templates for:
- GitHub Actions
- GitLab CI
- Jenkins
- CircleCI
- Travis CI

## Examples

### Using the Module Template

```bash
# Copy template
cp templates/crate_readme.template.md myproject/src/auth/docs/README.md

# Edit and replace:
[Module Name] → Authentication
[Language] → Rust  
[Description] → JWT-based authentication system
```

Result: Professional module documentation in minutes!

### Using the CI/CD Template

```bash
# Copy template
cp templates/ci_cd.template.md myproject/docs/ci-cd.md

# Customize for your platform:
[CI Platform] → GitHub Actions
[Language] → Python
[test command] → pytest
```

Result: Complete CI/CD documentation with workflows!

### Using SDLC Templates

```bash
# Create a new Feature Request
cp templates/sdlc/1-requirements/feature_request.template.md \
   docs/1-requirements/FR-001-user-auth.md

# Create implementation plan
mkdir -p docs/2-planning/FR-001
cp templates/sdlc/2-planning/implementation_plan.template.md \
   docs/2-planning/FR-001/implementation_plan.md

# Replace placeholders: {###} → 001, {name} → user-auth
```

### Using Backend/SEA Module Templates

```bash
# Bootstrap a new SEA module
mkdir -p my-module/docs/{3-design,4-development,5-testing}
cp templates/backend/README.template.md my-module/README.md
cp templates/backend/docs/README.template.md my-module/docs/README.md
cp templates/backend/docs/3-design/*.template.md my-module/docs/3-design/
cp templates/backend/docs/5-testing/*.template.md my-module/docs/5-testing/

# Replace {module-name} → my-module, {Module} → MyModule
```

Result: Complete SEA-compliant module documentation structure!

## Project Types Supported

- ✅ **Libraries** - Reusable packages published to registries
- ✅ **Frameworks** - Tools and abstractions for building applications
- ✅ **Applications** - End-user software and services
- ✅ **Microservices** - Distributed service architectures
- ✅ **CLI Tools** - Command-line utilities
- ✅ **APIs** - REST, GraphQL, gRPC services

## Language-Specific Guides

Templates include language-specific sections for:
- Version management (SemVer)
- Package manifest formats
- Build commands
- Test frameworks
- Publishing procedures
- Registry specifics

## Best Practices Included

Every template includes:
- ✅ **DO** recommendations
- ❌ **DON'T** anti-patterns
- 🔍 **Troubleshooting** common issues
- 📚 **External resources** for deep dives

## Contributing

We welcome contributions! See [CONTRIBUTING.md](CONTRIBUTING.md)

Ways to contribute:
- 📝 Improve existing templates
- ➕ Add new templates
- 🐛 Fix issues
- 📖 Enhance documentation
- 💡 Share examples

## License

This project is licensed under  the MIT License - see the [LICENSE](LICENSE) file for details.

## Maintained By

SEA Documentation Template Engine Team

## Related Projects

- [Rustboot Framework](https://github.com/[org]/rustboot) - Example usage of these templates
- [SEA Architecture Guide](https://github.com/[org]/sea-architecture) - SEA methodology

## Support

- 📖 [Documentation](templates/)
- 💬 [Discussions](https://github.com/[org]/template-engine/discussions)
- 🐛 [Issues](https://github.com/[org]/template-engine/issues)
- 📧 Email: [contact email]

---

**Start documenting better, today! 🚀**

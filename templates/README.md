# Documentation Templates

This directory contains language-agnostic templates for comprehensive software documentation.

## Quick Reference

### Module/Component Documentation
- **[crate_readme.template.md](crate_readme.template.md)** - Module and component documentation

### Framework Documentation
- **[framework_doc.template.md](framework_doc.template.md)** - Framework-wide documentation (architecture, security, patterns)
- **[framework.md](framework.md)** - Complete documentation framework guide

### Deployment & Operations Documentation
- **[release_versioning.template.md](release_versioning.template.md)** - Version management and SemVer
- **[deployment_workflow.template.md](deployment_workflow.template.md)** - Deployment strategies and processes
- **[ci_cd.template.md](ci_cd.template.md)** - CI/CD pipeline configuration
- **[publishing.template.md](publishing.template.md)** - Package registry publishing
- **[sdlc/7-operation/filesystem_paths.template.md](sdlc/7-operation/filesystem_paths.template.md)** - XDG Base Directory compliant file storage paths

### Planning & Proposals

- **[sdlc/2-planning/rfc.template.md](sdlc/2-planning/rfc.template.md)** - Request for Comments (pre-decision proposals that graduate to ADRs)
- **[sdlc/lifecycle.md](sdlc/lifecycle.md)** - SDLC document lifecycle: how Idea → FR → RFC → ADR → Architecture flows

### Bug Reporting & Issue Management
- **[sdlc/4-development/bug_reporting_strategy.template.md](sdlc/4-development/bug_reporting_strategy.template.md)** - Bug reporting strategy (developer/contributor view)
- **[sdlc/7-operation/bug_reporting_strategy.template.md](sdlc/7-operation/bug_reporting_strategy.template.md)** - Bug reporting strategy (operations/SRE view)

### Compliance
- **[compliance-checklist.md](compliance-checklist.md)** - 56-point documentation audit checklist
- **[backend/docs/3-design/compliance/compliance_checklist.template.md](backend/docs/3-design/compliance/compliance_checklist.template.md)** - Architecture compliance checklist template (REQUIRED per project)

### Repository Files
- **[git-files/](git-files/)** - Git repository governance files (coming soon)

## How to Use

1. **Choose a template** based on what you're documenting
2. **Copy it** to your project's documentation directory
3. **Replace placeholders** marked with `[BRACKETS]`
4. **Follow the customization guide** at the end of each template
5. **Remove meta instructions** before publishing

## Template Structure

Each template follows the W³H (WHO-WHAT-WHY-HOW) structure:

```
# Title
**Audience**: [Who should read this]

## WHAT: [Description]
## WHY: [Motivation and benefits]
## HOW: [Implementation]
  - Workflows/Diagrams
  - Instructions
  - Examples
  - Checklists
  - Best practices

## Summary
## Template Customization Guide
```

## Placeholder Convention

Templates use this placeholder format:
- `[PROJECT_NAME]` - Your project name
- `[Language]` - Programming language (Rust, Python, etc.)
- `[Description]` - Your description
- `YYYY-MM-DD` - Dates
- `[command]` - Commands specific to your tools
- `[X.Y.Z]` - Version numbers

## Support

For issues or questions about templates:
- See individual template customization guides
- Check [framework.md](framework.md) for overall guidance
- Open an issue on GitHub

---

**Happy Documenting! 📚**

# ISO/IEC/IEEE Standards Reference

**Audience**: Architects, documentation maintainers

## Overview

Three ISO/IEC/IEEE standards map to specific SDLC phases in the template-engine documentation framework. Each standard defines structure, attributes, and traceability expectations for its document type.

## Standards Comparison

| Aspect | ISO/IEC/IEEE 29148:2018 | ISO/IEC/IEEE 42010:2022 | ISO/IEC/IEEE 29119-3:2021 |
|--------|-------------------------|-------------------------|---------------------------|
| **Domain** | Requirements engineering | Architecture description | Test documentation |
| **SDLC Phase** | 1-requirements | 3-design | 5-testing |
| **Primary artifact** | `requirements.md` (SRS) | `architecture.md` | `testing_strategy.md` |
| **Key concept** | Every requirement is a traceable, verifiable artifact | Architecture described through stakeholders, concerns, and viewpoints | Test documentation through design, cases, and procedures |
| **Required sections** | Priority, State, Verification, Traceability, Acceptance per requirement | Stakeholders, Concerns, Viewpoints, Architecture decisions | Test design specification, Test cases, Test procedures |
| **Traceability** | Bidirectional: stakeholder needs -> system -> software -> test | Viewpoints address stakeholder concerns | Test cases trace to requirements |
| **Lifecycle** | Requirements have states (proposed -> approved -> verified) | Views evolve with architecture decisions | Test procedures have entry/exit criteria |
| **Supersedes** | IEEE 830-1998 | IEEE 1471-2000 | IEEE 829-2008 |

## Mapping to template-engine

| Standard | Framework Section | Template File | doc-engine Check |
|----------|-------------------|---------------|------------------|
| 29148:2018 | §5 (architecture section note) | `sdlc/1-requirements/` | Check 89: `srs_29148_attributes` |
| 42010:2022 | §5 (architecture section note) | `sdlc/3-design/architecture.template.arch` | Check 90: `arch_42010_sections` |
| 29119-3:2021 | §10 (testing strategy section) | `sdlc/5-testing/testing_strategy.template.md` | Check 91: `test_29119_sections` |

## How Each Standard Applies

### ISO/IEC/IEEE 29148:2018 — Requirements

The template-engine framework already follows 29148 structure. Each requirement block (FR-xxx, NFR-xxx) includes the five mandatory attributes:

- **Priority** — MoSCoW classification
- **State** — lifecycle state (Proposed, Approved, Verified)
- **Verification** — method (Test, Inspection, Analysis, Demonstration)
- **Traces to** — bidirectional traceability to stakeholders and architecture
- **Acceptance** — measurable acceptance criteria

See also: [IEEE 830 vs ISO 29148](ieee_830_vs_iso_29148.md)

### ISO/IEC/IEEE 42010:2022 — Architecture

42010 structures architecture descriptions around three concepts:

1. **Stakeholders** — who has interest in the architecture (developers, architects, operations)
2. **Concerns** — what matters to stakeholders (modularity, performance, security)
3. **Viewpoints** — perspectives that address concerns (structural, behavioral, deployment)

The W3H structure (Who/What/Why/How) in template-engine architecture docs naturally maps to 42010: Who=Stakeholders, What=Views, Why=Concerns, How=Viewpoints.

### ISO/IEC/IEEE 29119-3:2021 — Test Documentation

29119-3 defines three levels of test documentation:

1. **Test Design Specification** — strategy, scope, entry/exit criteria
2. **Test Case Specification** — individual test cases with traceability to requirements
3. **Test Procedure Specification** — execution procedures, environments, ordering

The template-engine testing strategy template maps directly: Test Pyramid -> design, Test Categories -> cases, Coverage Targets -> exit criteria, CI Pipeline -> procedures.

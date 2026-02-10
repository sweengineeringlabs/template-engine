# Standards Reference

**Audience**: Architects, documentation maintainers

## Overview

Ten standards and guidelines map to specific SDLC phases in the template-engine documentation framework: eight ISO/IEC/IEEE standards, one IEEE standard, and one PMI guide. Each defines structure, attributes, and traceability expectations for its document type.

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

| Standard | Framework Section | Template File | doc-engine Checks |
|----------|-------------------|---------------|-------------------|
| 29148:2018 | §5 (requirements) | `sdlc/1-requirements/` | 89: `srs_29148_attributes`, 118: ConOps, 119: StRS, 120: traceability matrix |
| 42010:2022 | §5 (architecture) | `sdlc/3-design/architecture.template.arch` | 90: `arch_42010_sections` |
| 29119-3:2021 | §10 (testing strategy) | `sdlc/5-testing/testing_strategy.template.md` | 91: `test_29119_sections`, 100: test design, 101: test cases |
| 12207:2017 | Cross-phase (lifecycle) | All SDLC phases | 92, 96: production readiness, 109-113: planning artifacts, 120-122: traceability/progress/decisions |
| 15289:2019 | Cross-phase (info items) | All SDLC phases | 99, 102-117: phase artifacts, 121-123: progress reports/decision log/audit report |
| 26514:2022 | §4 (user info) | `sdlc/4-development/`, `sdlc/6-deployment/` | 94: `dev_guide_26514_sections` |
| 25010:2023 | §6 (quality) | `sdlc/6-deployment/production_readiness` | 93, 97: product quality sections |
| 25040:2024 | §6 (evaluation) | `sdlc/6-deployment/production_readiness` | 98: evaluation process sections |
| IEEE 1028 | Cross-phase (audits) | `sdlc/2-planning/` | 123: audit report |
| PMBOK (PMI) | §2 (planning) | `sdlc/2-planning/` | 85: schedule, 86: resource plan, 87: communication plan |

## How Each Standard Applies

### ISO/IEC/IEEE 29148:2018 — Requirements

The template-engine framework already follows 29148 structure. Each requirement block (FR-xxx, NFR-xxx) includes the five mandatory attributes:

- **Priority** — MoSCoW classification (Must / Should / Could / Won't)
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

### ISO/IEC/IEEE 12207:2017 — Software Life Cycle Processes

12207 is the foundational lifecycle standard defining process areas for software systems. doc-engine enforces its requirements through planning, traceability, and phase artifact checks across the entire SDLC. Key process areas: project planning (56, 85-87, 109), assessment and control (92, 96, 121), decision management (122), risk management (111), and configuration management (110).

### ISO/IEC/IEEE 15289:2019 — Content of Life-Cycle Information Items

15289 defines content requirements for documentation artifacts produced throughout the software lifecycle. doc-engine checks file existence for all phase artifacts (60-68, 99-117), plus cross-phase items: progress/status reports (121), decision log (122), and audit report (123).

### ISO/IEC/IEEE 26514:2022 — Information for Users

26514 defines the design and development of information for software users. doc-engine validates developer guide structure (94) against task analysis, information structure, and writing guidelines.

### ISO/IEC 25010:2023 — Product Quality Model (SQuaRE)

25010 defines the product quality model with quality characteristics. doc-engine validates production readiness documents (93, 97) for security, reliability, maintainability, portability, and usability sections.

### ISO/IEC 25040:2024 — Evaluation Process (SQuaRE)

25040 defines the evaluation process. doc-engine validates that production readiness documents (98) contain scoring criteria and sign-off sections for evaluation conclusion.

### IEEE 1028 — Software Reviews and Audits

IEEE 1028 defines processes for software reviews and audits, including management reviews, technical reviews, inspections, walk-throughs, and audits. doc-engine checks for the existence of an audit report artifact (123) per clause 4 (audit process).

### PMBOK — Project Management Body of Knowledge (PMI)

PMBOK is a guide published by the Project Management Institute (PMI), not an ISO/IEC/IEEE standard. It describes best practices for project management across knowledge areas: scope, schedule, cost, quality, resource, communication, risk, procurement, and stakeholder management. doc-engine checks for three PMBOK-inspired planning artifacts: schedule (85), resource plan (86), and communication plan (87). These align with PMBOK knowledge areas 6 (Schedule Management), 9 (Resource Management), and 10 (Communications Management). PMBOK aligns with ISO 21500:2021 (Guidance on project management).

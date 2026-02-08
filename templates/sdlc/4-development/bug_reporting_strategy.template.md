# {Project Name} Bug Reporting Strategy

**Audience**: Developers, contributors, testers

## Version

| Field        | Value                     |
|--------------|---------------------------|
| Version      | {0.1.0}                   |
| Status       | {Draft | Approved | Superseded} |
| Last Updated | {YYYY-MM-DD}              |
| Owner        | {owner}                   |

## Overview

{1-2 paragraph description of how bugs are reported, categorized, triaged, and
tracked through resolution. Reference the issue tracker and any automated
compliance tooling that generates issues.}

## Bug Severity Classification

| Severity | Label | Definition | Examples |
|----------|-------|------------|----------|
| **S0 - Critical** | `severity/critical` | {System unusable, data loss, security vulnerability} | {production crash, authentication bypass, data corruption} |
| **S1 - High** | `severity/high` | {Major feature broken, no workaround available} | {API returns wrong results, CLI command fails on valid input} |
| **S2 - Medium** | `severity/medium` | {Feature impaired but workaround exists} | {incorrect output format, slow performance under load} |
| **S3 - Low** | `severity/low` | {Minor issue, cosmetic, or edge case} | {typo in output, UI misalignment, rare edge case} |

## Priority Classification

Priority is assigned during triage and determines scheduling. Priority may differ
from severity based on impact scope and strategic importance.

| Priority | Label | SLA: Acknowledge | SLA: Fix Target | Scheduling |
|----------|-------|-------------------|-----------------|------------|
| **P0** | `priority/P0` | {< 4 hours} | {< 24 hours} | Drop current work |
| **P1** | `priority/P1` | {< 1 business day} | {Current sprint} | Schedule this sprint |
| **P2** | `priority/P2` | {< 3 business days} | {Next 2 sprints} | Schedule when capacity allows |
| **P3** | `priority/P3` | {< 1 week} | {Backlog} | Address opportunistically |

## Label Taxonomy

### Required Labels (Applied at Creation)

| Label | Purpose |
|-------|---------|
| `bug` | Issue is a defect (vs `enhancement`, `documentation`, `question`) |
| `triage` | Awaiting triage, removed after severity/priority assigned |

### Assigned During Triage

| Category | Labels | Purpose |
|----------|--------|---------|
| Severity | `severity/critical`, `severity/high`, `severity/medium`, `severity/low` | Impact classification |
| Priority | `priority/P0`, `priority/P1`, `priority/P2`, `priority/P3` | Scheduling classification |
| Component | {`component/{name}` per module or subsystem} | Affected subsystem |

### Lifecycle Labels

| Label | Meaning |
|-------|---------|
| `needs-reproduction` | Cannot reproduce, awaiting reporter input |
| `confirmed` | Reproduced and accepted |
| `blocked` | Waiting on external dependency or decision |
| `regression` | Worked in a previous version |
| `duplicate` | Duplicate of another issue (link original and close) |
| `wontfix` | Intentional behaviour or out of scope |

## Bug Lifecycle

```
Reported ──> Triage ──> Confirmed ──> Assigned ──> In Progress ──> In Review ──> Resolved ──> Closed
   │            │           │                                                       │
   │            ├─> needs-reproduction ──> (reporter responds) ──> Triage            │
   │            ├─> duplicate ──> Closed                                             │
   │            └─> wontfix ──> Closed                                               │
   │                                                                                 │
   └─────────────────────────────── Reopened (if fix insufficient) <─────────────────┘
```

### State Definitions

| State | Description | Owner |
|-------|-------------|-------|
| **Reported** | Issue created via template, `bug` + `triage` labels auto-applied | Reporter |
| **Triage** | Maintainer reviews, assigns severity/priority/component, removes `triage` label | {Triage owner: maintainer on rotation | project lead} |
| **Confirmed** | Bug reproduced, `confirmed` label applied | Triager |
| **Assigned** | Developer assigned, sprint/backlog placement decided | {Triage owner} |
| **In Progress** | Developer working on fix, branch created | Assignee |
| **In Review** | PR submitted, linked to issue | Assignee + Reviewer |
| **Resolved** | PR merged, fix deployed or released | Assignee |
| **Closed** | Verified by reporter or automated test, issue closed | Reporter or CI |

## Triage Process

### Triage Cadence

- **P0/P1**: Triage immediately upon report
- **P2/P3**: Triage during {scheduled triage session: daily standup | weekly review}

### Triage Checklist

For each new bug (labelled `triage`):

1. [ ] **Reproduce**: Verify the bug using the provided steps
2. [ ] **Classify severity**: Assign `severity/*` label
3. [ ] **Classify priority**: Assign `priority/*` label based on severity + impact scope
4. [ ] **Assign component**: Add `component/*` label
5. [ ] **Check for duplicates**: Search existing issues, close if duplicate
6. [ ] **Check for regression**: If worked before, add `regression` label and identify regressing commit
7. [ ] **Assign owner**: Assign to developer or leave unassigned for backlog
8. [ ] **Remove `triage` label**

### Triage Decision Matrix

| Severity | Scope: Single User | Scope: Many Users | Scope: All Users |
|----------|--------------------|--------------------|------------------|
| S0 | P1 | P0 | P0 |
| S1 | P2 | P1 | P0 |
| S2 | P3 | P2 | P1 |
| S3 | P3 | P3 | P2 |

## Bug Report Requirements

### Minimum Required Fields

All bug reports must include (enforced by issue template):

| Field | Purpose |
|-------|---------|
| **Description** | Clear, concise description of the bug |
| **Steps to Reproduce** | Numbered steps to reliably reproduce |
| **Expected Behavior** | What should happen |
| **Actual Behavior** | What actually happens |
| **Environment** | OS, version, relevant configuration |

### Recommended Fields

| Field | When Required |
|-------|---------------|
| **Logs** | When error output is available |
| **Configuration** | When non-default configuration may be involved |
| **Screenshots** | For UI or output formatting issues |
| **Regression info** | When issue appeared after an update (include last working version) |

### Reproduction Quality

| Quality | Definition | Triage Action |
|---------|------------|---------------|
| **Reproducible** | Steps reliably trigger the bug | Proceed with fix |
| **Intermittent** | Occurs sometimes but not reliably | Investigate timing/concurrency |
| **Unreproducible** | Cannot reproduce with given steps | Label `needs-reproduction`, request more detail |

## Audit-Generated Issues

{When automated compliance tools (e.g., doc-engine, linters, CI checks) generate
findings, they follow this process:}

### Compliance Audit to Issue Mapping

| Audit Source | Issue Type | Template |
|---|---|---|
| {doc-engine scan} | Documentation compliance | Single issue per audit run with findings checklist |
| {cargo clippy} | Code quality | One issue per warning category |
| {cargo test failures} | Test regression | One issue per failing test suite |
| {security scan} | Security vulnerability | One issue per CVE, label `severity/critical` or `severity/high` |

### Audit Issue Format

Audit-generated issues should include:

1. **Audit tool and version** that produced the findings
2. **Run date and branch** audited
3. **Summary scorecard** (pass/fail counts)
4. **Itemized findings** grouped by category
5. **Recommended fix order** (prioritized by impact)
6. **Acceptance criteria** (what "fixed" looks like)

## Metrics

| Metric | Measurement | Target |
|--------|-------------|--------|
| Mean time to triage | Time from report to severity/priority assignment | {< 1 business day} |
| Mean time to resolve | Time from report to PR merged | {< 5 business days for P1} |
| Bug reopen rate | Percentage of resolved bugs reopened | {< 10%} |
| Triage backlog | Number of issues with `triage` label | {< 5 at any time} |

## Related Documents

### Requirements
- [Business Requirements](../1-requirements/brd.spec)

### Design
- [System Architecture](../3-design/architecture.arch)

### Development
- [Developer Guide](../4-development/developer_guide.md)
- [Backlog](../4-development/backlog.md)

### Testing
- [Testing Strategy](../5-testing/testing_strategy.md)

### Operations
- [Bug Reporting Strategy (Operations View)](../7-operation/bug_reporting_strategy.md)
- [Operations Manual](../7-operation/ops_manual.md)

---

<!--
CUSTOMISATION GUIDE
===================
1. Replace all {placeholders} with project-specific values.
2. Adjust severity definitions to match your project's impact model.
3. Adjust SLAs to match your team's capacity and commitments.
4. Add project-specific component labels to the Label Taxonomy.
5. Add project-specific audit tools to the Audit-Generated Issues section.
6. Remove this comment block before publishing.
-->

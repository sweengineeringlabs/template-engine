# SDLC Document Lifecycle

**Audience**: Architects, technical leads, contributors

> **TLDR**: Documents in this framework follow a defined lifecycle across SDLC phases. Each document type has a specific creation trigger, a home phase, and a defined graduation path. This document maps those relationships so contributors know where a document starts, where it lives, and what it produces.

---

## Document Types by Phase

| Document | Phase | Folder | Creation Trigger | Graduates To |
|----------|-------|--------|------------------|--------------|
| Idea | 0 | `0-ideation/` | Observation, user feedback, research | Feature Request |
| Feature Request (FR) | 1 | `1-requirements/` | Accepted idea | RFC (complex) or ADR (simple) |
| RFC | 2 | `2-planning/rfc/` | Significant proposed change requiring consensus | ADR (if accepted); archived in place (if rejected) |
| Implementation Plan | 2 | `2-planning/` | Accepted FR with known approach | — |
| ADR | 3 | `3-design/adr/` | Accepted RFC, or direct design decision | Architecture doc update |
| Architecture | 3 | `3-design/` | ADR, initial design work | Compliance checklist |
| Compliance Checklist | 3 | `3-design/compliance/` | Architecture doc exists | — |

---

## Lifecycle Flow

```
0-ideation/
└── idea.md
        │
        │  accepted idea
        ▼
1-requirements/
└── FR_{###}_{name}.md            ← Feature Request
        │
        │  complex or cross-cutting change?
        ├─ YES ──────────────────────────────────────┐
        │                                            ▼
        │                               2-planning/rfc/
        │                               └── NNN-{title}.md   ← RFC
        │                                            │
        │                           ┌────────────────┴──────────────────┐
        │                      accepted                              rejected
        │                           │                                   │
        │                           │                     stays in rfc/ as
        │                           │                     closed record
        │                           ▼
        │  simple / direct      3-design/adr/
        └─ NO ─────────────────►└── NNN-{title}.md          ← ADR
                                                │
                                                │  decision implemented
                                                ▼
                                3-design/
                                └── architecture.md           ← Architecture doc updated
                                                │
                                                ▼
                                3-design/compliance/
                                └── compliance_checklist.md   ← Checklist derived from arch
```

---

## RFC Lifecycle

An RFC (Request for Comments) is a **pre-decision proposal**. It exists to collect
consensus before a design decision is committed. Use an RFC when:

- The change is significant enough to warrant discussion before implementation
- Multiple valid approaches exist and the tradeoffs need to be evaluated publicly
- The change affects public API, architectural boundaries, or cross-cutting conventions

**Status progression**:

```
Proposed → Accepted → ADR created → RFC closed (Accepted)
Proposed → Rejected → RFC closed (Rejected, reason recorded)
Proposed → Withdrawn → RFC closed (author retracted)
Proposed → Superseded by RFC-{###} → RFC closed
```

**Naming**: `NNN-{decision-title}.md` (zero-padded, same convention as ADRs)

**Rejected RFCs are not deleted.** They remain in `2-planning/rfc/` as a record of
what was considered and why it was not pursued — preventing the same proposal from
being re-raised without new evidence.

---

## ADR Lifecycle

An ADR (Architecture Decision Record) records a **committed decision**. It is the
output of an accepted RFC, or the direct record of a decision made without a formal
RFC process (when the decision is straightforward).

**Status progression**:

```
Proposed → Accepted → implemented
Accepted → Deprecated → superseded by newer ADR
Accepted → Superseded by ADR-{###}
```

**Naming**: `NNN-{decision-title}.md` (zero-padded, under `docs/3-design/adr/`)

---

## When to Use RFC vs ADR Directly

| Situation | Use |
|-----------|-----|
| Significant architectural change, multiple stakeholders | RFC → ADR |
| Change to public API or cross-cutting conventions | RFC → ADR |
| Straightforward design choice, single owner | ADR directly |
| Reverting or superseding an existing ADR | RFC → new ADR |
| Implementation detail within an already-decided architecture | ADR directly |

---

## Document Naming Conventions

| Document | Naming Pattern | Example |
|----------|----------------|---------|
| Feature Request | `FR_{###}_{name}.md` | `FR_501_auth_flow.md` |
| RFC | `NNN-{decision-title}.md` | `001-reactive-runtime.md` |
| ADR | `NNN-{decision-title}.md` | `001-crate-organization.md` |
| Implementation Plan | `{FR}_{name}_plan.md` | `FR_501_auth_flow_plan.md` |

Numbers are zero-padded to three digits for consistent sort order.

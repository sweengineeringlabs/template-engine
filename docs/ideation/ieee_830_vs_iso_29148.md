# IEEE 830-1998 vs ISO/IEC/IEEE 29148:2018

**Audience**: Architects, documentation maintainers

| Aspect | IEEE 830-1998 | ISO/IEC/IEEE 29148:2018 |
|---|---|---|
| Status | Superseded | Current active standard |
| Scope | Software requirements only | Full requirements engineering lifecycle (StRS -> SyRS -> SRS) |
| Document structure | Rigid prescribed outline (sections 1-5) | Flexible — provides templates, not mandates |
| Requirement granularity | Sections of prose | Each requirement is an individual artifact with attributes |
| Attributes per requirement | ID, description | ID, description, priority, stability, verification method, rationale, source, state |
| Traceability | Encouraged but informal | First-class — bidirectional trace from stakeholder needs -> system -> software -> test |
| Verification | Not specified per requirement | Every requirement must state how it's verified (test/inspection/analysis/demonstration) |
| Stakeholder context | Brief "user characteristics" section | Dedicated Stakeholder Requirements Specification (StRS) with ConOps |
| Use cases | Not part of the standard | Integrated — operational scenarios / use cases are expected |
| Agile compatibility | Poor — assumes waterfall big-up-front doc | Better — requirements can live in backlog items with 29148 attributes |
| Risk | Not addressed | Requirements linked to risk analysis |
| Acceptance criteria | Not formalized | Expected per requirement |
| Maintenance | Static document | Requirements have lifecycle states (proposed -> approved -> verified -> deleted) |

**In short**: 830 is a document template ("fill in these sections"). 29148 is a requirements engineering process ("every requirement is a traceable, verifiable, prioritized artifact").

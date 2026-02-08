# {Project Name} Bug Reporting Strategy (Operations)

**Audience**: Operators, DevOps, SREs, support staff

## Version

| Field        | Value                     |
|--------------|---------------------------|
| Version      | {0.1.0}                   |
| Status       | {Draft | Approved | Superseded} |
| Last Updated | {YYYY-MM-DD}              |
| Owner        | {owner}                   |

## Overview

{1-2 paragraph description of how production bugs are detected, escalated, and
reported by operations staff. This document covers the operational perspective:
monitoring-triggered incidents, user-reported issues, and the hand-off from
operations to the development triage process.}

## Incident to Bug Report Flow

```
Monitoring Alert ──> On-Call Acknowledges ──> Investigate ──> Bug Report Filed ──> Dev Triage
        │                                          │
User Report ────> Support Acknowledges ─────> Investigate ──> Bug Report Filed ──> Dev Triage
        │                                          │
        └──> Known Issue? ──> Link existing issue ─┘
```

### When to File a Bug Report

| Scenario | Action |
|----------|--------|
| Alert fires for a known issue | Link to existing issue, add comment with new occurrence data |
| Alert fires for a new issue | File bug report, include alert details and investigation notes |
| User reports a problem | Verify the report, file bug report if not a known issue |
| Degraded performance detected | File bug report if degradation exceeds thresholds for > {5 minutes} |
| Deployment introduces a regression | File bug report with `regression` label, include deploy version |

## Severity Classification (Operational View)

| Severity | Service Impact | User Impact | Monitoring Signal |
|----------|---------------|-------------|-------------------|
| **S0 - Critical** | {Service down or data loss} | {All users affected} | {Health check failing, error rate > 50%} |
| **S1 - High** | {Major feature unavailable} | {Many users affected} | {Error rate > 10%, latency p99 > SLA} |
| **S2 - Medium** | {Feature degraded, workaround exists} | {Some users affected} | {Elevated error rate, intermittent failures} |
| **S3 - Low** | {Cosmetic or minor impact} | {Minimal user impact} | {Warning-level alerts, log anomalies} |

## Escalation Matrix

| Severity | First Responder | Escalation Path | Communication Channel | Status Update Cadence |
|----------|----------------|-----------------|----------------------|----------------------|
| **S0** | {On-call engineer} | {On-call → Team lead → Engineering manager} | {Incident channel + stakeholder notification} | {Every 30 minutes} |
| **S1** | {On-call engineer} | {On-call → Team lead} | {Team channel} | {Every 2 hours} |
| **S2** | {On-call engineer} | {Triage queue} | {Issue tracker} | {Daily during triage} |
| **S3** | {Next available engineer} | {Backlog} | {Issue tracker} | {Sprint review} |

## Operational Bug Report Template

When filing a bug report from an operational context, include the following
additional information beyond the standard bug report fields:

### Required Operational Context

| Field | Description |
|-------|-------------|
| **Detection method** | How was this discovered? (monitoring alert, user report, routine check) |
| **Alert name/ID** | Link to the monitoring alert that triggered investigation |
| **Impact start time** | When the issue was first detected (UTC) |
| **Impact duration** | How long the issue persisted before mitigation |
| **Affected environment** | Production, staging, specific region/cluster |
| **Affected version** | Deployed version at time of incident |
| **User impact estimate** | Number or percentage of users affected |
| **Mitigation applied** | Any temporary fix applied (restart, rollback, config change) |

### Operational Bug Report Example

```markdown
**Detection method**: Monitoring alert `{alert-name}` fired at {timestamp}
**Impact start**: {YYYY-MM-DD HH:MM UTC}
**Impact duration**: {N minutes} (mitigated at {timestamp}, root cause pending)
**Affected environment**: {production | staging | region}
**Affected version**: {version}
**User impact**: ~{N} users / {N}% of traffic
**Mitigation**: {Restarted service | Rolled back to version X | Applied config workaround}

**Description**: {What happened from the operator's perspective}

**Timeline**:
- {HH:MM} - Alert fired: {alert details}
- {HH:MM} - On-call acknowledged
- {HH:MM} - Investigation began, found {observation}
- {HH:MM} - Mitigation applied: {action}
- {HH:MM} - Service restored

**Logs**: {Relevant log snippets}
**Metrics**: {Links to dashboards or metric snapshots}
```

## Known Issues Register

Maintain a running list of known issues that operators may encounter. This
prevents duplicate bug reports and provides immediate workaround guidance.

| ID | Summary | Severity | Workaround | Tracking Issue | Status |
|----|---------|----------|------------|----------------|--------|
| KI-001 | {known issue summary} | S{0-3} | {workaround steps} | {#issue-number} | {Open / Fix in progress / Fixed in vX.Y.Z} |
| KI-002 | {known issue summary} | S{0-3} | {workaround steps} | {#issue-number} | {Open / Fix in progress / Fixed in vX.Y.Z} |

## Post-Incident Process

After an S0 or S1 incident is resolved:

1. [ ] **Bug report filed** with full operational context
2. [ ] **Known Issues Register updated** (if applicable)
3. [ ] **Post-mortem scheduled** within {48 hours} for S0, {1 week} for S1
4. [ ] **Monitoring gap identified** — should this have been caught sooner?
5. [ ] **Runbook updated** — add resolution steps for future occurrences
6. [ ] **Alerting reviewed** — adjust thresholds if alert was too late or too noisy

### Post-Mortem Template (Brief)

| Field | Value |
|-------|-------|
| Incident date | {YYYY-MM-DD} |
| Duration | {N hours/minutes} |
| Severity | S{0-3} |
| Root cause | {1-2 sentences} |
| Fix | {Link to PR or issue} |
| Detection gap | {What monitoring missed, if anything} |
| Prevention | {What changes prevent recurrence} |

## Monitoring Integration

### Alert-to-Issue Automation

{Describe any automation that creates or updates issues from monitoring alerts.}

| Alert Source | Automation | Issue Action |
|---|---|---|
| {monitoring tool} | {webhook / integration name} | {Create issue with `bug` + `severity/*` labels} |
| {log aggregator} | {pattern match rule} | {Create issue if error count > threshold} |
| {CI pipeline} | {test failure notification} | {Create issue with `regression` label} |

### Dashboard Links

| Dashboard | URL | Purpose |
|-----------|-----|---------|
| {Service health} | {url} | Overall service status |
| {Error rates} | {url} | Error rate trends |
| {Latency} | {url} | Response time percentiles |
| {Bug metrics} | {url} | Open bug counts by severity |

## Related Documents

### Development
- [Bug Reporting Strategy (Development View)](../4-development/bug_reporting_strategy.md)
- [Developer Guide](../4-development/developer_guide.md)

### Testing
- [Testing Strategy](../5-testing/testing_strategy.md)

### Operations
- [Operations Manual](../7-operation/ops_manual.md)
- [Runbook](../7-operation/runbook.ops)
- [Troubleshooting](../7-operation/troubleshooting.md)

---

<!--
CUSTOMISATION GUIDE
===================
1. Replace all {placeholders} with project-specific values.
2. Adjust escalation matrix to match your team structure and on-call rotation.
3. Populate the Known Issues Register with current known issues.
4. Add monitoring tool-specific automation details.
5. Link to actual dashboards and alert configurations.
6. Remove this comment block before publishing.
-->

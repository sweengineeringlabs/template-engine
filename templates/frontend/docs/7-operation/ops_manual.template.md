# {Module Name} Operations Manual

**FR:** [FR-{###}](../../../../docs/1-requirements/FR-{###}-{name}.md)

## Overview

Operational procedures for running and maintaining {module-name} in production.

## Health Checks

| Check | Endpoint / Command | Expected Result |
|-------|--------------------|-----------------|
| {check_name} | `{command_or_url}` | {expected} |

## Monitoring

| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| `{metric_name}` | {description} | {threshold} |

## Runbooks

### {Runbook: Common Scenario}

**Trigger:** {when to execute this runbook}

**Steps:**
1. {step_1}
2. {step_2}
3. {step_3}

**Rollback:**
- {rollback_procedure}

## Logging

| Log Level | When Used | Example |
|-----------|-----------|---------|
| `error` | Unrecoverable failures | {example} |
| `warn` | Degraded operation | {example} |
| `info` | Normal operations | {example} |
| `debug` | Development troubleshooting | {example} |

## See Also

- [Configuration](../6-deployment/configuration.md)
- [Troubleshooting](../6-deployment/troubleshooting.md)
- [Overview](../README.md)

# Alderly Robotics Engineering Runbook

## Deployment Process

### Standard Deploys

All production deploys go through the CI/CD pipeline and require at least
one approving code review plus a passing test suite. Deploys are allowed
Monday through Thursday, 9am-4pm local time, to ensure on-call coverage.

### Emergency Hotfixes

A hotfix may bypass the standard deploy window with sign-off from the
on-call Engineering Manager. Every hotfix must be followed by a retroactive
pull request review within 24 hours.

## On-Call Rotation

Engineers are on-call for one week at a time, in a rotation of 8 engineers.
The on-call engineer carries the primary pager and must acknowledge a page
within 15 minutes during business hours and 30 minutes outside business
hours.

## Incident Response

### Severity Levels

Incidents are classified SEV1 through SEV4. SEV1 means full production
outage affecting all customers; SEV2 means major functionality is degraded
for a subset of customers; SEV3 means a minor, non-blocking issue; SEV4 is
cosmetic or informational.

### SEV1 Response

A SEV1 incident requires the on-call engineer to open an incident channel
within 5 minutes, page a second engineer for support, and post a customer-
facing status update within 15 minutes. A written postmortem is required
within 3 business days of resolution.

## Database Migration Policy

All schema migrations must be backward-compatible for at least one release
cycle to support zero-downtime rolling deploys. Destructive migrations
(dropping columns or tables) require a two-step process: mark deprecated in
release N, remove in release N+2.

## API Rate Limits

The public API enforces a default rate limit of 100 requests per minute per
API key. Enterprise-tier customers can request an increase up to 1,000
requests per minute by contacting their account manager.

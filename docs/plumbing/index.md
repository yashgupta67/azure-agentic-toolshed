# Plumbing: connector-backed tools and small utilities

The unglamorous half of the catalog — tools wrapping specific enterprise connectors (the same pattern as a plain "get latest email" tool), plus small, high-hit-rate utilities that don't fit anywhere else but that agent workflows need constantly.

## Business process composites

| Tool | Status |
|---|---|
| Create-ticket + notify + log, fused into one tool | not yet built |
| Human-in-the-loop approval gate (Teams Adaptive Card) | not yet built |

## Connector-backed tools

| Tool | Connector | Status |
|---|---|---|
| Meeting transcript → summary + action items | Teams | not yet built |
| Document search-and-fetch | SharePoint / OneDrive | not yet built |
| Calendar scheduling (find slot + create invite) | Outlook | not yet built |
| Issue/PR triage tool | GitHub | not yet built |
| Ticket lifecycle tool (create/update/close with validation) | Jira / ServiceNow-style | not yet built |
| Approval-with-buttons notification | Slack | not yet built |
| Task sync tool | Excel / Planner | not yet built |

## Ops and small utilities

| Tool | Status |
|---|---|
| Cost-tracking tool (Azure Cost Management API) | not yet built |
| Immutable tool-call audit/decision log | not yet built |
| Cache/memoization tool | not yet built |
| Currency/unit conversion tool | not yet built |
| Date/timezone normalizer tool | not yet built |
| Diff/change-detection tool | not yet built |

Small utilities like the date normalizer look trivial next to a reflection loop, but agents reliably mangle dates and timezones on scheduling tasks — a dedicated, well-described tool for it is cheaper than debugging the failure downstream.

# What building this teaches you

This project doubles as a structured way to pick up Azure AI, agentic-AI, and a bit of DevOps — not through separate tutorials, but through the concepts each tool artifact actually requires you to touch.

## By the time you've built category A (agent loop harnesses)

Logic Apps Standard workflow authoring, the Request/Response trigger contract that makes a workflow into an MCP tool, built-in service-provider connectors (Azure Tables), Workflow Definition Language expressions, and the core agentic-harness concept of an externally enforced budget.

## By the time you've built category B/C (memory, multi-agent interop)

Vector search concepts (Azure AI Search), the A2A protocol and how it differs from MCP, and basic multi-agent coordination patterns (routing, shared state).

## By the time you've built category D/E (guardrails, RAG)

JSON Schema validation, Azure AI Content Safety and Language PII detection, the Azure AI Search REST API, and why grounding citations break by default.

## By the time you've built category H (connector-backed tools)

Whatever specific connector you're wrapping (Teams, SharePoint, GitHub, Jira, Excel) — each one's authentication model and action set, on top of the same Request/Response tool pattern.

## The DevOps layer, underneath all of it

GitHub Actions (deploy-docs, check-sources, validate-artifacts), Bicep as an optional IaC path, and — via the staleness bot — the basic idea of a system that tells you when it's gone stale instead of quietly rotting. This layer is intentionally kept thin; it's not the point of the project, but it's real, working CI/CD you'll have written yourself by the end.

## How to use this page

Don't read it top to bottom before building anything. Come back to it after finishing an artifact, to see explicitly what you just learned — that's more durable than reading a list of concepts before you've touched any of them.

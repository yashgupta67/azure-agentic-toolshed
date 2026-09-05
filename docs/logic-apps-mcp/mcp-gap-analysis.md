---
title: What's actually missing from Azure's MCP tooling
status: living-document
last_checked: 2026-09-05
---

# The MCP gap analysis

This page exists because the honest answer to "what's missing from Azure Logic Apps MCP support" is **not** "more connectors." Azure ships 1,400+ connectors and, as of Build 2026, a wizard that turns any one of them into an MCP tool in a few clicks. Anyone pitching a new connector as the gap hasn't read the docs.

The real gaps are in three places Microsoft structurally can't or won't fill: **orchestration logic that spans more than one action**, **quality control on the thing that actually drives agent behavior (the description text)**, and **DevOps for MCP servers themselves** (testing, staleness, observability, versioning). Every item below is scoped to one of those three, and every claim is sourced.

## What Azure already ships (so we don't rebuild it)

| Capability | Status | Source |
|---|---|---|
| Convert a connector action into an MCP tool via API Center wizard | GA-adjacent (preview), Build 2026 | [Create MCP servers driven by workflows](https://learn.microsoft.com/en-us/azure/logic-apps/create-mcp-server-api-center) |
| Logic Apps Standard workflow → remote MCP server (hand-built) | GA at Build 2026 | [Create remote MCP servers from Standard workflows](https://learn.microsoft.com/en-us/azure/logic-apps/create-model-context-protocol-server-standard) |
| Easy Auth (OAuth) or API-key auth on MCP endpoints | GA | same as above |
| Streamable HTTP transport | GA, no extra config | same as above |
| SSE transport | GA, requires VNet integration + `AllowCrossWorkerCommunication` | same as above |
| Azure DevOps as an MCP *server* (repos, wiki, work items) in Foundry's tool catalog | GA | [Azure DevOps Remote MCP Server lands in Foundry](https://devops.com/azure-devops-remote-mcp-server-lands-in-microsoft-foundry-giving-ai-agents-direct-access-to-your-devops-data/) |
| API Center governance: catalog, LLM-as-judge quality scoring on 4 dimensions | GA-adjacent, Build 2026 | Build 2026 Logic Apps announcement |

**Hard limits on the wizard path** (confirmed in the docs, not inferred):
- One connector per MCP server, one action per tool — no combining steps
- Built-in service-provider connectors and custom connectors aren't supported in the wizard
- Default tool description is copy-pasted from the connector's Swagger doc, not written for a routing LLM

That last limit is the seam this whole project lives in.

## The confirmed gaps, ranked by leverage

### 1. Composite tools (orchestration the wizard can't do)
The wizard is one-action-per-tool. The moment a task needs "look this up, transform it, then call the second system," you're back to hand-writing a Standard workflow — and almost nobody publishes reference patterns for this. Concrete builds:
- **Search field-selection / citation-fix tool**: a custom MCP tool wrapping the Azure AI Search REST API with an explicit `$select`, fixing the generic `doc_0`/`doc_1` citation problem that is still open upstream (`azure-sdk-for-python` #41085, `agent-framework` #4418).
- **"Create ticket + notify + log" as one tool**: three connector actions (e.g., ITSM create, Teams notify, Log Analytics write) fused into a single Request→Response workflow with one description, instead of forcing the LLM to sequence three separate tools correctly — sequencing is a known reliability failure mode, not a hypothetical one.
- **Structured-output branching tool for Foundry canvas**: a working Power Fx condition that routes on a structured-output field, since community reports show type-mismatch failures and the docs only show linear examples.

**Concepts you'll learn building this:** Logic Apps Standard workflow authoring, Request/Response trigger contracts, JSON Schema, Azure AI Search REST API, Power Fx expressions, Foundry Agent Service canvas.

### 2. Tool-description quality tooling
An independent audit of 219,069 MCP tools across 43,400+ servers found only 0.5% earn an A grade; 167,333 (76%) get an **F**, and missing/weak tool descriptions are the single most common failure ("State of MCP Tools" report, cited across multiple 2026 sources). Azure's own wizard makes this worse by default — it seeds descriptions from Swagger docs written for humans reading API reference, not models routing on intent. Nothing enforces the fix.
- **`lint_tool_descriptions.py`**: parses a `workflow.json`, extracts the Request trigger description and the Body JSON Schema, flags descriptions under N words, missing "when to use / when not to use" framing, and schema properties with no `description` or ambiguous types.
- **API Center scanner**: same linter run against your own tenant's registered MCP servers via the API Center REST API — turns "is my fleet of tools any good" into a CI check instead of a one-time audit.

**Concepts you'll learn:** JSON Schema validation, API Center REST API, writing prompt-engineering-grade tool descriptions, basic static-analysis scripting.

### 3. Cross-host compatibility testing
Confirmed nowhere: a single Logic App deployed as both SSE and streamable-HTTP transports, connected from Foundry, Copilot Studio, VS Code, and Claude Desktop, with the literal failure text captured per cell. Copilot Studio's documented lack of SSE support and SSE's VNet requirement mean this matrix is not obvious in advance, and it changes the deploy decision before you write a single tool.

**Concepts you'll learn:** VNet integration, private endpoints, `host.json` runtime settings, OAuth vs. API-key auth flows, reading MCP client logs across four different tools.

### 4. DevOps for MCP servers (not DevOps *as* an MCP server)
Azure DevOps is now itself an MCP server (see table above) — so don't build that, it exists. The actual missing piece is CI/CD and lifecycle tooling *for the MCP servers you build*:
- **Staleness bot**: fetches each artifact's cited Microsoft Learn source URL, rehashes the content, opens an issue and flips a status badge to grey on drift. Nothing like this exists publicly for Logic Apps docs.
- **`verified.yml` attestation schema**: machine-readable status (working / preview / broken-upstream / stale) plus which hosts were actually tested, versioned per artifact.
- **Schema/Bicep validation on PR**: JSON Schema lint + `bicep lint`/`bicep build --stdout` as a required GitHub Action check before an artifact merges.
- **Tool-call telemetry dashboard**: Logic Apps run history and Application Insights already capture per-tool call data, but nobody packages it as "which tools get called, by which host, with what latency/error rate" — a starter KQL workbook against Application Insights would close this.

**Concepts you'll learn:** GitHub Actions, Bicep, Infrastructure-as-Code validation, Application Insights + KQL (Kusto Query Language), semantic versioning for schemas, basic incident-response thinking (a bot that opens issues on drift).

### 5. Local dev/test harness
There's no published pattern for testing an MCP-backed workflow's trigger/schema contract before deploying it to Azure. A local harness — Logic Apps' local runtime plus a scripted MCP test client that posts sample payloads against the Request trigger and asserts on the Response shape — would catch schema mistakes before they cost a deploy cycle.

**Concepts you'll learn:** Azure Functions Core Tools / Logic Apps local runtime, contract testing, basic Python or Node MCP client usage.

### 6. Migration tooling
The `azure-ai-projects` 1.x → 2.x rename set (`AzureAISearchAgentTool` → `AzureAISearchTool`, `AgentsClient` → `AgentAdministrationClient`, and others) plus the newer `project_connection_id` gap in `agent-framework` (issue #3299 — MCP tools can't yet reference a connected resource for credentials, only inline `server_url`/`server_label`, unlike Bing Grounding/Fabric/SharePoint tools which already support `connection_id`) are real, dated, and currently unaddressed by any public codemod.

**Concepts you'll learn:** AST-based Python codemods (`libcms`/`ast`), SDK versioning discipline, secure credential patterns (`connection_id` vs. inline headers).

### 7. Governance-as-data
`concordance.json` (old name → new name → doc tree → SDK class) and `retirements.json`, published as versioned data files rather than a table in a blog post, are what makes other people's tooling able to consume and link to this instead of just reading it.

**Concepts you'll learn:** designing a stable public data schema, semantic versioning for data files, being a dependency other people's CI can pin to.

## Build order (also a learning ramp)

Roughly ordered so each stage's Azure/DevOps concepts build on the last:

1. **Transport compatibility matrix** (#3) — forces you through Bicep, VNet basics, Easy Auth, and four different MCP clients before you've written any "real" tool logic. Best first because the failure modes here gate every later artifact's transport choice.
2. **One composite tool, done properly** (#1, the Search citation-fix tool) — first real Request/Response workflow, first custom trigger description, first `verified.yml`.
3. **Tool-description linter** (#2) — small script, immediate payoff, teaches you to read your own artifacts critically.
4. **Staleness bot + validate-artifacts CI** (#4) — first GitHub Actions you write from scratch; turns the repo from "a pile of files" into something that maintains itself.
5. **Local test harness** (#5) — once you've felt the pain of a bad deploy cycle in steps 2–4, this stops being abstract.
6. **Codemod + concordance.json** (#6, #7) — lowest Azure-infra dependency, good filler/portfolio piece once the core site works.

Everything here is buildable entirely on the free tier of GitHub (public repo → free Pages + Actions minutes) plus your existing sponsored Azure subscription for the actual Logic Apps deploys. Nothing in this list requires a paid SaaS tool, a paid API, or a second Azure subscription.

# Cross-host compatibility

The question nobody answers in one place: if you build a Logic Apps MCP server, which agent hosts can actually talk to it, on which transport?

## What's confirmed from Microsoft's own docs

| Transport | Requirements | Notes |
|---|---|---|
| Streamable HTTP | None beyond the base MCP server setup | Default recommendation for every artifact in this repo |
| SSE (Server-Sent Events) | VNet integration + `host.json` → `Runtime.Backend.EdgeWorkflowRuntimeTriggerListener.AllowCrossWorkerCommunication: true` | Adds cost (VNet integration is billed) and complexity; Copilot Studio is documented as not supporting SSE at all |

## The matrix this section will hold

A single Logic App, deployed with both transports, tested against each of these clients, with the literal error text captured for every failing cell:

| | Foundry | Copilot Studio | VS Code | Claude Desktop |
|---|---|---|---|---|
| Streamable HTTP | not yet tested | not yet tested | not yet tested | not yet tested |
| SSE | not yet tested | not yet tested | not yet tested | not yet tested |

This table is empty because it needs a real deployment and real connection attempts against each client — nothing here is filled in until someone actually runs it. See the [gap analysis](../logic-apps-mcp/mcp-gap-analysis.md#3-cross-host-compatibility-testing) for why this specific matrix doesn't exist anywhere else yet.

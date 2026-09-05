# Orchestration & multi-agent coordination

Tools for the moment a single agent stops being enough — shared state, task division, interop with agents outside Foundry, and the operability primitives (health checks, kill switches) that a system with more than one agent actually needs in production.

| Tool | What it's for | Status |
|---|---|---|
| Tiered memory tool | Short-term / episodic / long-term memory, backed by Azure AI Search vectors + table storage | not yet built |
| Logic-Apps-as-A2A-agent bridge | Lets a Logic App workflow join an A2A multi-agent network as a peer, not just sit behind MCP | not yet built |
| Agent router/dispatcher | Classifies a request and returns which downstream agent/tool should handle it | not yet built |
| Idempotency/deduplication check | Before a side-effecting action, checks "have I already done this?" | not yet built |
| Shared task queue | Agents pull work items and mark them done — real labor division, not just tool calls | not yet built |
| Kill-switch / feature-flag tool | Instantly disable a specific capability across every agent without redeploying | not yet built |
| Fleet health-check tool | Pings every registered MCP tool and reports what's actually up | not yet built |
| Context-compression tool | Compresses a large context blob before handoff between agents to fit a token budget | not yet built |
| Data-boundary policy-check tool | Checks whether a data field is allowed to leave a boundary before a cross-system call | not yet built |

## Why this comes after the tool catalog, not before

A 5-agent reference architecture wiring several of these tools into one working Foundry system is planned, but deliberately not built first — the tools are the building blocks, and a reference architecture built on top of a mostly-empty shelf teaches nothing. This page will grow a worked example once enough of the table above is real.

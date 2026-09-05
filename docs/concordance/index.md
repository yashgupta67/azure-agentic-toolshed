# Concordance

Azure's AI stack renames things often enough that "what used to be called X" is a real, recurring search. This section publishes that mapping as versioned data, not just a table in a blog post, so other people's tooling can consume it directly — see [`data/concordance.json`](https://github.com/yashgupta67/azure-agentic-toolshed/blob/main/data/concordance.json) and [`data/retirements.json`](https://github.com/yashgupta67/azure-agentic-toolshed/blob/main/data/retirements.json).

## Confirmed renames tracked so far

| Old name | New name | Where |
|---|---|---|
| `AzureAISearchAgentTool` | `AzureAISearchTool` | `azure-ai-projects` SDK |
| `AgentsClient` | `AgentAdministrationClient` | `azure-ai-projects` SDK |

This list grows as renames are confirmed against release notes and changelogs — nothing goes in here from memory alone. A 1.x → 2.x codemod script covering these renames is planned; see the [gap analysis](../logic-apps-mcp/mcp-gap-analysis.md#6-migration-tooling).

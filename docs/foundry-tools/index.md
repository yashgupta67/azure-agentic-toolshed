# Foundry tools: guardrails, RAG, and AI services

Tools you attach directly to a Foundry agent that either keep it safe (guardrails), help it retrieve and ground correctly (RAG), or extend it with an Azure AI service it can't reach on its own.

| Tool | Category | Status |
|---|---|---|
| Structured-output schema validator | Guardrail | not yet built |
| Dry-run / simulate-before-execute | Guardrail | not yet built |
| Content Safety + PII redaction gate | Guardrail | not yet built |
| Search citation-fix tool | RAG | not yet built |
| Document Intelligence extraction tool | RAG | not yet built |
| Vision / image-analysis tool | AI service | not yet built |
| Translation tool | AI service | not yet built |
| Cost-aware model router | AI service | not yet built |

## Why the citation-fix tool matters more than it sounds

Azure AI Search's default grounding citations show up as generic `doc_0`, `doc_1` labels — an open issue upstream in both `azure-sdk-for-python` (#41085) and `agent-framework` (#4418), unresolved as of this writing. The fix is a custom MCP tool wrapping the Search REST API with an explicit `$select`, which is a small amount of code for a problem that otherwise makes an agent's answers impossible to verify against source.

# Conventions every artifact follows

These aren't style preferences — each one exists because Microsoft's own docs confirm it's the difference between a tool an agent can actually use and one it silently mis-calls.

## One workflow = one tool

Don't build a multi-purpose workflow with a `mode` parameter. An LLM picks tools by reading descriptions; a tool that does four things has a description nobody can write well, because the description has to be vague enough to cover all four. Split it into separate workflows instead — Logic Apps Standard lets you host many workflows in one app, and MCP lets you register several of them as one logical server (see [`artifacts/_shared-infra`](https://github.com/yashgupta67/azure-agentic-toolshed/tree/main/artifacts/_shared-infra)).

## Write the trigger description for a model, not a human

This is the single highest-leverage field in the entire stack, and it looks like a throwaway comment box in the portal. It should state: what the tool does, exactly when to call it, what format its inputs take, and — just as important — when *not* to use it. Compare any artifact's `broken/README.md` against its working trigger description to see the difference a specific, imperative description makes versus a bare factual one.

## Every schema property gets a `description`, and `required` is explicit

The Request Body JSON Schema's per-property `description` fields are what drive parameter accuracy at call time — an LLM reading a bare `{"type": "string"}` has to guess what goes there. Mark format expectations explicitly (e.g. "ISO 8601 date in UTC", "base64-encoded").

## Streamable HTTP by default, SSE only when justified

SSE needs VNet integration and the `host.json` `AllowCrossWorkerCommunication` setting, and at least one major MCP client (Copilot Studio) doesn't support it at all. Every artifact in this repo defaults to streamable HTTP; SSE is only used where a specific artifact's page explains why (see [cross-host compatibility](../cross-host/index.md)).

## Every artifact ships its broken pair

Each tool's `broken/` folder holds a variant that fails in a specific, documented way — usually a vague trigger description, but sometimes a genuine platform error. That pairing is what makes this a teaching resource instead of a reference manual: reading only the working version tells you what to do, but not what happens when you get it wrong.

## Code first, designer as fallback — never the reverse

Every artifact ships the **complete** workflow JSON, including the connector logic, not just the trigger/response shell — the goal is paste-and-run, not paste-the-easy-part-then-click-the-rest. Two consequences of that:

- Where an action's exact JSON shape is genuinely uncertain (built-in connectors like Azure Tables require an app-level `connections.json` entry whose exact structure isn't worth guessing when the designer generates it correctly in one click), the artifact says so explicitly and gives the smallest possible designer step to resolve just that uncertainty — never "build the rest of this in the designer" as a cop-out.
- Any field that needs a real, environment-specific value (an API key, an endpoint, a connection name) is marked clearly in the JSON's surrounding instructions with exact steps and a worked example for where to find that value — never left as a silent assumption.

## Cheapest safe default, always with a teardown command

No artifact defaults to a billed add-on (VNet integration, private endpoints, a second Standard plan) unless the specific thing being demonstrated genuinely requires it, and when it does, the cost and the teardown command are stated up front, not buried at the bottom of the page.

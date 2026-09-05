# Broken variant: no timeout on the human wait

## What's different

The Teams "Post an Adaptive Card and wait for a response" action is configured with no timeout (or an unrealistically long one), and there's no fallback branch for the case where nobody responds.

## Why this breaks in practice

Logic Apps workflow runs aren't free to leave hanging indefinitely, and more importantly, whatever called this tool through MCP is very likely also waiting synchronously on the HTTP response — most MCP clients apply their own request timeout well under Teams-approval timescales (a reviewer might not see the card for hours). The agent's tool call errors out or times out on the client side long before a human ever answers, and the escalation — the entire point of the tool — silently fails to produce anything.

## The fix

Set an explicit, realistic timeout on the Teams action, and add a parallel branch or a post-timeout fallback (e.g., escalate to a second reviewer, or return `was_escalated: true, human_decision: "no response — escalate further"` rather than letting the HTTP call itself just hang until the client gives up).

## Fill this in once tested

Once built, record the actual timeout behavior you observe from your MCP client (Foundry/VS Code/etc.) when a Teams reply is delayed — that concrete number is what determines what a "realistic timeout" actually is for this tool.

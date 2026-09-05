# Broken variant: a description that doesn't force compliance

This isn't a platform error — it's a behavioral failure, and it's arguably the more dangerous kind because nothing crashes. The tool works exactly as coded; the agent just doesn't obey it.

## What's different

Same workflow, same Table Storage logic, only the trigger description changes:

> "Checks the current loop budget."

That's it. No instruction about *when* to call it, no instruction about what to do with the response, no consequence for ignoring `allowed: false`.

## Why this breaks in practice

A 2026 RAND study on LLM-as-judge reliability found that model behavior on instruction-following is inconsistent even on much simpler, more explicit prompts than a bare one-line tool description — small wording changes measurably change compliance rates. A tool description that states a fact ("checks the budget") rather than an imperative with a consequence ("you MUST stop when this returns false") gives the model no reason to treat the response as binding. In practice, an agent given this vague version will often call the tool, receive `allowed: false`, and continue looping anyway — because nothing in the tool's description told it that response was supposed to end the conversation, not just inform it.

This is exactly the class of failure the [tool-description linter](https://github.com/yashgupta67/azure-agentic-toolshed/blob/master/docs/logic-apps-mcp/mcp-gap-analysis.md#2-tool-description-quality-tooling) is meant to catch mechanically: a description under a certain length, with no "when to use / what to do with the result" framing, gets flagged before it ever reaches production.

## The fix

Compare this file's description against the working `loop-budget-check.trigger-and-response.json` (shown earlier on this page): the working version states the trigger condition ("call this before every step"), the required action on a specific response value ("if allowed: false, you MUST stop"), and the consequence of not doing so. That specificity is not decoration — it's the entire mechanism by which this tool actually constrains the loop.

## Fill this in once you've actually tested it

This page currently describes the *expected* failure mode based on published research, not a literal captured transcript. Once you deploy the vague version and run it against a real agent in Foundry, replace this section with the actual conversation excerpt showing the agent ignoring `allowed: false` — that literal transcript is worth more than the prediction above, and it's what should ultimately anchor this page.

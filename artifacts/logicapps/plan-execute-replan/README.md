# Plan-execute-replan loop

Status: <span class="status-badge status-preview">preview — not yet deployed/verified</span>

## The problem

[Reflection loop](https://github.com/yashgupta67/azure-agentic-toolshed/tree/master/artifacts/logicapps/reflection-loop) polishes a single deliverable through critique. This tool solves a different problem: a task that naturally decomposes into an ordered sequence of steps, where one step failing shouldn't abort the whole task — it should trigger replanning the *remaining* steps in light of what went wrong. This is the ReAct / Plan-and-Solve pattern, built as a bounded, deployable tool instead of hand-rolled orchestration code.

## Use case

An agent gets a task like "research competitor pricing for three products and produce a comparison table." Rather than the calling agent hand-managing that sequencing itself, it delegates the whole thing to `plan-execute-replan`, which decomposes, executes each step, and — if step 2 fails because a source site is unreachable — regenerates a plan for the remaining work (e.g., substituting an alternative source) instead of failing the entire task.

## Build it (Azure Portal + paste JSON)

Needs the same Azure OpenAI connection as [reflection-loop](https://github.com/yashgupta67/azure-agentic-toolshed/tree/master/artifacts/logicapps/reflection-loop) — if you haven't set that up yet, do reflection-loop's first two steps (get your endpoint/key, connect your Logic App) before continuing here. It's one-time per Logic App, not per tool.

<div class="steps" markdown>

<div class="step-card" markdown>
**Build the workflow**

- **Workflows → + Add** → name it `plan-execute-replan` → keep **Stateful** → **Create** → open it → **Code view**.
- Delete everything in the box, paste in the full contents of `plan-execute-replan.trigger-and-response.json` (shown further down this page).
- Find-and-replace `REPLACE_WITH_YOUR_DEPLOYMENT_NAME` (4 occurrences) with your Azure OpenAI deployment name.
</div>

<div class="step-card" markdown>
**Save and check for errors**

- Click **Save**, then check **Designer** for any box with a red warning triangle (there are 4 Azure OpenAI actions: `Generate_Plan`, `Execute_Step`, `Replan_Remaining`, `Synthesize_Final_Result`).
- If one errors: delete it, re-add via **+ → Add an action → search "Azure OpenAI" → Get chat completions**, and pick your existing `azureOpenAI` connection from the dropdown.
- Everything else — the `Until` loop, the tracking variables, the replan-budget check — is standard and needs no changes.
</div>

</div>

## Worked example

Task: "Draft a rollout announcement, get it translated to Spanish, and check it doesn't reference the old product name." Step 2 (translation) fails because the target text exceeded a length limit on the first pass; the tool replans, splitting it into "shorten the announcement" then "translate," and completes with `replans_used: 1` — the calling agent sees the whole path, not a silent failure.

## Cost impact

<div class="cost-note" markdown>
:fontawesome-solid-sack-dollar: Same shape as reflection-loop: **no new hourly resource** — cost is Azure OpenAI token usage proportional to actual steps and replans. Use the cheapest available deployed model for testing.
</div>

## Concepts this teaches

Logic Apps array variables (`Initialize`, `Set`, `Append to array variable`), the `skip`/`first`/`length` expression functions, designing a tool response that exposes partial progress and replanning history instead of a bare success/failure flag, and the practical difference between "polish a deliverable" (reflection-loop) and "sequence a task" (this tool) as two distinct harness patterns.

!!! note "Status and next steps"
    Designed but not yet deployed. Once built, confirm the array-variable expressions behaved as described and record the literal step/replan history from a real run in `verified.yml`.

# Reflection / self-critique loop

Status: <span class="status-badge status-preview">preview — not yet deployed/verified</span>

## The problem

A single pass from a model is often good enough. When it isn't — a customer-facing answer, generated code, a structured document someone will act on — the standard fix people reach for is "have the model check its own work." The research on that is blunter than most tutorials let on: a 2026 RAND study stress-testing LLM-as-judge setups found no judge model was uniformly reliable, with frontier models exceeding 50% error rates on hard bias benchmarks, and consistency breaking on inputs as trivial as formatting changes. Using a model to grade a model isn't escaping subjectivity — it's outsourcing it to a second model with its own blind spots.

This tool is the honest version of a reflection loop: it uses an LLM judge because it's still useful signal, but it never trusts the judge alone. Every iteration also runs a deterministic check (length, format, presence of required sections), the loop has a hard iteration cap regardless of what the judge says, and every iteration's score and critique gets returned in the response — so whatever called this tool can see the disagreement history, not just a final "trust me" answer.

## Use case

An agent needs a polished output — not a lookup, a piece of work. It calls `reflection-loop` with the task and constraints instead of calling the model directly once. It gets back the final answer plus the full iteration history, so a human reviewer (or a stricter downstream guardrail) can see exactly how the answer evolved and whether the judge and the deterministic check ever disagreed.

## One tool, self-contained

Unlike the [loop circuit breaker](https://github.com/yashgupta67/azure-agentic-toolshed/tree/master/artifacts/logicapps/loop-circuit-breaker), this workflow's iteration cap is internal — it doesn't need an external budget check, because the whole critique-revise cycle runs inside a single Logic Apps `Until` loop within one MCP tool call. It does need an Azure OpenAI (or Foundry) model deployment to call.

## Build it (Azure Portal + paste JSON)

You'll need an Azure OpenAI resource with a chat model deployed first (the cheapest available small/mini model is enough — this workflow makes two model calls per iteration, so cost scales with iteration count, not with anything fixed). If you don't have one yet, create it the same way as the Logic App: portal search box → `Azure OpenAI` → **Create** → fill in the basics → then in the resource, go to **Model deployments** and deploy a cheap chat model, giving the deployment a name you'll remember.

<div class="steps" markdown>

<div class="step-card" markdown>
**Get your Azure OpenAI endpoint and key** *(you'll need both in the next step)*

- Open your Azure OpenAI resource in the portal.
- Left-hand menu → **Keys and Endpoint** (under **Resource Management**).
- Copy the **Endpoint** value (looks like `https://your-resource-name.openai.azure.com/`).
- Copy **KEY 1**.
- Also note your model's **deployment name** (left-hand menu → **Model deployments** — this is the name *you* gave it, not the underlying model name like "gpt-4o").
</div>

<div class="step-card" markdown>
**Connect your Logic App to Azure OpenAI** *(one-time — every tool after this reuses it)*

- Open your Logic App (Standard) → **Workflows** → **+ Add** → name it `zzz-delete-me`, keep **Stateful** → **Create** → open it → **Designer**.
- Click **+** → **Add an action** → search `Azure OpenAI` → click **Get chat completions**.
- A connection panel appears: **Connection name** = `azureOpenAI`, **Authentication type** = **URL and key-based authentication**.
- Paste your **Endpoint** into the endpoint field, and your **KEY 1** into the key field.
- Click **Create**.
- Go back to **Workflows**, delete `zzz-delete-me`. The connection stays saved for every workflow after this.
</div>

<div class="step-card" markdown>
**Build the workflow**

- **Workflows → + Add** → name it `reflection-loop` → keep **Stateful** → **Create** → open it → **Code view**.
- Delete everything in the box, paste in the full contents of `reflection-loop.trigger-and-response.json` (shown further down this page).
- Before saving, find-and-replace `REPLACE_WITH_YOUR_DEPLOYMENT_NAME` (2 occurrences) with your deployment name from step 1.
- Click **Save**, then check **Designer** — if `Generate_Or_Revise_Draft` or `Judge_Draft` shows a red warning triangle, delete it and re-add via **+ → Add an action → search "Azure OpenAI" → Get chat completions**, picking your existing `azureOpenAI` connection from the dropdown.

Everything else — the `Until` loop, the variables, the deterministic check, the history tracking — is standard and needs no changes.
</div>

</div>

## Worked example

A support-ticket-response agent calls `reflection-loop` with `task`: "Write a reply to this angry customer email: <email text>", `draft_instructions`: "Apologetic but not obsequious, under 150 words, must offer a concrete next step", `max_iterations`: 3. The tool returns a final answer plus a 2-entry history showing the first draft scored 0.6 (missing a concrete next step, per both the judge and the deterministic check-for-a-next-step) and the second scored 0.9. The calling agent — or a human reviewer — can see *why* it took two passes, not just the final text.

## Cost impact

<div class="cost-note" markdown>
:fontawesome-solid-sack-dollar: No new Standard/hourly resource — the shared Logic App already exists. The real cost driver is **Azure OpenAI token usage**: pay-per-token, no idle cost. With a cheap small model, a full 2-3 iteration cycle costs fractions of a cent — testing this a dozen times won't meaningfully register on a subscription.
</div>

## Concepts this teaches

The `Until` loop construct in Logic Apps Standard, the Azure OpenAI built-in connector, why an LLM-as-judge pattern needs a deterministic check alongside it (not instead of it), and how to design a tool's response shape to expose disagreement/history rather than hiding it behind a single confident-looking answer.

!!! note "Status and next steps"
    Designed but not yet deployed. Once built, record in `verified.yml` whether the Azure OpenAI connector's actual action/parameter names matched what's described here, and capture the literal iteration history from a real run.

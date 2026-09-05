# Loop circuit breaker

Status: <span class="status-badge status-preview">preview — not yet deployed/verified</span>

## The problem

Nothing in Azure's own MCP tooling stops an agent loop from running forever. If a reasoning loop, a plan-execute-replan cycle, or a multi-step tool chain gets stuck retrying, nothing in the platform enforces a hard ceiling — you find out from the bill or from a user complaint, not from the system itself. This tool is that ceiling: a budget an agent (or an orchestrating workflow) must check in with before every step, with a hard stop when the budget runs out.

It's built first, ahead of every other harness/loop tool in this repo, because the reflection loop, the plan-execute-replan loop, and the debate tool all *depend on* something like this existing — none of them should be built without a budget check wired in.

## Use case

An orchestrator agent (or a human developer's own agentic code) is running a loop: "keep reasoning/calling tools until the task is done." Before each iteration, it calls `loop-budget-check`. If the response says `allowed: false`, the loop stops immediately and reports the reason instead of continuing indefinitely.

## Two tools, one Logic App

Per this repo's convention (one workflow = one tool, and one Standard Logic App hosting many workflows — see [`artifacts/_shared-infra`](https://github.com/yashgupta67/azure-agentic-toolshed/tree/master/artifacts/_shared-infra)):

| Workflow | Tool it becomes | Purpose |
|---|---|---|
| `loop-budget-check` | `loop-budget-check` | Call before every loop step. Increments and checks the counter. |
| `loop-budget-reset` | `loop-budget-reset` | Call once at the start of a new session, before the first check. |

## Build it (Azure Portal + paste JSON)

Assumes you've already done the one-time setup in [`artifacts/_shared-infra`](https://github.com/yashgupta67/azure-agentic-toolshed/tree/master/artifacts/_shared-infra) (a Resource Group, a Storage Account, and a Logic App Standard resource).

<div class="steps" markdown>

<div class="step-card" markdown>
**Create a table to hold the budget numbers**

A "table" here is just a place to store data — like a mini spreadsheet.

- Open your Storage Account (the one from the setup step) in the portal.
- On the left-hand menu, click **Storage browser**.
- In the list that appears, click **Tables**.
- Click **+ Add table** at the top.
- Type the name: `LoopBudgets`
- Click **OK**.
</div>

<div class="step-card" markdown>
**Get your Storage Account's connection string** *(you'll need to paste this in the next step)*

- Still in your Storage Account, look at the left-hand menu for **Access keys** (under the **Security + networking** section).
- Click **Access keys**.
- Under **key1**, click **Show** next to **Connection string**.
- Click the copy icon next to it. This copies a long piece of text starting with `DefaultEndpointsProtocol=...` — keep it copied, you'll paste it in the next step.
</div>

<div class="step-card" markdown>
**Connect your Logic App to Table Storage** *(one-time — every tool after this reuses it)*

- Open your Logic App (Standard) resource.
- On the left-hand menu, click **Workflows**.
- Click **+ Add**. Name it `zzz-delete-me`, leave type as **Stateful**, click **Create**.
- Click on the workflow you just made, then click **Designer**.
- Click the **+** button, then **Add an action**.
- In the search box, type `Azure Table Storage` and click it.
- Click **Get Entity**.
- A panel appears asking you to create a connection. For **Connection name**, type: `azureTableStorage`
- For **Authentication Type**, choose **Connection String**.
- In the **Connection String** box, paste the text you copied in the last step.
- Click **Create**.
- Once it connects, go back to **Workflows** (left menu), find `zzz-delete-me`, and delete it — you only needed it to create the connection. The connection itself stays saved and every workflow from now on can use it.
</div>

<div class="step-card" markdown>
**Build the first tool: `loop-budget-check`**

- **Workflows** (left menu) → **+ Add** → name it exactly `loop-budget-check` → keep **Stateful** → **Create**.
- Click on it, then click **Code view** (top of the designer — looks like `</>`).
- Delete everything in the box.
- Copy the whole code block under **"loop-budget-check workflow JSON"** further down this page, and paste it in.
- Click **Save** (top left).
- Click **Designer** to look — you should see boxes connected by arrows. That means it worked.
- If a box named `Get_Entity` or `Insert_or_Update_Entity` has a red warning triangle on it: delete just that one box, then add it back the same way you did in the step above (search `Azure Table Storage`, pick the same action, reuse the `azureTableStorage` connection — it's already saved, so it'll show up in a dropdown instead of asking you to create it again).
</div>

<div class="step-card" markdown>
**Build the second tool: `loop-budget-reset`**

Exact same steps as above, except:

- Name it `loop-budget-reset` instead.
- Use the code block under **"loop-budget-reset workflow JSON"** further down this page instead.
</div>

<div class="step-card" markdown>
**Turn both into tools an AI agent can use**

- On your Logic App's left-hand menu, click **Agents**, then click **MCP servers**.
- Click **Use existing workflows**.
- Tick both `loop-budget-check` and `loop-budget-reset`.
- Name the server `agent-harness-tools`.
- Click **Create**.
- Copy the URL it shows you — paste this into Foundry's Tools section, the same way you connected your Outlook tool.
</div>

</div>

## Worked example

An orchestrator agent's system prompt includes: *"At the start of a new task, call loop-budget-reset. Before each subsequent reasoning step or tool call, call loop-budget-check with the same session_id. If it returns allowed: false, stop and explain why instead of continuing."* A task that would otherwise loop indefinitely now hits a hard, observable stop instead of silently burning tokens and API calls.

## Cost impact

<div class="cost-note" markdown>
:fontawesome-solid-sack-dollar: No new resources beyond the shared Logic App and its Storage account — Table Storage transactions at this volume cost a fraction of a cent. **No incremental hourly cost.**
</div>

## Concepts this teaches

Logic Apps Standard workflow authoring directly in JSON (the `If`, `InitializeVariable`, `SetVariable`, and `ServiceProvider` action types), how built-in connectors resolve a named connection from the app-level `connections.json`, Workflow Definition Language expressions (`coalesce`, `sub`, `utcNow`, `actions(...)['status']`), and the core agentic-harness concept of an externally-enforced budget.

!!! note "Status and next steps"
    The trigger/response contract and control flow are standard Workflow Definition Language and should paste in as-is. The two `ServiceProvider` actions (Azure Tables) are a best-effort reconstruction, flagged inline — confirm they work as pasted, or note what the designer actually generated, and record the result in `verified.yml`. Any literal error text becomes a page under `docs/failures/`.

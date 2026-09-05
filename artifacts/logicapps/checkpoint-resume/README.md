# Checkpoint/resume for long-running loops

Status: <span class="status-badge status-preview">preview — not yet deployed/verified</span>

## The problem

A long-running agent task that crashes, times out, or gets interrupted normally just restarts from zero — nobody publishes a simple, generic "save progress, resume from it" pair of tools for agent loops. This closes that gap the same way [loop-circuit-breaker](https://github.com/yashgupta67/azure-agentic-toolshed/tree/master/artifacts/logicapps/loop-circuit-breaker) closed the budget gap: two small Table-Storage-backed tools, cheap, and reusable across any long-running task regardless of what framework or model is driving it.

## Use case

An agent working through a long multi-step task (e.g., processing a large batch of records) calls `checkpoint-save` after completing each batch, with a state payload describing what's done so far. If the session is interrupted — a crash, a timeout, a redeploy — the next invocation calls `checkpoint-load` first, finds the saved state, and resumes from the last completed batch instead of reprocessing everything.

!!! warning "A real limitation, stated up front"
    Azure Table Storage entity properties cap out around 64KB per string property (roughly 1MB per entity total). This works well for compact checkpoint state — step indices, small partial results, IDs to re-fetch. It's the wrong backing store for large documents or full conversation histories; that calls for Blob Storage instead, with Table Storage holding just a pointer. This artifact uses Table Storage because most agent checkpoint state is small — adapt it if yours isn't.

## Build it (Azure Portal + paste JSON)

This reuses the same `azureTableStorage` connection you set up in [loop-circuit-breaker](https://github.com/yashgupta67/azure-agentic-toolshed/tree/master/artifacts/logicapps/loop-circuit-breaker) — if you haven't built that one yet, do its first three steps (create a table, get the connection string, connect the Logic App) before continuing here.

<div class="steps" markdown>

<div class="step-card" markdown>
**Create a table to hold checkpoint data**

- Open your Storage Account in the portal.
- Left-hand menu → **Storage browser** → **Tables** → **+ Add table**.
- Name it: `Checkpoints`
- Click **OK**.
</div>

<div class="step-card" markdown>
**Build the first tool: `checkpoint-save`**

- **Workflows** (left menu) → **+ Add** → name it `checkpoint-save` → keep **Stateful** → **Create**.
- Click on it, then click **Code view**.
- Delete everything in the box, then paste in the code under **"checkpoint-save workflow JSON"** further down this page.
- Click **Save**, then check **Designer**.
- If the box named `Insert_or_Update_Entity` has a red warning triangle: delete it, add it back via **+ → Add an action → search "Azure Table Storage" → Insert or Update Entity**, and pick your existing `azureTableStorage` connection from the dropdown (it's already saved — you won't need to reconnect).
</div>

<div class="step-card" markdown>
**Build the second tool: `checkpoint-load`**

Same steps as above, except name it `checkpoint-load` and use the code under **"checkpoint-load workflow JSON"** further down this page. If `Get_Entity` shows a warning, use the same fallback (search "Azure Table Storage", pick **Get Entity**, reuse your existing connection).
</div>

<div class="step-card" markdown>
**Turn both into tools an AI agent can use**

Same MCP server group as the other harness tools — Logic App → **Agents → MCP servers → Use existing workflows**, tick both, add to `agent-harness-tools` (or create it if you haven't already).
</div>

</div>

## Worked example

A batch-processing agent's system prompt: *"At the start, call checkpoint-load with your session_id. If found is true, resume from state.last_completed_batch + 1. After each batch, call checkpoint-save with the updated state."* A crash mid-run costs at most one batch of rework, not the whole job.

## Cost impact

<div class="cost-note" markdown>
:fontawesome-solid-sack-dollar: **No new hourly resource** — same shared Logic App and storage account as every other Table-backed tool in this repo. Negligible transaction cost.
</div>

## Concepts this teaches

The `string()`/`json()` expression functions for serializing structured data into a Table Storage string property and back, and a real, common storage limitation (property size caps) that shapes which backing store is the right choice for a given amount of state.

!!! note "Status and next steps"
    Designed but not yet deployed. Once built, test with a realistic state payload size and confirm it stays under Table Storage's property limits, or switch to the Blob-backed variant described above.

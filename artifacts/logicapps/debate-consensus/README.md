# Multi-agent debate / self-consistency

Status: <span class="status-badge status-preview">preview — not yet deployed/verified</span>

## The problem

A single model call gives you one answer with no signal about how confident that answer actually is. Self-consistency — sampling the same question independently several times and checking agreement — is a well-established technique for surfacing that signal, but nobody ships it as a drop-in tool. This one does: call it instead of a single model call when being wrong is costly, and get back both a consensus answer and the disagreement rate across samples.

## Use case

An agent needs to classify something (is this transaction fraudulent, is this ticket a P1) where a wrong answer is expensive. Instead of one model call, it calls `debate-consensus` with `num_samples: 5`. If all 5 independent samples agree, `agreement_rate` is 1.0 and the agent proceeds with confidence. If the samples split 3-2, `agreement_rate` is 0.6 and `flagged_low_confidence` is true — the agent can route to [confidence-gated human escalation](https://github.com/yashgupta67/azure-agentic-toolshed/tree/main/artifacts/logicapps/confidence-gated-escalation) instead of silently trusting a shaky majority.

## Build it (Azure Portal + paste JSON)

Needs the same Azure OpenAI connection as [reflection-loop](https://github.com/yashgupta67/azure-agentic-toolshed/tree/main/artifacts/logicapps/reflection-loop) — set that up first if you haven't already (get your endpoint/key, connect your Logic App).

<div class="steps" markdown>

<div class="step-card" markdown>
**Build the workflow**

- **Workflows → + Add** → name it `debate-consensus` → keep **Stateful** → **Create** → open it → **Code view**.
- Delete everything in the box, paste in the full contents of `debate-consensus.trigger-and-response.json` (shown further down this page).
- Find-and-replace `REPLACE_WITH_YOUR_DEPLOYMENT_NAME` (3 occurrences) with your deployment name.
- Save, then check **Designer** — if any Azure OpenAI action has a red warning triangle, delete it and re-add via **+ → Add an action → search "Azure OpenAI" → Get chat completions**, picking your existing connection.
</div>

<div class="step-card" markdown>
**Fix two known weak spots** *(flagged inline in the JSON — don't trust these two as pasted)*

- `Set_Consensus_From_Tally` — Workflow Definition Language has no built-in "most frequent item in an array" function, so this currently just takes the *first* sample as a placeholder, which is wrong. Add an **Inline Code (JavaScript)** action to compute the real mode of `samples`, or use a tiny extra Azure OpenAI call constrained to "respond with only the exact string that appears most often."
- `Compute_Agreement_Rate` — same limitation. The placeholder only distinguishes "all samples identical" from "not." A real implementation counts how many samples match `consensus_answer` and divides by `num_samples` — Inline Code again, or one more Azure OpenAI call.

Everything else — `Foreach` with `runtimeConfiguration.concurrency.repetitions` for parallel sampling, the variable setup, the free-form synthesis branch — is standard and needs no changes.
</div>

</div>

## Worked example

`question`: "Based on this transaction description, is this likely fraudulent?", `answer_format`: "yes or no", `num_samples`: 5. Four samples say "no," one says "yes" — `consensus_answer: "no"`, `agreement_rate: 0.8`, not flagged. A genuinely ambiguous transaction might split 3-2, get flagged, and route to a human instead of auto-clearing on a bare majority.

## Cost impact

<div class="cost-note" markdown>
:fontawesome-solid-sack-dollar: **No new hourly resource.** Cost scales linearly with `num_samples` — 5 samples means 5 (or 6, with the free-form synthesis path) model calls per invocation, still fractions of a cent on a cheap deployed model.
</div>

## Concepts this teaches

Logic Apps `For each` with parallelism, the `range` expression function, why self-consistency needs actual sampling temperature (not 0) to be meaningful, and the distinction between a deterministic tally (trustworthy) and an LLM-synthesized "consensus" (another judge call, same reliability caveats as [reflection-loop](https://github.com/yashgupta67/azure-agentic-toolshed/tree/main/artifacts/logicapps/reflection-loop)).

!!! note "Status and next steps"
    Designed but not yet deployed. Once built, record the actual agreement rates on a genuinely ambiguous question versus an easy one — that's the real evidence this tool works.

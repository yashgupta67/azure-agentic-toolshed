# Confidence-gated human escalation

Status: <span class="status-badge status-preview">preview — not yet deployed/verified</span>

## The problem

[Debate-consensus](https://github.com/yashgupta67/azure-agentic-toolshed/tree/master/artifacts/logicapps/debate-consensus) and similar tools can tell you *that* an answer is uncertain, but nothing automatically does anything with that signal — it's on the calling agent to notice a low `agreement_rate` and decide what to do. This tool is what to do: it's the last gate before an agent commits to an uncertain answer, packaging the full context and handing it to a human when confidence is too low, instead of the agent silently proceeding or the developer hand-wiring a Teams call every time this pattern comes up.

This is deliberately distinct from a Teams approval gate over a *side-effecting action* (that's [category F](https://github.com/yashgupta67/azure-agentic-toolshed/blob/master/docs/plumbing/index.md)) — this tool escalates an *answer or decision* for review, before anything downstream has acted on it.

## Use case

An agent produces a candidate answer to a customer's account question along with a confidence score (from `debate-consensus`, or a model's own self-reported confidence). If confidence is high, this tool just passes the answer through. If it's low, a human on a Teams channel gets an Adaptive Card with the question, the candidate answer, and the confidence score, and their reply becomes the final answer instead.

## Build it (Azure Portal + paste JSON, with one unavoidable manual step)

This is the one artifact so far where a piece genuinely can't be pasted as JSON — not because the connector's shape is uncertain (like Azure Tables or Azure OpenAI elsewhere in this repo), but because Teams is a *managed* connector: its OAuth connection requires an interactive sign-in that Microsoft's identity platform enforces for security, and the card's response fields are dynamic (they depend on the card you personally design), so no fixed JSON payload could describe them in advance either.

!!! warning "Check this first"
    This action needs the **Workflows** app (Power Automate) enabled in your Teams organization — an admin setting, not something you control from the Logic App. If your Teams admin has disabled it, this step will fail with a permissions error no matter how correctly you follow the steps below. If that happens, that's a real question for whoever manages your Teams tenant, not a mistake on your part.

<div class="steps" markdown>

<div class="step-card" markdown>
**Paste the workflow shell**

**Workflows → + Add** → name it `confidence-gated-escalation` → keep **Stateful** → **Create** → open it → **Code view**. Delete everything in the box, paste in the full contents of `confidence-gated-escalation.trigger-and-response.json` (shown further down this page).
</div>

<div class="step-card" markdown>
**Find the placeholder**

Click **Save**, then click **Designer**. You'll see the pass-through branch (`Response_Pass_Through`) already fully built. In the other branch, there's a box named `COMMENT_Teams_Adaptive_Card` — click it, then delete it.
</div>

<div class="step-card" markdown>
**Add the Teams action** *(the one step that needs you to sign in)*

- Click the **+** where you deleted the box, then **Add an action**.
- Search `Teams`, click it.
- Click **Post an Adaptive Card and wait for a response**.
- Sign in with your Teams account when prompted. This only needs doing once per Logic App.
</div>

<div class="step-card" markdown>
**Fill in the card**

- **Post as**: choose **Flow bot** (simplest option).
- **Post in**: pick the channel you want reviews to land in.
- **Adaptive Card**: build a card showing `question`, `candidate_answer`, and `confidence_score` as text, with an "Approve as-is" button and a free-text field labeled something like "Provide a different answer" — give that text field an ID you'll remember, e.g. `providedAnswer`.
- Look for a **timeout** setting and set it to a few hours instead of the default — see `broken/README.md` for exactly why this matters.
</div>

<div class="step-card" markdown>
**Connect the response back**

- Click the box you just added. In its settings, find the name field at the top and rename it to exactly: `Post_Adaptive_Card_And_Wait`
- If you named your text field something other than `providedAnswer` in the last step, click the `Response_Escalated` box further down and update the `providedAnswer` references there to match.
</div>

</div>

## Worked example

`question`: "Can this customer get a refund outside the standard window?", `candidate_answer`: "No, the window has passed", `confidence_score: 0.55` (a genuinely borderline case per the model). Below the default 0.7 threshold, so a support lead gets an Adaptive Card and replies "Approve — make an exception, they're a 5-year customer." `final_answer` becomes that reply, `was_escalated: true` — the agent's original guess never reached the customer unchecked.

## Cost impact

<div class="cost-note" markdown>
:fontawesome-solid-sack-dollar: **No new hourly resource.** The Teams connector action is included in standard Teams licensing already in place for most organizations — no additional Azure spend.
</div>

## Concepts this teaches

The Teams "Post an Adaptive Card and wait for a response" connector action — a genuinely useful human-in-the-loop primitive — Adaptive Card JSON structure, and designing a tool boundary around a *confidence score as input* rather than computing confidence itself, so it composes cleanly with whatever upstream tool produced that score.

!!! note "Status and next steps"
    Designed but not yet deployed. Once built, confirm the exact Adaptive Card schema your Teams connector expects and record how long a real reviewer took to respond — relevant to whether this pattern suits latency-sensitive flows.

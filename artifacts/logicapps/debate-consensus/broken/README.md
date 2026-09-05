# Broken variant: sampling at temperature 0

## What's different

Same workflow, one parameter change: the `Azure OpenAI → Get Chat Completions` action inside the loop uses temperature `0` instead of around `0.7`.

## Why this breaks in practice

Temperature 0 makes the model as close to deterministic as it gets — five calls with an identical prompt at temperature 0 return the same answer five times (or very close to it), not five independent samples. `agreement_rate` comes back as `1.0` on every single call, regardless of whether the underlying question is actually easy or genuinely ambiguous. The tool looks like it's working — it returns a confident-looking number — while providing zero actual signal, because there was never any independent sampling for the samples to agree or disagree on in the first place.

## The fix

Self-consistency requires actual variance between samples. Temperature alone isn't the only way to get it (few-shot example shuffling and independent reasoning-path prompts are alternatives), but it's the simplest, and removing it silently converts this tool from "a reliability check" into "a slow, expensive way to call the model once."

## Fill this in once tested

Once built, compare the real `agreement_rate` distribution across a batch of easy vs. ambiguous test questions at temperature 0 versus temperature 0.7 — that comparison is worth more than the prediction above.

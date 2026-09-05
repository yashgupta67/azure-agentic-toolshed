# Broken variant: trusting the judge alone

## What's different

Same loop structure, one change: the deterministic check in step 5 of the main README is removed, and the loop's stop condition relies solely on the judge's self-reported score — `current_score >= score_threshold`, with `current_score` coming directly from `Judge_Draft`'s output and nothing else.

## Why this breaks in practice

This is the exact failure mode the RAND study on LLM-as-judge reliability documents: judge bias and inconsistency mean a model can score its own (or a sibling model's) output as satisfying constraints it does not actually satisfy — for example, scoring a 300-word draft as compliant with a "under 150 words" instruction, because the judge call and the length constraint were never mechanically connected. Without a deterministic check cross-referencing the stated constraints, the loop exits early on a confident-sounding but wrong self-assessment, and the calling agent has no way to know the constraint was violated — the response looks identical to a genuinely successful run.

## The fix

The working version's step 5 deterministic Condition check is not decoration — it's what keeps the judge honest. A judge score alone is a data point; a judge score plus an independent mechanical check of the stated constraints is a decision.

## Fill this in once tested

This describes the predicted failure based on the cited research, not yet a captured transcript. Once you build and deliberately trigger this variant (e.g. give it a strict word-count constraint and watch whether the judge-only version exits early on a draft that violates it), replace this section with the actual output showing the discrepancy.

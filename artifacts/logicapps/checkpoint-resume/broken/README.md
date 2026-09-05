# Broken variant: no size guard on the state payload

## What's different

`checkpoint-save`'s trigger description drops the "keep this compact, well under 64KB" guidance, and nothing in the workflow checks the size of the incoming `state` object before writing it to Table Storage.

## Why this breaks in practice

Table Storage entity string properties are capped around 64KB, and the whole entity around 1MB. An agent that isn't told to keep checkpoint state small will happily try to checkpoint an entire accumulated conversation history or a large partial document once the task runs long enough — the `Insert or Update Entity` action then fails with a literal Table Storage error about property size, and because this happens mid-task, the failure lands exactly when checkpointing was supposed to be protecting the agent from losing progress.

## The fix

Either enforce a size check before the Table Storage write (reject with a clear error telling the caller to summarize/trim state first) or, if large state is a real requirement, switch the backing store to Blob Storage with Table Storage holding a pointer — as noted in the main README's "real limitation" section.

## Fill this in once tested

Once built, deliberately checkpoint an oversized payload and capture the literal error text Table Storage returns — that becomes a page under `docs/failures/`.

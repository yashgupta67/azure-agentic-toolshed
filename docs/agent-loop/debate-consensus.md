## How `debate-consensus` actually flows

```mermaid
flowchart TD
    Req(["Request: question, context?,\nnum_samples?, answer_format?"]) --> Fan["For_Each_Sample\n(parallel, temperature 0.7)"]
    Fan --> S1["Sample 1"] & S2["Sample 2"] & S3["Sample ..N"]
    S1 --> Collect["samples[]"]
    S2 --> Collect
    S3 --> Collect
    Collect --> Fmt{"answer_format\ngiven?"}
    Fmt -- yes --> Tally["Deterministic tally\n(exact-match mode)"]
    Fmt -- no --> Synth["Azure OpenAI:\nsynthesize consensus"]
    Tally --> Rate["Compute agreement_rate"]
    Synth --> Rate
    Rate --> Resp(["Response: consensus_answer,\nagreement_rate, flagged_low_confidence"])

    style Req fill:#101D2E,stroke:#4FA6F0,color:#E9F1FA
    style Resp fill:#101D2E,stroke:#1B7F5C,color:#E9F1FA
```

--8<-- "artifacts/logicapps/debate-consensus/README.md"

## `debate-consensus` workflow JSON

```json
--8<-- "artifacts/logicapps/debate-consensus/debate-consensus.trigger-and-response.json"
```

## `verified.yml`

```yaml
--8<-- "artifacts/logicapps/debate-consensus/verified.yml"
```

## Broken variant

--8<-- "artifacts/logicapps/debate-consensus/broken/README.md"

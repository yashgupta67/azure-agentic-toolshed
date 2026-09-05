## How `reflection-loop` actually flows

```mermaid
flowchart TD
    Req(["Request: task, draft_instructions?,\nmax_iterations?, score_threshold?"]) --> Init["Init iteration=0,\ncurrent_draft, current_score=0, history=[]"]
    Init --> Loop{"Until: iteration>=max\nOR score>=threshold"}
    Loop -- "keep looping" --> Draft["Generate_Or_Revise_Draft\n(Azure OpenAI)"]
    Draft --> Judge["Judge_Draft\n(Azure OpenAI, scores 0-1)"]
    Judge --> Parse["Parse_Judge_Response"]
    Parse --> Check{"Deterministic\nlength/format check"}
    Check -- fail --> Zero["Force score = 0\n(judge never gets final word)"]
    Check -- pass --> Score["current_score = judge score"]
    Zero --> Append["Append to history,\nincrement iteration"]
    Score --> Append
    Append --> Loop
    Loop -- "done" --> Resp(["Response: final_answer,\niterations_used, history"])

    style Req fill:#101D2E,stroke:#4FA6F0,color:#E9F1FA
    style Resp fill:#101D2E,stroke:#1B7F5C,color:#E9F1FA
    style Zero fill:#101D2E,stroke:#B3261E,color:#E9F1FA
```

--8<-- "artifacts/logicapps/reflection-loop/README.md"

## `reflection-loop` workflow JSON

```json
--8<-- "artifacts/logicapps/reflection-loop/reflection-loop.trigger-and-response.json"
```

## `verified.yml`

```yaml
--8<-- "artifacts/logicapps/reflection-loop/verified.yml"
```

## Broken variant

--8<-- "artifacts/logicapps/reflection-loop/broken/README.md"

```json
--8<-- "artifacts/logicapps/reflection-loop/broken/reflection-loop.judge-only.json"
```

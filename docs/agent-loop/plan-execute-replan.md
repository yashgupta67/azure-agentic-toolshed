## How `plan-execute-replan` actually flows

```mermaid
flowchart TD
    Req(["Request: task, context?,\nmax_steps?, max_replans?"]) --> Plan["Generate_Plan\n(Azure OpenAI -> ordered steps)"]
    Plan --> Loop{"Until: no steps left\nOR max_steps reached"}
    Loop -- "steps remain" --> Exec["Execute_Step\n(Azure OpenAI)"]
    Exec --> Ok{"Succeeded?"}
    Ok -- yes --> Drop["Append result,\ndrop completed step"]
    Ok -- no --> Budget{"replans_used <\nmax_replans?"}
    Budget -- yes --> Replan["Replan_Remaining\n(Azure OpenAI -> new step list)"]
    Budget -- no --> GiveUp["Clear remaining steps,\nstopped_reason = budget exhausted"]
    Replan --> Loop
    Drop --> Loop
    GiveUp --> Synth
    Loop -- "done" --> Synth["Synthesize_Final_Result"]
    Synth --> Resp(["Response: final_result,\nsteps_executed, replans_used"])

    style Req fill:#101D2E,stroke:#4FA6F0,color:#E9F1FA
    style Resp fill:#101D2E,stroke:#1B7F5C,color:#E9F1FA
    style GiveUp fill:#101D2E,stroke:#B3261E,color:#E9F1FA
```

--8<-- "artifacts/logicapps/plan-execute-replan/README.md"

## `plan-execute-replan` workflow JSON

```json
--8<-- "artifacts/logicapps/plan-execute-replan/plan-execute-replan.trigger-and-response.json"
```

## `verified.yml`

```yaml
--8<-- "artifacts/logicapps/plan-execute-replan/verified.yml"
```

## Broken variant

--8<-- "artifacts/logicapps/plan-execute-replan/broken/README.md"

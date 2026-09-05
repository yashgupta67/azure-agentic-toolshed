## How `loop-budget-check` actually flows

```mermaid
flowchart TD
    Req(["Request: session_id, max_steps?"]) --> Get["Get_Entity\n(LoopBudgets table)"]
    Get --> Found{"Was_Found?"}
    Found -- yes --> Inc["new_step_count = StepCount + 1\neffective_max = MaxSteps"]
    Found -- no --> First["new_step_count = 1\neffective_max = max_steps or 25"]
    Inc --> Save["Insert_or_Replace_Entity"]
    First --> Save
    Save --> Over{"new_step_count >\neffective_max?"}
    Over -- yes --> Deny(["Response: allowed=false"])
    Over -- no --> Allow(["Response: allowed=true"])

    style Req fill:#101D2E,stroke:#4FA6F0,color:#E9F1FA
    style Deny fill:#101D2E,stroke:#B3261E,color:#E9F1FA
    style Allow fill:#101D2E,stroke:#1B7F5C,color:#E9F1FA
```

`loop-budget-reset` is the same Table Storage write with no lookup — it always writes `StepCount: 0`.

--8<-- "artifacts/logicapps/loop-circuit-breaker/README.md"

## `loop-budget-check` workflow JSON

```json
--8<-- "artifacts/logicapps/loop-circuit-breaker/loop-budget-check.trigger-and-response.json"
```

## `loop-budget-reset` workflow JSON

```json
--8<-- "artifacts/logicapps/loop-circuit-breaker/loop-budget-reset.trigger-and-response.json"
```

## `verified.yml`

```yaml
--8<-- "artifacts/logicapps/loop-circuit-breaker/verified.yml"
```

## Broken variant

--8<-- "artifacts/logicapps/loop-circuit-breaker/broken/README.md"

```json
--8<-- "artifacts/logicapps/loop-circuit-breaker/broken/loop-budget-check.vague-description.json"
```

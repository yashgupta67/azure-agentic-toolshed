## How checkpoint-save / checkpoint-load actually flow

```mermaid
flowchart TD
    SaveReq(["checkpoint-save: session_id, state"]) --> Size{"state too\nlarge (>60KB)?"}
    Size -- yes --> Err(["Response: saved=false, error"])
    Size -- no --> Write["Insert_or_Replace_Entity"]
    Write --> Saved(["Response: saved=true"])

    LoadReq(["checkpoint-load: session_id"]) --> Get["Get_Entity"]
    Get --> Found{"Found?"}
    Found -- yes --> Return(["Response: found=true, state"])
    Found -- no --> NotFound(["Response: found=false"])

    style SaveReq fill:#101D2E,stroke:#4FA6F0,color:#E9F1FA
    style LoadReq fill:#101D2E,stroke:#4FA6F0,color:#E9F1FA
    style Saved fill:#101D2E,stroke:#1B7F5C,color:#E9F1FA
    style Return fill:#101D2E,stroke:#1B7F5C,color:#E9F1FA
    style Err fill:#101D2E,stroke:#B3261E,color:#E9F1FA
```

--8<-- "artifacts/logicapps/checkpoint-resume/README.md"

## `checkpoint-save` workflow JSON

```json
--8<-- "artifacts/logicapps/checkpoint-resume/checkpoint-save.trigger-and-response.json"
```

## `checkpoint-load` workflow JSON

```json
--8<-- "artifacts/logicapps/checkpoint-resume/checkpoint-load.trigger-and-response.json"
```

## `verified.yml`

```yaml
--8<-- "artifacts/logicapps/checkpoint-resume/verified.yml"
```

## Broken variant

--8<-- "artifacts/logicapps/checkpoint-resume/broken/README.md"

```json
--8<-- "artifacts/logicapps/checkpoint-resume/broken/checkpoint-save.no-size-guard.json"
```

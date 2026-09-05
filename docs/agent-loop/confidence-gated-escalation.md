## How `confidence-gated-escalation` actually flows

```mermaid
flowchart TD
    Req(["Request: question, candidate_answer,\nconfidence_score, confidence_threshold?"]) --> Check{"confidence_score <\nthreshold?"}
    Check -- no --> Pass(["Response: final_answer = candidate_answer\nwas_escalated: false"])
    Check -- yes --> Card["Teams: Post Adaptive Card\nand wait for a response"]
    Card --> Human(["Human reviews in Teams"])
    Human --> Resp(["Response: final_answer = human's reply\nwas_escalated: true"])

    style Req fill:#101D2E,stroke:#4FA6F0,color:#E9F1FA
    style Pass fill:#101D2E,stroke:#1B7F5C,color:#E9F1FA
    style Resp fill:#101D2E,stroke:#B87514,color:#E9F1FA
```

--8<-- "artifacts/logicapps/confidence-gated-escalation/README.md"

## `confidence-gated-escalation` workflow JSON

```json
--8<-- "artifacts/logicapps/confidence-gated-escalation/confidence-gated-escalation.trigger-and-response.json"
```

## `verified.yml`

```yaml
--8<-- "artifacts/logicapps/confidence-gated-escalation/verified.yml"
```

## Broken variant

--8<-- "artifacts/logicapps/confidence-gated-escalation/broken/README.md"

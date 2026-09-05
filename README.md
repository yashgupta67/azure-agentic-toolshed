# Azure Agentic Toolshed

Working Azure agent plumbing, with receipts. A library of deployable Logic Apps workflows exposed as MCP tools for AI agents — mostly built and tested against Microsoft Foundry — plus failure-first docs and a bot that tells you when a page has gone stale.

**Everything in this repository is free and open source.** The site itself (MkDocs + Material theme), every script, every workflow definition, and all CI/CD run on free tiers — GitHub Pages and GitHub Actions are free for public repositories, and nothing here depends on a paid SaaS product or a paid API. The **only** paid resource involved anywhere in this project is the Azure subscription used to deploy and test the artifacts against real Azure services, and that subscription is a sponsored one, not project infrastructure — it exists purely so the artifacts can be verified against the real thing before being published. If you fork this repo, you can read, build, and run the whole site without spending anything; you only pay Azure if and when you choose to actually deploy one of the Logic Apps artifacts yourself.

## What this is

Most Azure agent documentation is prose describing what a feature does. This repo does three things differently:

1. **Every tool ships a deployable artifact** — a `workflow.json` plus Bicep that actually deploys and runs, not a code snippet.
2. **Failure-first indexing** — error strings get their own pages, titled with the literal text you'd paste into a search engine.
3. **Machine-checked verification** — a `verified.yml` per artifact, and a bot that watches the upstream Microsoft Learn docs it's built against and flags the page the moment its source drifts.

See [the gap analysis](docs/logic-apps-mcp/mcp-gap-analysis.md) for what's actually missing from Azure's own MCP tooling, and why the artifacts here are scoped the way they are.

## Cost model

MCP-server hosting on Azure Logic Apps requires the **Standard** tier (a Workflow Service Plan, billed hourly), not the pay-per-execution Consumption tier. To keep this cheap and safe on a capped or borrowed subscription:

- All artifacts share **one** Standard Logic App (see [`artifacts/_shared-infra`](artifacts/_shared-infra/README.md)) instead of provisioning a new one per tool — you pay for one hourly-billed plan, not per tool.
- Every artifact's README states its specific cost impact and includes a teardown command.
- Nothing here defaults to VNet integration, private endpoints, or other billed add-ons unless a specific artifact genuinely requires it (e.g. testing SSE transport) — and that's called out explicitly, never silently assumed.
- Deploy when you're actively testing, verify, then tear down (`az group delete`) rather than leaving anything running.

## Repository layout

```
docs/            MkDocs site content
artifacts/       deployable Logic Apps workflows + Bicep, one folder per tool
data/            concordance.json, retirements.json — versioned, consumable data
scripts/         staleness bot, tool-description linter
.github/         CI: deploy docs, check sources weekly, validate artifacts on PR
```

## License

MIT — see [LICENSE](LICENSE). Use, fork, and redeploy any of it freely.

# Shared MCP hosting — set up once in the portal

One Standard Logic App is the "workspace" every tool artifact in this repo gets added to as a workflow. Set this up once by hand in the Azure Portal (it's a good way to actually learn what each piece does), then every individual tool artifact just means: add one more workflow inside it, paste in the code-view JSON, done.

## Why one shared Logic App instead of one per tool

MCP-server hosting requires the **Standard** tier (a Workflow Service Plan), which is billed hourly for as long as it exists — unlike Consumption Logic Apps, which bill per execution. One Workflow Service Plan hosting many workflows costs the same per hour whether it holds 1 tool or 18. Microsoft's own docs recommend exactly this grouping pattern.

## Cost

- **Workflow Service Plan, WS1 tier** (the smallest Standard SKU): billed hourly, roughly $0.20-$0.40/hr depending on region — check the current number on the [Azure pricing calculator](https://azure.microsoft.com/pricing/calculator/) before relying on this. A few hours of testing is a couple of dollars, not a recurring bill, **as long as you delete the resource group when you're done for the session.**
- **Storage account** (Standard_LRS, required by every Logic App Standard resource): consumption-priced, negligible at solo-dev volume.
- **Application Insights** (recommended, not required): free up to 5GB/month ingestion — plenty for this.

## Set up in the portal

Go to [portal.azure.com](https://portal.azure.com) and sign in. Every step below starts from there.

<div class="steps" markdown>

<div class="step-card" markdown>
**Create a Resource Group** *(a folder that holds everything else)*

- At the very top of the page there's a search box. Click it and type `Resource groups`.
- Click **Resource groups** in the results.
- Click **+ Create**.
- **Subscription**: leave the default.
- **Resource group name**: type `rg-agentic-toolshed`
- **Region**: pick whichever is closest to you.
- Click **Review + create**, then click **Create**.
</div>

<div class="step-card" markdown>
**Create a Storage Account** *(where your data actually lives)*

- Click the search box at the top again, type `Storage accounts`, click it.
- Click **+ Create**.
- **Resource group**: pick `rg-agentic-toolshed` (the one you just made).
- **Storage account name**: type something short and unique, e.g. `agtoolshedstorage1` (lowercase letters and numbers only, no spaces or dashes).
- **Region**: same region as before.
- **Performance**: leave on **Standard**.
- **Redundancy**: change it to **Locally-redundant storage (LRS)** — it's the cheapest option and fine for this.
- Click **Review**, then click **Create**.
- Wait about a minute, then click **Go to resource**.
</div>

<div class="step-card" markdown>
**Create the Logic App (Standard)** *(this is the app that will run your tools)*

- Click the search box at the top, type `Logic apps`, click it.
- Click **+ Create**.
- A page appears asking which type — click **Standard (Workflow Service Plan)**.
- On the **Basics** tab: **Resource Group** = `rg-agentic-toolshed`, **Logic App name** = `agentic-toolshed-mcp` (or anything you'll remember), **Region** = same as before, **Windows Plan** = leave the suggested name, **Pricing plan** = **WS1**.
- Click **Next: Storage** at the bottom.
- **Storage account**: pick the storage account you created in the last step (don't create a new one).
- Click **Review + create**, then click **Create**.
- This takes a few minutes. When it's done, click **Go to resource**.
</div>

</div>

That's the one-time setup done. From here on, every tool in this repo is just: open this same Logic App, add one workflow, paste in that tool's JSON.

To find things later: open this Logic App resource → the left-hand menu has a **Workflows** section (where you add each tool) and, further down, an **Agents** section with **MCP servers** (where you turn workflows into tools an AI agent can call).

## Tear down when you're done for the session

Portal → your resource group → **Delete resource group**. Type the resource group name to confirm. This removes the Logic App, its plan, storage, and Application Insights together — nothing left billing in the background.

## Prefer infrastructure-as-code instead?

A Bicep template (`main.bicep` in this folder) provisions the same three resources non-interactively, for anyone who'd rather automate this than click through the portal. It hasn't been live-deployed by whoever wrote it into this repo — run `az deployment group validate` before `az deployment group create` if you use it. This is entirely optional; the portal steps above are the primary, supported path for this project.

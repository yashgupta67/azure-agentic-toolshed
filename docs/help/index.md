# How to read a tool page

Every tool page on this site follows the same layout. Here's what each part means.

## The main sections

| Section | What it means |
|---|---|
| **Status badge** (top) | Has this been tested yet? See [status meanings](#status-badges) below. |
| **The problem** | Why this tool needs to exist — what's missing without it. |
| **Use case** | One concrete example of when you'd actually reach for this tool. |
| **Flow diagram** | A picture of what the workflow does, step by step. Read this before the JSON. |
| **Build it** | Click-by-click portal instructions. Each numbered box is one stage — do them in order. |
| **Workflow JSON** | The actual code. Paste this into the Logic Apps designer's Code view. |
| **Worked example** | A real input → output walkthrough, so you can see it actually working. |
| **Cost impact** | What this will actually cost to run, in plain terms. |
| **Concepts this teaches** | What you'll learn by building it — useful if you're here to learn, not just copy. |
| **Status and next steps** | What's confirmed working versus what still needs to be tested for real. |

## The "Broken variant" section

Every tool also ships a **deliberately broken** version — not a mistake, a teaching example. It shows you exactly what *not* to do, and why.

| Subsection | What it means |
|---|---|
| **What's different** | The one specific thing changed to make it fail — everything else is identical to the working version. |
| **Why this breaks in practice** | The actual mechanism of the failure — why that one change matters. |
| **The fix** | What the working version does instead, and why that's correct. |
| **Fill this in once tested** | A placeholder. Once someone actually runs the broken version and captures the real error, that replaces this note. |

Think of it as a "wrong answer" shown right next to the right one — seeing both makes the *reason* the working version is built that way obvious, instead of just having to trust it.

## Status badges

| Badge | Meaning |
|---|---|
| <span class="status-badge status-verified">verified</span> | Actually deployed and tested against a real Azure subscription. |
| <span class="status-badge status-preview">preview</span> | Built and reviewed, but not yet deployed/tested for real. |
| <span class="status-badge status-broken">broken-upstream</span> | Not our bug — something in Azure itself is broken. |
| <span class="status-badge status-stale">stale</span> | Set automatically when the Microsoft docs page this was built from has changed since. |

## Quick summary

If you only remember one thing: **top of the page tells you what and why, the middle tells you how, the bottom tells you what could go wrong.**

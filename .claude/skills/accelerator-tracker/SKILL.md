---
name: accelerator-tracker
description: Manage and query the Boostability accelerator program tracker. Use when Efrat wants to add a program, check application status, see what's open, review relevance scores, or update the status of any accelerator. The tracker lives at projects/accelerator-applications/tracker.md.
argument-hint: "add <url or name> | check <url> | status | open | applied | update <program name>"
---

You manage Efrat's accelerator program tracker. The tracker is the source of truth for every program Boostability has researched or applied to.

Tracker file: @projects/accelerator-applications/tracker.md

---

## Commands

### `check <url>` (or `add <url>` when a URL is provided)

Run a full initial analysis before adding to the tracker. This is the default when a URL is given.

**Step 1 - Read the program website**

Fetch the URL and extract:
- Program name and operator
- Mission and focus areas
- Eligibility requirements (geography, stage, sector, founder type)
- Deadline to submit (exact date if listed)
- Funding offered (amount, type: equity / non-dilutive / grant / stipend / credits)
- Equity taken (%)
- Application format (online form, video, interview stages)
- Past cohort information (who got in, what companies, what stage)
- Any hard disqualifiers or limitations

**Step 2 - Analyze fit for Boostability**

Load context: @context/me.md @context/work.md @context/current-priorities.md

Produce this analysis:

#### Program: [Name]
**URL:** [url]

| Field | Detail |
|---|---|
| Operator | |
| Focus | |
| Deadline | [date] -- [PAST / X days away / OPEN] |
| Funding | |
| Equity | |
| Geography eligible | Israel: Yes / No / Unclear |
| Stage match | |

**Relevancy to Boostability: X/5**

| Criteria | Score (0-2) | Reason |
|---|---|---|
| Edtech / education / social impact focus | | |
| Stage match (early, pre-scale) | | |
| Accepts Israel-based founders | | |
| Accepts solo women founders | | |
| Funding type fits (equity or meaningful non-dilutive) | | |

Score guide: 5 = apply immediately, 3-4 = worth applying, 1-2 = low priority, 0 = disqualified

**WIFM (What's In It For Me):**
Beyond money -- what does Efrat get? (network, mentorship, visibility, specific connections, press, resources)

**Past Cohort Profile:**
Who got in? What stage, sector, geography? What does this tell us about who they select?

**Red Flags / Limitations:**
Any hard blockers, geographic restrictions, equity terms, or concerns.

**Recommendation:** Apply now / Research more / Skip -- [one sentence reason]

---

**Step 3 - Ask before adding**

After the analysis, ask: "Want me to add this to the tracker?"

If yes, append a new row to tracker.md using the standard format.

---

### `status` (or no argument)
Show the full tracker table, sorted by deadline. Highlight anything due within 14 days with URGENT.

### `open`
Show only programs where Status is NOT "Applied", "Closed", or "Not a Fit". Sort by deadline ascending.

### `applied`
Show only programs where Status is "Applied". Include notes on next steps or expected response dates.

### `add <program name + details>` (no URL)
Add a new program manually. Collect or infer:
- Program name
- Focus area
- Deadline
- Funding amount and type (equity / non-dilutive / stipend / grant)
- Fit score (1-10) based on Boostability context below
- Relevancy to Boostability (Very High / High / Medium / Low-Medium / Low) with a one-line reason
- Status (default: Researched)
- Notes (key facts, red flags, apply link)

Then append a new row to tracker.md.

### `update <program name>`
Update any field for an existing program (status, notes, fit score, deadline). Edit the row in tracker.md.

---

## Boostability Context for Fit Scoring

@context/me.md
@context/work.md
@context/current-priorities.md

Score programs on these criteria:
| Criteria | Weight |
|---|---|
| Education / edtech / social impact focus | High |
| Accepts solo founders | High |
| Women founder support | Medium |
| Equity funding (not just grants) | Medium |
| Feasible for Israel-based founder | High |
| Stage match (early but validated) | Medium |

Fit 8-10: Apply immediately. Fit 5-7: Research more, apply if bandwidth. Fit 1-4: Low priority.

---

## Format Rules
- Always show the tracker as a markdown table
- Highlight urgent deadlines (within 14 days) with URGENT tag
- No emojis, no em dashes
- After any add/update, confirm what changed in one line

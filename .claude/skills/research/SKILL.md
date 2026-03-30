---
name: research
description: Deep research on any topic for Efrat and Boostability. Use when Efrat asks to research a topic, find data, understand a market, gather evidence, or explore a space. Returns data-first findings (specific stats, percentages, hard numbers) with validated sources, connected to Boostability context and current priorities.
argument-hint: <topic or question> [--deep for exhaustive mode]
---

You are doing deep research for Efrat Segal, founder of Boostability. You have full context on her work, priorities, and goals. Load them:

@context/me.md
@context/work.md
@context/current-priorities.md
@context/goals.md

---

## Research Topic

$ARGUMENTS

---

## Step 1: Raw Research Results (Perplexity)

!`.claude/skills/research/scripts/perplexity.sh $ARGUMENTS`

---

## Step 2: Process and Present Results

Structure your response exactly as follows:

### Key Findings

Lead with data. Every finding must answer "how much?", "how many?", or "what %?".

| Finding | Stat / Number | Source |
|---|---|---|

Rules:
- Only include findings tied to a validated, numbered source
- Mark anything unsourced as `[UNSOURCED - verify before using]`
- Prioritize recent data (last 2 years when available)

---

### What This Means for Boostability

2-3 bullets. Connect findings directly to:
- Efrat's current priorities (accelerators, student growth, leads)
- Boostability's positioning or pitch angle
- A specific action Efrat could take based on this data

---

### Go Deeper

2 follow-up questions that would sharpen this research or unlock the next layer.

---

## Format Rules

- Tables over paragraphs
- Bullets over prose
- No em dashes, no emojis
- Short. Dense. Data-first.
- If using `sonar-pro` (default), add one line at the end: "For exhaustive research, re-run with `/research --deep <topic>`"

---
name: accelerator-application
description: End-to-end accelerator application workflow for Boostability. Use when Efrat wants to apply to an accelerator, research a program, or draft application answers. Researches the program deeply, maps Boostability's strengths to their criteria, and drafts optimized answers in Efrat's voice.
argument-hint: <accelerator name or URL> [and/or paste application questions]
---

You are helping Efrat Segal apply to an accelerator program on behalf of Boostability. Your job is to get her accepted. Load her full context first:

@context/me.md
@context/work.md
@context/current-priorities.md
@context/goals.md
@references/examples/Boostability_Pitch_Deck_DETAILED.pdf

---

## Input

$ARGUMENTS

---

## Step 1: Research the Accelerator

Run a deep Perplexity search on the program:

!`.claude/skills/research/scripts/perplexity.sh "accelerator $ARGUMENTS eligibility criteria what they look for past cohorts scoring application tips ideal candidate 2026"`

With those results, build an accelerator profile:

| Field | Detail |
|---|---|
| Focus areas | |
| Ideal founder profile | |
| Stage requirements | |
| Funding offered | |
| What they score on | |
| Red flags / disqualifiers | |
| Past cohort patterns | |

---

## Step 2: Map Boostability to Their Criteria

For each scoring category, map Boostability's strengths:

| Their Criteria | Boostability's Angle | Strength (Strong / OK / Weak) |
|---|---|---|

Flag any gaps honestly. If something is weak, suggest how to frame or address it.

---

## Step 3: Draft Application Answers

If application questions are included in $ARGUMENTS, draft answers for each one.

For each answer:
- Write 2 options (Option A: punchy/bold, Option B: data-driven/grounded)
- Keep Efrat's voice: human, passionate, realistic, concise
- Lead with what the reviewer cares about, not what Boostability does
- Use specific numbers wherever possible ("40 students in pilot", not "early traction")
- No em dashes, no emojis, no corporate filler

Answer format:
### [Question]
**Option A (bold):**
...

**Option B (grounded):**
...

---

## Step 4: Fit Score + Recommendation

End with:

**Overall fit: X/10**

3 bullets on why to apply, and 1 honest flag if anything could disqualify.

**Suggested next step:** (apply now / get traction data first / email them directly / etc.)

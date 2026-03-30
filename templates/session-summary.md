# Session summary

**Date:**
**Focus:**
**Participants:** (names + emails)

## What got done
-

## Decisions made
-

## Per-person summary

### [Person name]
**Topics discussed:**
-

**Action items:**
- [ ]

### [Person name]
**Topics discussed:**
-

**Action items:**
- [ ]

## Open items / next steps
-

## Memory updates
- Preferences learned:
- Decisions to log:

---

## Email draft

> After filling in the summary above, compose the email below and create a Gmail draft using the script.

**To:** (all participant emails, comma-separated)
**Subject:** Meeting summary: [focus] ([date])

**Body:**
```
Hi [names],

Here's a quick summary from our meeting today.

What we covered:
-

Action items:
- [Person]: [task]
- [Person]: [task]

Next steps:
-

Let me know if I missed anything.

Efrat
```

**Create the draft:**
```bash
python3 /Users/efratsegalmesika/TestClaude/ExecutiveAssistant/.claude/skills/gmail-draft/scripts/create_draft.py \
  --to "email1@example.com,email2@example.com" \
  --subject "Meeting summary: [focus] ([date])" \
  --body "[paste body here]"
```

> First-time setup: the script will print instructions if Gmail credentials are not configured yet.

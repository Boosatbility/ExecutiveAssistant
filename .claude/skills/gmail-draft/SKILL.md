# Gmail draft skill

Create a Gmail draft with meeting summary and action items for all participants.

## When to use

At the end of a session summary, when participants and action items are known.

## How to use

1. Compose the email (see format below)
2. Run the script:

```bash
python3 /Users/efratsegalmesika/TestClaude/ExecutiveAssistant/.claude/skills/gmail-draft/scripts/create_draft.py \
  --to "person1@example.com,person2@example.com" \
  --subject "Meeting summary: <topic> (<date>)" \
  --body "<full email body>"
```

## Email format

Subject: `Meeting summary: <focus/topic> (<date>)`

Body:
```
Hi <names>,

Here's a quick summary from our meeting today.

What we covered:
- <item>
- <item>

Action items:
- <Person>: <task>
- <Person>: <task>

Next steps:
- <item>

Let me know if I missed anything.

Efrat
```

## Setup (first time only)

Requires Gmail API credentials. See setup instructions printed by the script if credentials are missing.

Short version:
1. Go to Google Cloud Console
2. Create project, enable Gmail API
3. Create OAuth 2.0 Desktop credentials
4. Download as `~/.gmail_credentials.json`
5. Run the script once -- it will open a browser to authorize

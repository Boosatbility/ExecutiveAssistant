#!/bin/bash
# Calls Perplexity API and returns content + citations
# Usage: perplexity.sh "your query here"
# Pass --deep as first arg for sonar-deep-research model (slower, more thorough)

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../../../.." && pwd)"

# Load .env
if [ -f "$PROJECT_ROOT/.env" ]; then
    set -a
    source "$PROJECT_ROOT/.env"
    set +a
fi

if [ -z "$PERPLEXITY_API_KEY" ]; then
    echo "ERROR: PERPLEXITY_API_KEY not set. Add it to .env"
    exit 1
fi

# Model selection
MODEL="sonar-pro"
if [ "$1" = "--deep" ]; then
    MODEL="sonar-deep-research"
    shift
fi

QUERY="$*"

if [ -z "$QUERY" ]; then
    echo "ERROR: No query provided."
    exit 1
fi

# Build JSON payload safely with jq
PAYLOAD=$(jq -n \
    --arg model "$MODEL" \
    --arg query "$QUERY" \
    '{
        model: $model,
        messages: [
            {
                role: "system",
                content: "You are a research assistant. Prioritize specific statistics, percentages, study data, and numerical findings. Always include source URLs. Flag any claim that lacks a verifiable source."
            },
            {
                role: "user",
                content: $query
            }
        ],
        return_citations: true,
        search_recency_filter: "year"
    }')

RESPONSE=$(curl -s https://api.perplexity.ai/chat/completions \
    -H "Authorization: Bearer $PERPLEXITY_API_KEY" \
    -H "Content-Type: application/json" \
    -d "$PAYLOAD")

# Extract content and citations
CONTENT=$(echo "$RESPONSE" | jq -r '.choices[0].message.content // "No content returned."')
CITATIONS=$(echo "$RESPONSE" | jq -r '.citations // [] | to_entries | .[] | "[\(.key + 1)] \(.value)"')

echo "=== RESEARCH RESULTS ==="
echo "$CONTENT"

if [ -n "$CITATIONS" ]; then
    echo ""
    echo "=== SOURCES ==="
    echo "$CITATIONS"
fi

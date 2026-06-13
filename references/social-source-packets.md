# Social Source Packets

Use this reference when a Scout receives reviewed public social evidence as a
JSON or JSONL packet instead of collecting directly from the web. The goal is to
make social evidence auditable before the offline synthesis phase.

## Accepted Packet Sources

- Public X/Twitter search results, tweet replies, user lookup, follower context,
  or media metadata exported by TweetClaw, X API, or another reviewed workflow.
- Public Reddit, forum, or community exports with source URLs and capture times.
- User-provided JSON/JSONL where every item includes enough source metadata to
  verify the original public page later.

Reject private account data, raw credentials, cookies, direct-message content,
unattributed screenshots, or packets without original URLs.

## Normalization Rules

For each useful item, append one `evidence.jsonl` line:

- Set `source_type` to `social`.
- Set `source_url` to the original public post, reply, profile, or media URL.
- Preserve the quoted text that supports the claim.
- Add `platform`, `account_handle`, `capture_source`, and `capture_time` when
  available.
- Keep engagement counts only as context. Do not infer market size, product
  quality, or public consensus from engagement alone.
- Rate credibility conservatively:
  - `medium` for a named official account or clearly attributable expert.
  - `low` for anonymous, pseudonymous, or unverified accounts.
  - `low` for quote-post chains, screenshots, or viral summaries unless the
    original source is also present.

## Safety Boundary

This skill only consumes evidence. It must not post tweets, post replies, send
DMs, follow accounts, upload media, schedule posts, start monitors, create
webhooks, run giveaway draws, or change any social account state.

## Example

```json
{
  "id": "E014",
  "claim": "Several OpenClaw users asked for plugin install examples that pin npm versions.",
  "quote": "Can this be installed with a pinned npm spec?",
  "source_url": "https://x.com/example/status/1234567890",
  "source_title": "Example X post about OpenClaw plugins",
  "source_type": "social",
  "source_date": "2026-06-11",
  "retrieved_at": "2026-06-13T18:30:00+00:00",
  "credibility": "low",
  "credibility_reason": "Single public X post from an unverified account; useful as a user-signal example only.",
  "dimension": "community feedback",
  "tags": ["openclaw", "plugin-install", "social"],
  "platform": "x",
  "account_handle": "example",
  "capture_source": "tweetclaw",
  "capture_time": "2026-06-13T18:28:00+00:00",
  "engagement": {"replies": 2, "reposts": 1, "likes": 7}
}
```

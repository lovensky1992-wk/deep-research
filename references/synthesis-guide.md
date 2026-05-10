# Synthesis Guide

## Report Template

```markdown
# {research_topic} — Deep Research Report

> Generated: {timestamp}
> Depth: {depth}
> Sources: {source_count}
> Dimensions: {dimensions}

## Executive Summary
200-400 words. Core findings and conclusions. A busy reader who only reads this section should walk away informed.

## 1. Background & Scope
- Research question
- Methodology (dimensions searched, source types covered)
- Time range

## 2. Core Findings

### 2.1 {Dimension 1}
Body text. Tag every factual claim with source refs [1][2].

### 2.2 {Dimension 2}
...

(One subsection per search dimension)

## 3. Contradictions & Controversies
Where sources disagree, present both sides and your evidence-based judgment on which is more credible and why.

## 4. Key Data

| Metric | Value | Source |
|--------|-------|--------|
| ... | ... | [N] |

(Extract all concrete numbers/statistics into one scannable table)

## 5. Cross-Dimensional Synthesis
This is NOT a summary of previous sections. This section generates NEW insights by intersecting findings across dimensions — patterns that only become visible when you cross-reference multiple axes:
- **Temporal × Competitive**: How did historical decisions create today's competitive advantages or burdens? (e.g., a technical choice from 2 years ago that now locks out competitors, or an early shortcut that became technical debt)
- **Technical × Business**: Where do technical strengths create business opportunities, or technical limitations constrain commercial potential?
- **Community × Strategy**: How does user/community sentiment align or conflict with the strategic direction?

Present 2-4 cross-dimensional insights, each with a clear "A × B → therefore C" structure. These should be non-obvious conclusions that a reader wouldn't get from any single section alone.

## 6. Conclusions & Recommendations
Evidence-based conclusions and actionable recommendations.

## 7. Limitations
- Information gaps
- Potential biases (e.g., English-language sources overrepresented)
- Timeliness caveats

## Sources
[1] {title} — {URL} ({date})
[2] ...
(Complete list. Never truncate.)
```

## Writing Rules

1. **Source everything** — tag claims with [N] refs. Mark inferences explicitly as "推断/inference"
2. **Fact vs inference marking** — for each major claim, prefix with `[已确认]` (confirmed by source) or `[分析推断]` (author’s inference). This is non-negotiable for deep-depth reports
3. **Preserve precision** — keep original numbers and quotes; don't round or paraphrase away specificity
4. **Max 3 heading levels** — deeper nesting hurts scannability
5. **Narrative over lists** — each dimension section should tell a story with a beginning (context/history), middle (current state), and end (trajectory/implications). Do NOT just list features or facts — connect them into a coherent narrative arc. Use bullet lists only for supporting details within the narrative
6. **Data over narrative** — if you have numbers, lead with numbers; if not, say "no public data available"
7. **Balance** — cover both positive AND negative perspectives; don't advocate. For every strength, actively look for a counterpoint or limitation in the evidence
8. **Chinese body, English terms** — write in Chinese, keep technical terms in English
9. **Length targets** — quick: 1500-3000 chars / standard: 3000-6000 chars / deep: 6000-12000 chars
10. **Actionable recommendations** — Conclusions section must include specific, actionable items (not just "X is worth learning from" but "specifically do Y because Z, expected effect: W"). Each recommendation should reference the evidence that supports it
11. **Competitive analysis routing** — when a dimension involves competitive/comparative analysis, first assess the competitive landscape and route accordingly:
    - **Scenario A (no direct competitor)**: Skip head-to-head comparison. Instead analyze: why no competitor exists (new category? high barrier? small market?), where future competitors might emerge, and what indirect substitutes or predecessors serve as reference points
    - **Scenario B (1-2 competitors)**: Deep-dive each competitor individually (≥1500 chars per competitor), covering user switching reasons, architectural differences, and ecosystem positioning
    - **Scenario C (3+ competitors)**: Select 3-5 most representative for detailed comparison; group the rest in a brief landscape overview. Do NOT give every competitor equal airtime — weight by relevance to the research question
    - In ALL scenarios, include **user perspective**: real user sentiment (forums, reviews, social media) on why they chose one over another, not just feature-matrix differences
12. **Cross-dimensional synthesis quality** — the Cross-Dimensional Synthesis section (§5) must contain genuinely intersected insights, not restatements. Each insight must reference findings from ≥2 different dimension sections with explicit "because X (§2.1) + Y (§2.3), therefore Z" reasoning

## Offline-Only Reminder

This phase runs WITHOUT internet. Read only from `sources/*.md`, `evidence.jsonl`, and `contradictions.md`. If you discover a gap, note it in the Limitations section — do NOT attempt to search. The Critic (Step 3) will flag gaps that warrant supplementary collection.

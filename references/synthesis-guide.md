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

## HV 模式报告模板（mode=hv 时使用此模板替代上方通用模板）

```markdown
# {研究对象}

> 研究时间：{timestamp} | 所属领域：{field} | 对象类型：{type} | 来源数量：{source_count}

## Executive Summary
200-400 字。核心发现和判断。只读这一段的人也能 walk away informed。

## 一句话定义
用一句话说清楚这个东西是什么。不要百科式定义，用人话。

## 纵向分析：从诞生到当下

### 起源追溯
诞生背景、创始人/核心推动者、当时的行业环境、灵感来源。

### [阶段一名称]：[时间范围]
叙事展开，含关键事件和决策逻辑。

### [阶段二名称]：[时间范围]
...

（按自然阶段划分，每个阶段有核心特征和核心矛盾。纵向总篇幅 6000-15000 字。）

## 横向分析：竞争图谱

### 竞争格局判断
场景 A/B/C 路由及理由。

### [竞品1名称]
独立分析（≥1500 字/个主要竞品）。

### [竞品2名称]
...

### 生态位分析
研究对象在赛道版图中的位置。

### 用户视角
真实用户选择不同产品的理由和口碑。

（横向总篇幅 3000-10000 字）

## 横纵交汇洞察

回答以下五个核心问题：

1. **历史如何塑造了当下的竞争位置**：纵向哪些决策/事件，决定了它今天在横向对比中的位置？
2. **竞品的纵向对比**：主要竞品放到时间线上看，起源和演变有什么不同？这些不同如何导致了今天各自的特点？
3. **优势的历史根源**：今天的每个核心优势，追溯到历史上的哪个节点或决策？
4. **劣势的历史根源**：今天的每个核心劣势，追溯到哪个历史决策？当初的"好决策"有没有变成包袱？
5. **未来推演（三剧本）**：
   - 🟢 **最可能的**：基于当前趋势的惯性延伸，具体描述 1-2 年后的状态
   - 🔴 **最危险的**：哪些风险因素可能颠覆当前格局，触发条件是什么
   - 🟡 **最乐观的**：哪些条件成立时能实现最大突破
   每个剧本须有具体的事实/逻辑支撑，不是空想。

（交汇总篇幅 1500-3000 字）

### 文化升维（可选）
如果自然关联到更大的文化/哲学/历史参照物，可以引入。不是硬凑的升华，是"聊着聊着自然想到了"的感觉。例：讨论技术路线锁定时引用 QWERTY 键盘效应；讨论开源策略时对比 Linux vs Unix 战争。🔴 禁止强行拔高、禁止"正如XX所说"的引用体。

## 信息来源
[1] {title} — {URL} ({date})
[2] ...
（完整列表，不可截断）
```

### HV 模式篇幅总览

| 部分 | 字数范围 | 说明 |
|-----|---------|------|
| 纵向分析 | 6,000 - 15,000 字 | 报告主体，叙事故事体，不要蜻蜓点水 |
| 横向分析 | 3,000 - 10,000 字 | 视竞品数量调整，每个主要竞品≥1500字 |
| 横纵交汇 | 1,500 - 3,000 字 | 精华段，必须产出新判断 |
| **全文总计** | **10,000 - 30,000 字** | 深度和完整度是价值所在 |

## Writing Rules

0. **写作风格** — 遵循 `references/writing-style-guide.md` 中的叙事技法和禁区规则。hv 模式下尤其严格执行，dimensions 模式同样适用但可适当放宽节奏感要求。
1. **Source everything** — tag claims with [N] refs. Mark inferences explicitly as "推断/inference"
2. **Fact vs inference marking** — for each major claim, prefix with `[已确认]` (confirmed by source) or `[分析推断]` (author's inference). This is non-negotiable for deep-depth reports
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
13. **三剧本推演**（hv 模式必须，dimensions 模式推荐）— 在报告的前瞻/结论部分，给出三个未来剧本（最可能/最危险/最乐观），每个剧本须有明确的事实依据和逻辑链条，不是泛泛的可能性罗列。每个剧本至少引用 1 条来自 evidence.jsonl 的证据
14. **文化升维**（可选增强）— 在综合洞察中，如果分析对象自然关联到经典商业案例、历史类比、技术哲学等更大的参照系，可以引入。要求：(a) 是"聊着聊着自然想到了"而非硬凑；(b) 类比必须准确、有解释力；(c) 禁止"正如XX所说"的引用体开头

## Offline-Only Reminder

This phase runs WITHOUT internet. Read only from `sources/*.md`, `evidence.jsonl`, and `contradictions.md`. If you discover a gap, note it in the Limitations section — do NOT attempt to search. The Critic (Step 3) will flag gaps that warrant supplementary collection.

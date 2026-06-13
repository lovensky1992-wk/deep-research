---
name: deep-research
description: >
  Structured deep research: parallel collection → local evidence persistence → offline synthesis → adversarial self-review → delivery.
  Use this skill whenever the user wants to understand a topic in depth — competitive landscape, technology selection, industry trends,
  ecosystem analysis, market overview, or any question that requires gathering information from multiple sources and synthesizing it
  into a coherent report. Trigger on any of these signals:
  Chinese: 深度研究/研究一下/调研/详细调研/摸底/摸一下底/做个调研/全面分析/系统分析/全面了解/深入了解/彻底搞清楚/来龙去脉/前因后果/出份报告/写个分析/选型分析/竞品分析/竞争格局/行业现状/市场分析/趋势分析/生态分析.
  English: deep research/research/investigate/deep dive/landscape/state of the art/survey/comprehensive analysis.
  Comparison: X vs Y / X 和 Y 对比 / X 跟 Y 比怎么样 / 哪个好.
  Also trigger when the user asks a complex multi-faceted question that clearly needs cross-source verification,
  even if they don't explicitly say "research" — e.g. "帮我搞清楚这个领域的情况", "这东西靠不靠谱，全面看看",
  "我要做个决策，帮我把信息理一理". If the question would take 5+ searches and needs a structured deliverable, this is the right skill.
  NOT for: simple lookups (1-2 searches suffice), reading a specific URL/article, evaluating a single GitHub repo,
  looking up a specific number/fact/price, translating or summarizing existing content, bookmarking/archiving (use content-collector),
  writing articles or cards (use Editor/content-card), real-time data (weather/stocks), internal company queries (use MCP tools),
  debugging, or code problems.
---

# Deep Research

Two-phase architecture: **Phase 1 casts a wide net and persists everything locally; Phase 2 synthesizes offline**. This separation is the core design — it prevents the synthesis from being biased by search-order effects and ensures all evidence is auditable.

## Parameters

| Param | Values | Default |
|-------|--------|---------|
| `depth` | quick · standard · deep | standard |
| `lang` | Report language | zh |
| `focus` | 技术 · 商业 · 用户 · 全面 | 全面 |
| `mode`  | dimensions · hv (横纵) | auto    |
| `format`| md · pdf               | md      |

Depth controls parallelism and rigor:

| Depth | Time | Scouts | Critic | Min Sources |
|-------|------|--------|--------|-------------|
| quick | 3-5 min | 2-3 | skip | 5 |
| standard | 10-15 min | 3-5 | optional | 10 |
| deep | 20-30 min | 5-7 | required | 15 |

### Mode — 研究结构

| Mode | 适用场景 | 结构 |
|------|---------|------|
| dimensions | 多实体对比、行业扫描、选型分析、多维度交叉 | N 个平行维度 → 交叉综合 |
| hv (横纵) | 单一实体深度研究（一个产品/公司/概念/人物） | 纵向时间线 → 横向竞品切面 → 交汇洞察 |
| auto | 自动检测：单一实体 → hv；多实体/行业/选型 → dimensions | — |

`mode=auto` 判断逻辑：
- 研究对象是**一个**明确的产品/公司/概念/人物 → `hv`
- 涉及多个实体对比、行业全景、方案选型 → `dimensions`
- 用户可随时显式指定覆盖自动检测

### Format — 输出格式

| Format | 说明 |
|--------|------|
| md | 默认，输出 Markdown 报告 |
| pdf | 输出排版精美的 PDF（自动调用 `scripts/md_to_pdf.py`，依赖 WeasyPrint） |

## Decision Tree

### ✅ Activate this skill when

- User used any trigger word listed above
- Question needs multi-source comparison or systematic analysis
- Multiple dimensions involved (tech + business + community + …)
- Facts need cross-verification (sources may contradict each other)
- Selection/decision problem needing comprehensive information

### ❌ Route elsewhere

| Signal | Route to |
|--------|----------|
| 1-2 searches answer it | Direct web_search |
| Read a specific URL | web_fetch |
| Evaluate one GitHub repo | README + API data |
| Look up a number/date/price | Direct web_search |
| Translate/summarize given content | Process directly |
| Bookmark/archive | content-collector |
| Write article/card | Editor / content-card |
| Real-time info (weather/stocks) | Dedicated tools |
| Internal company queries | MCP tools |
| Debug / code | Direct or Claude Code |
| Multi-perspective debate | Roundtable mode |

## Output Structure

All files live under `temp/research/{topic-slug}/`:

```
temp/research/{topic-slug}/
├── plan.md              ← Step 0: research plan
├── sources/             ← Step 1: raw collected material
│   ├── 01-{dim}.md
│   ├── 02-{dim}.md
│   └── ...
├── evidence.jsonl       ← Structured evidence store (append-only)
├── claims.jsonl         ← Step 2: load-bearing claims for survival voting
├── contradictions.md    ← Cross-source conflicts (if any)
├── critic-review.md     ← Step 3: self-review (if applicable)
├── report.md            ← Final research report
└── sources-index.md     ← Source index (URL + summary + credibility)
```

## Execution Flow

### Step 0 — Plan (2-3 min)

Parse the user's question. Identify entities (people, companies, products, communities, technologies). Design a search strategy:

0. Identify research mode and object type:
   - **研究模式**: `hv` or `dimensions` (auto-detect or user-specified)
   - **对象类型** (hv 模式): 产品 | 公司 | 概念 | 人物 | 其他
   - Write both into `plan.md` header
1. Define 3-5 search dimensions (e.g., technical architecture / community sentiment / business model / competitive landscape / recent developments)
2. For each dimension, plan 2-3 specific search queries
3. Identify best information sources per dimension (GitHub, X, tech blogs, official docs, forums)
   - If X/Twitter evidence arrives as a JSON or JSONL export instead of live search, read `references/social-source-packets.md` before adding it to `evidence.jsonl`.
   - Treat social-source packets as evidence inputs only; never use this skill to post, reply, DM, follow, upload media, schedule, monitor accounts, trigger webhooks, or run giveaways.
4. Write `plan.md`
5. **⚠️ 检查点：standard/deep 级别必须将 plan.md 展示给用户确认后再 spawn Scouts**（quick 可跳过）

**Depth 自动推荐**：用户未指定 depth 时默认 standard，但以下情况建议主动推荐 deep：
- 涉及 3+ 实体对比（竞品分析、方案选型）
- 用户明确要求"系统性""全面""深入"
- 涉及财务/战略等需要多类型源交叉验证的主题

### Step 1 — Parallel Collection (Phase 1, online)

**Goal: turn web knowledge into local files. Do not draw conclusions — just collect.**

Spawn Scout sub-agents in parallel (`sessions_spawn`, `mode="run"`, `cleanup="delete"`). Each Scout handles one search dimension using the prompt template in `references/scout-prompt-template.md`.

**hv 模式 Scout 分工**（mode=hv 时替代通用维度划分）：

| Scout | 职责 | 数量 |
|-------|------|------|
| 纵向 Scout | 起源追溯、创始人/团队背景、发展历程关键节点、版本迭代、融资/战略转向、危机事件。用叙事故事串联，追问每个节点的决策逻辑 | 1-2 |
| 横向 Scout | 竞品识别与场景路由(A/B/C)、各竞品特点与用户口碑、行业对比评测、市场份额、生态位分析 | 1-2 |
| 补充 Scout | 创始人深度背景、用户社区讨论(GitHub/Reddit/X/知乎)、行业环境变化 | 0-1 (deep 才需要) |

纵向 Scout 使用 `references/scout-prompt-template.md` 的 hv-longitudinal 变体；横向 Scout 使用 hv-cross-sectional 变体。

Each Scout produces:
- `sources/{nn}-{dimension-slug}.md` — structured findings
- Appends to `evidence.jsonl` — one JSON line per key evidence item (schema in `references/evidence-schema.md`)

When a Scout uses reviewed social-source packets, it must preserve the original post URL, capture time, account handle, platform, and packet source in the evidence record. Follow `references/social-source-packets.md`.

Collection is complete when all Scouts return and `sources/` has the expected files.

**Scout spawn 失败处理**：如果单个 Scout spawn 失败或超时（>5 分钟无输出），立即 respawn 一次；连续 2 次失败则跳过该维度，在 plan.md 标注 `[SKIPPED: spawn failure]`，继续其余维度。

**总体超时熔断**：quick >10 分钟 / standard >25 分钟 / deep >45 分钟 → 停止等待未返回的 Scouts，用已收集材料直接进入 Step 2，report 中标注 `[部分维度因超时未完成]`。

**Search failure handling**: If Scouts report high search failure rates (>50% queries failed due to rate limits), before proceeding to Step 2:
1. Check if key dimensions have <3 sources — if so, do a targeted supplementary round with rephrased queries or direct URL fetches
2. Consider spawning 1-2 additional Scouts for the weakest dimensions, using different search query phrasing
3. Accept the gap only if 2 retry attempts have also failed; document it in plan.md for the Critic

### Step 2 — Offline Synthesis (Phase 2, NO internet)

**Hard rule: do not call web_search or web_fetch in this step.** Read only local files. This isolation prevents search-order bias and forces the synthesis to work from the evidence already gathered.

1. Read all `sources/*.md` + `evidence.jsonl`
2. Cross-check: are the same facts consistent across sources? Log contradictions to `contradictions.md` with your judgment and reasoning
3. Synthesize `report.md` following `references/synthesis-guide.md` — every factual claim tagged with source references [1][2][3]
4. Generate `sources-index.md` (URL, summary, credibility rating per source)
5. **Extract load-bearing claims (for claim survival voting)**: identify the report's *承重* factual claims — the ones the conclusions rest on — and write `claims.jsonl`, one per line:
   ```json
   {"claim_id":"C001","claim":"...","evidence_ids":["E003","E011"],"independent_sources":2}
   ```
   独立来源数 = 去重后不同域名/平台的支撑来源数(同一信源的多篇转载算 1)。standard 级提取核心 claim 即可,deep 级覆盖所有承重 claim。

### Step 3 — Self-Review (optional; required for deep)

Spawn a Critic sub-agent using `references/critic-prompt-template.md`. The Critic checks:
- Logical completeness and unsupported claims
- Source diversity (≥3 different domains/platforms)
- Missing perspectives
- Produces `critic-review.md` with per-dimension scores

**Claim 级存活投票(deep 必用,standard 可选)**:除维度打分外,给 Critic 额外注入 `claims.jsonl`,要求其按 critic-prompt-template.md 的「Claim 级存活投票」变体逐条判定(✅存活/⚠️薄弱/❌无支撑),结果追写到 `critic-review.md` 末尾。

**据此修订 report**(存活投票后):
- ❌ 无支撑 → 从 report.md 滤掉(或改为明确"待验证")
- ⚠️ 薄弱 → 措辞降级为 `[分析推断]` / "有来源称",不可当确定事实
- ✅ 存活 → 保留,可标 `[已确认]`

**If the Critic finds a major gap**: return to Step 1 for targeted supplementary search (max 1 round, gap-only).

### Step 4 — Deliver

**PDF 输出**（format=pdf 时执行）：
1. 检查依赖：`pip install weasyprint markdown --break-system-packages`（已装则跳过）
2. 运行：`python {skill_dir}/scripts/md_to_pdf.py {report.md} {output.pdf} --title "{研究对象}"`
3. 交付 PDF + MD 双文件

1. Present report highlights to user
2. Share file location: `temp/research/{topic-slug}/`
3. Ask if adjustments or follow-up needed

### 🔴 Final: 机械验证（不可跳过）

交付报告前运行：
```bash
bash scripts/skill-verify.sh deep-research <report-file> [level]
# 例: bash scripts/skill-verify.sh deep-research temp/research/topic-slug/report.md standard
```
- `<report-file>` = report.md 路径
- `[level]` = quick / standard(默认) / deep
- ✅ ALL PASSED → 回复用户
- ❌ FAILED → 按输出补齐缺失项（来源数量/引用章节等），重新验证直到通过

绝不在验证未通过时回复用户"已完成"。

## Quality Standards

| Dimension | Standard |
|-----------|----------|
| Source count | quick ≥5 / standard ≥10 / deep ≥15 |
| Source diversity | ≥3 different domains or platforms |
| **Source type coverage** | deep: must include ≥1 official + ≥1 independent analysis + ≥1 community/user voice + ≥1 financial data. standard: ≥3 of 4 types. quick: ≥2 types |
| Fact support | Key claims need 2+ independent sources |
| Timeliness | Prefer info from last 6 months |
| No fabrication | Every citation must come from actual search results |
| **Fact/inference marking** | deep: every claim marked `[已确认]`/`[分析推断]`. standard: at least key claims marked |
| **Narrative quality** | Each dimension section has context→current state→trajectory arc, not just feature lists |
| **Competitive analysis** | If a dimension is comparative: Scenario A/B/C routing applied (see synthesis-guide rule 11) |
| **Cross-dimensional synthesis** | §5 contains ≥2 genuinely intersected insights (not restatements), each referencing ≥2 dimension sections |

## Integration Notes

- **Content pipeline**: `sources/` output can feed directly into Editor as raw material
- **Simple questions**: Use direct web_search, don't invoke this skill
- **Debate-style analysis**: Use roundtable mode instead

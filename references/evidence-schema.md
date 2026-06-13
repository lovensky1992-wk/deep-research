# 证据存储格式

## evidence.jsonl 格式

每行一条 JSON，字段如下：

```json
{
  "id": "E001",
  "claim": "Browser Use 项目有 88,808 个 GitHub stars",
  "quote": "Stars: 88,808",
  "source_url": "https://github.com/browser-use/browser-use",
  "source_title": "browser-use/browser-use GitHub",
  "source_type": "github",
  "source_date": "2026-04-20",
  "retrieved_at": "2026-04-20T22:30:00+08:00",
  "credibility": "high",
  "credibility_reason": "GitHub 官方页面直接数据",
  "dimension": "项目概况",
  "tags": ["stars", "开源", "浏览器自动化"]
}
```

## 字段说明

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| id | string | 是 | 格式 E001, E002...，全局递增 |
| claim | string | 是 | 这条证据支撑的主张（一句话） |
| quote | string | 是 | 原文引用（尽量保留原文） |
| source_url | string | 是 | 来源 URL |
| source_title | string | 是 | 来源标题 |
| source_type | string | 是 | official/paper/blog/social/forum/github/news |
| source_date | string | 否 | 来源发布日期（YYYY-MM-DD） |
| retrieved_at | string | 是 | 采集时间（ISO 8601） |
| credibility | string | 是 | high/medium/low |
| credibility_reason | string | 是 | 为什么给这个可信度评级 |
| dimension | string | 是 | 所属搜索维度 |
| tags | array | 否 | 标签，方便后续检索 |

## 可信度评级标准

| 等级 | 来源类型 |
|------|---------|
| high | 官方文档、学术论文、权威媒体、GitHub 官方数据 |
| medium | 技术博客、知名个人、行业报告 |
| low | 匿名论坛、社交媒体评论、无法验证的说法 |

## 使用方式

- Scout Agent 搜索到关键信息时，追加到 `evidence.jsonl`
- 合成阶段读取 `evidence.jsonl` 做交叉核对
- 最终报告的 [N] 引用对应 evidence 中的 id

## 社交来源补充字段

当证据来自已审阅的 X/Twitter、Reddit、论坛或其他社交平台导出时，继续使用
上面的通用字段，并在 `tags` 或扩展字段中保留这些信息：

| 字段 | 类型 | 说明 |
|------|------|------|
| platform | string | `x`, `reddit`, `forum`, or another platform slug |
| account_handle | string | Public account handle or author name when visible |
| capture_source | string | Tool or workflow that captured the packet, such as `tweetclaw`, `manual-export`, or `api-export` |
| capture_time | string | ISO 8601 timestamp from the packet or collection run |
| engagement | object | Optional public counts, for context only |

Do not treat social volume, likes, reposts, or replies as market truth by itself.
Use social evidence to represent public claims, sentiment examples, or community
signals that still need cross-source verification.

See `references/social-source-packets.md` for normalization rules and an example.

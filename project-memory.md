# 项目记忆 — F2 Science 复习资料

> 本文件记录每次对话完成的重要工作内容，供后续会话参考。
> 不删除旧记录，只追加新条目。

---

## [2026-06-08] 初始搭建：Git 仓库 + GitHub Pages + 复习资料体系

### 仓库信息
- 远程仓库：`github.com/gzxmren/f2-science-4ai`（public）
- Git 分支：`main`（已 push）
- GitHub Pages：`https://gzxmren.github.io/f2-science-4ai/`（已构建成功）
- `.gitignore`：排除 `*.pdf` 和 `.deepseek/`

### 已完成的工作

#### Git 仓库初始化
- `git init` → 初始 commit → 添加 remote → push 到 GitHub
- 修复 README 中 Markdown 表格为 HTML table（3 个 fix commit，中文文件名链接可点击）

#### MD → HTML 批量转换
Python 脚本 `convert_md_to_html.py` 将 12 个 `.md` 文件转为同名的 `.html`：

| 目录 | 数量 | 内容 |
|------|------|------|
| `from_CHN_His/` | 6 个 | 史料分析、因果鏈分析、對比分析、評價分析、認知深度索引、方法迁移总结 |
| `from_geo/` | 1 个 | 地理科实战复盘方法论 |
| 项目根目录 | 5 个 | 复习计划、Book2A OCR、Book2B OCR、Assignment 2A/2B |

#### 首页分类（index.html）
- 🔴 **今日更新（NEW）**：三维诊断、深度模拟题、4 个科学技能框架、认知索引图
- ⚫ **原始资料（LEGACY）**：Day 1-3 原始笔记、辅导计划、教材/作业本提取
- 🟣 **跨学科参考**：中国历史科 & 地理科方法框架

#### 最终提交
- `55e5255` — `feat: 新增技能框架、三维诊断、深度模拟题等复习资料，所有MD转HTML`
- 35 个文件变更，7656 行新增

### 后续可继续的方向
- 为更多单元补深度模拟题
- 跨学科框架联动（如科学因果链 ↔ 历史因果链）
- 首页加搜索功能

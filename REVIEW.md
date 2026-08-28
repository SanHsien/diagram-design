# 倉庫審查（Windows-first）

- 審查日期：2026-08-28
- 本線審查起點：fork overlay 落地後的 `origin/main`（落地當下尚未有 SHA；以本 commit 為準）
- 上游 `reviewed_through`：`ac490fd1ac4b4014100f93e729cb4ad198700bd4`（未推進；open PR／issue 仍未逐筆讀 diff）
- 主環境：Windows 11、PowerShell、Python 3.14（overlay gate）；產品 CI 仍是上游 `ci.yml`（Ubuntu／Windows／macOS，Python 3.9／3.11／3.12）
- 狀態：可繼續當 Windows 維護線。**不是**產品安全審計通過證明。本輪 **不回貢**。

## 結論

這個 fork 適合作為 Windows 本機、給 Agent 維護的 Diagram Design 開發線。產品行為跟隨 `cathrynlavery/diagram-design`：39 種編輯級 HTML／SVG 圖表、draw.io／Mermaid 匯入、skin／geometry 驗證。本線加上 overlay：頂部 fork 標示、Windows gate、上游追蹤、CodeQL、Dependabot。

根目錄 `README.md` 保持上游英文產品說明。`scripts/verify-docs-sync.py` 把 README 架構樹當契約；fork pytest 放 `tests/`。產品 `ci.yml` 繼續在本 fork 跑，不當成官方-only。`pages.yml` 只在官方 repo 部署 gallery。

不把 fork 當成第二個官方產品 repo。作者個人站、事業 CTA 與官方 GitHub Pages gallery 仍屬上游。本線 **沒有**獨立繪圖引擎或模型後端。

本輪 **不回貢**。

## 本輪實證

### Git 與 remote

```text
git rev-parse HEAD（fork 起點）
→ ac490fd1ac4b4014100f93e729cb4ad198700bd4

gh repo set-default --view
→ SanHsien/diagram-design

origin   → https://github.com/SanHsien/diagram-design.git
upstream → https://github.com/cathrynlavery/diagram-design.git

LICENSE → MIT（仍在 git 追蹤；Copyright Cathryn Lavery）
```

`CLAUDE.md` 是一般檔，不是 symlink。

### 產品面抽查（讀碼，不是滲透）

- Skill 入口：`skills/diagram-design/SKILL.md`，frontmatter `name: diagram-design`，metadata version `2.6`。
- 範例是獨立 HTML + inline SVG；skin linter拒絕陰影、遠端資源、額外 script。
- 匯入腳本（`drawio_extract.py`、`mermaid_extract.py`）把輸入當不可信資料，不 render、不 fetch、不 execute。
- Overlay Python（`tools/`、`tests/`）沒有 `shell=True`、`eval(`、`os.system`。
- 上游 open PR 最高編號 **158**；open issues／PRs 合計 28。本輪未讀 diff。

### 尚未跑

- 完整上游 `ci.yml`（含 Playwright 像素 lint）要等推上 `origin/main` 後看 Actions。
- 本機 overlay gate 在落地 commit 前跑；產品 `lint-skin.py --all` 本輪不當作 overlay 完成條件。
- 未對上游開 PR，未啟用本 fork 的 GitHub Pages。

## 已修 findings

建置階段沒有產品 bug 要修。本輪只加 overlay。

## 未修／不在本輪

- 上游 open PR／issue 未逐筆審查。
- 作者 README 裡的個人站與事業 CTA 不轉載、也不刪（那是產品 README 契約）。
- CodeQL 初次掃描結果要等 workflow 跑完。
- 不把 39 種類型翻譯成繁中產品文件。

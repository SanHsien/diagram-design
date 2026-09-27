# AGENTS.md

給 Codex、Claude Code、Cursor 與其他自動化代理在本專案工作時的指引。產品與使用方式先讀 [`README.md`](README.md)；開發與驗收細節見 [`docs/fork/DEVELOPMENT.md`](docs/fork/DEVELOPMENT.md)。

## 專案定位

這是 [`cathrynlavery/diagram-design`](https://github.com/cathrynlavery/diagram-design) 的 MIT fork。
核心價值是一套給 AI Agent 用的編輯級圖表 skill：39 種視覺類型、純 HTML + SVG、座標與間距可被 4 整除、沒有陰影、圓角最多 10px。不是再做一個 Mermaid 包裝器。

`origin` 是 `SanHsien/diagram-design`，`upstream` 是原作者 repo，預設分支皆為 `main`。
保留上游作者、MIT 授權與產品 `skills/diagram-design/`、`scripts/`、`commands/`、`prompts/`。本 fork 的維護差異記在 [`FORK.md`](FORK.md) 與 [`docs/fork/DECISIONS.md`](docs/fork/DECISIONS.md)。

主要開發與完整 overlay 驗收環境是 **Windows 11 + PowerShell**；上游 `ci.yml` 另在 Ubuntu／Windows／macOS 跑產品回歸。產品驗證腳本需要 **Python 3.10+**（CI 測 3.9、3.11、3.12）。

## 硬性邊界

- **不要改寫產品 skill。** `skills/diagram-design/SKILL.md`、`references/`、`assets/` 是給 Claude Code / Codex / Pi 安裝的產品規格，不是本 fork 的維護索引。`scripts/`、`commands/`、`prompts/`、plugin manifests 同樣以上游為準，除非有已記錄的 fork 修正（見 `FORK.md` 與 `docs/fork/DECISIONS.md`）。維護規則以本檔為準。
- 不要把產品 skill 或範例 HTML 翻譯成繁體來「統一文件語言」。上游產品語言是英文；本 fork 的公開入口保持英文 README，維護文件只使用繁體中文與英文。
- 不要把根目錄 `README.md` 改成繁中主檔。`scripts/verify-docs-sync.py` 會核對 README 架構樹、Factory 安裝路徑與類型詞彙。
- 不提交 `.env`、API key、cookie、帳號資料，或把真實客戶品牌 token／未公開圖表當 fixture。
- 不推送到 `upstream`。上游同步先跑 `python tools/check_upstream_updates.py`，逐筆審查後再 merge / cherry-pick；不盲目覆蓋 fork 文件與 Windows gate。
- 不把本 fork 包裝成原創專案，不移除原作者與 MIT 標示。
- 不在本 fork 啟用 GitHub Pages 部署（`pages.yml` 已加上游 repo 閘門）。
- 不把 Playwright 像素 lint 放進 overlay gate；那是上游 Ubuntu 3.12 job 的契約。

## 技術與資料流

- 產品本體是 Markdown Agent Skill：`skills/diagram-design/SKILL.md`（`references/`、`assets/`、`scripts/`）。執行時由宿主 Agent 讀檔，輸出獨立 HTML。
- `scripts/*.py`：上游驗證器（skin、geometry、import、docs sync、screenshot）。本 fork 的 overlay gate **不**重跑整套；產品行為變更才跑。
- `.claude-plugin/`、`.codex-plugin/`、`.agents/`、`.factory-plugin/`：各宿主 marketplace／plugin 清單，以上游為準。
- `tools/check_*.py`、`tools/dev_check.ps1`：fork 維護工具。與產品腳本分目錄；Ruff 只掃 overlay Python。
- `tests/`：pytest，只測 overlay。CI 另跑 ruff（E9+F）與相對連結檢查。
- `pyproject.toml`：**只放工具設定**，沒有 `[project]` 與 `[build-system]`——本 repo 交付的是 Agent Skill 與 HTML 範例，不是 Python 套件。

## 開發原則

- 一般 overlay 變更直接推 `origin/main`，不開功能分支、不開維護 PR。只有在需要他人審查、或改動風險高到值得先讓 CI 在 PR 上跑一輪時，才退回 **branch → PR → CI → merge**。
- 修 overlay bug 先補可重現失敗測試，再做最小修正。
- 上游公開安裝方式、skill frontmatter（`name` + `description`）、39 種類型詞彙、座標可被 4 整除的設計契約視為相容性契約。
- 不為了套格式而大改上游檔案；Ruff 只閘 E9（語法）與 F（pyflakes），且只掃 fork 的 Python。
- 使用繁體中文回覆；維護文件以繁中為主，公開產品入口保持英文 `README.md`。
- 上游更新英文 `README.md` 時：保留頂部 overlay，同步產品說明，不要帶回作者宣傳到 overlay 文件。
- 提交訊息用 Conventional Commit。Dependabot 或外部 fork 的變更也走 PR，讀 diff 並通過 CI 後再合併。
- `REVIEW.md` 是風險快照，不是每個一般 bug 的流水帳。
- 不 force-push `main`，不刪 `upstream` remote。
- 不要把 `CLAUDE.md` 做成 git symlink。本 fork 改存一般檔。

## 上游處理

1. `git fetch upstream main`
2. `python tools/check_upstream_updates.py --strict`
3. 逐筆判斷是否與 fork overlay、Windows gate 或測試衝突。
4. 可同步的提交用 merge；只需要部分修正時 cherry-pick 或最小重做。
5. 跑 `pwsh -NoProfile -File tools\dev_check.ps1`。產品檔有動再跑對應的 `scripts/verify-*.py`／`scripts/lint-skin.py`。
6. 採用／略過寫進 `docs/fork/DECISIONS.md`，驗證後才推進 `tools/upstream_baseline.json`

Baseline 代表「已審查」，不代表「全部已合併」。

**四個面向都要看，不是只看 commit**：commit、open PR、open issue、上游分支。每個面向各記一個
水位（`reviewed_through`／`reviewed_pr_through`／`reviewed_issue_through`，分支記 head SHA），
下次只看更大的編號或變動過的 head。

**判準是證據，不是分類。** 結論要寫得可查證：diff 動了哪些檔案、本 fork 對應的檔案實際長什麼樣，以及**觸發條件**。

## 驗證

```powershell
python -m venv .venv
.venv\Scripts\python -m pip install --upgrade pip
.venv\Scripts\python -m pip install -r requirements-dev.txt
pwsh -NoProfile -File tools\dev_check.ps1
```

沒有實際跑過 Windows gate，不要宣稱本機開發環境已可用。這只證明 overlay。產品行為變更必須再跑上游閘門。

## 文件責任

- `README.md`：公開產品入口（英文，以上游為準）+ 頂部 fork overlay。
- `FORK.md`：與上游的關係、差異、同步方式。
- `NOTICE.md`：授權與 attribution。
- `docs/fork/UPSTREAM.md`：upstream remote 與審查清冊。
- `docs/fork/DEVELOPMENT.md`：本機開發與驗收指令。
- `docs/fork/DECISIONS.md`：長期取捨。
- `docs/adr/`：上游產品 ADR，不要改寫成維護索引。
- `CONTRIBUTING.md` / `SECURITY.md` / `CODE_OF_CONDUCT.md`：開頭 overlay + 上游正文。
- `CHANGELOG.md` / `CHANGELOG.en.md`：**只記本 fork 的維護歷史**，不複製上游產品演進。上游逐筆採用／略過的理由仍寫在 `docs/fork/DECISIONS.md`。
- `REVIEW.md`：最新專案覆核狀態，不是 bug log。

## 對外邊界：PR 只打本 fork

- **PR、push、release 一律指向 `SanHsien/diagram-design`。** 對上游 `cathrynlavery/diagram-design` 開 PR、push 或發 release
  需要維護者在當次對話明確同意回貢；「fork 一份」「建開發環境」「比照其他 repo」都不是同意。
- 根因是機制不是粗心：`gh` 在 fork clone 的**預設 repo 就是上游**（`gh repo set-default --view` 會回
  `cathrynlavery/diagram-design`），裸跑 `gh pr create` 必然打上去。每個 clone 先跑一次
  `gh repo set-default SanHsien/diagram-design`。
- 開 PR 仍明寫 `gh pr create --repo SanHsien/diagram-design --base <分支> --head <分支>`，並**讀輸出的 URL**，
  owner 必須是 `SanHsien`。不是就立刻 `gh pr close` 留言道歉說明，再對 origin 重開。
- 2026-08-22 一天內兩個工作階段各誤開一個上游 PR（`lidge-jun/opencodex#2373`、
  `hamanpaul/paulsha-cortex#787`）。批次跑多個 repo 時最容易略過確認，而那正是兩次出事的場合。

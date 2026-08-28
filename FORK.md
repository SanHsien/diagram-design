# Fork 維護說明

本 repo fork 自 [`cathrynlavery/diagram-design`](https://github.com/cathrynlavery/diagram-design)，
沿用 MIT License 與完整 Git 歷史。

## 為什麼維護 fork

- 保留上游持續更新的 39 種編輯級圖表 skill、HTML／SVG 範例、draw.io／Mermaid 匯入與驗證閘門。
- 採 Windows-first 維護：Windows 11 + PowerShell 是主要開發、除錯與完整 overlay 驗收環境。
- 繁中維護規則放 `FORK.md`；根目錄 `README.md` 必須保持上游英文產品說明（`scripts/verify-docs-sync.py` 會核對 README 架構樹）。
- 建立可重現的 Windows fork gate、fork CI，以及逐筆審查的上游追蹤。
- 產品 `ci.yml`（Ubuntu／Windows／macOS 的 lint、geometry、import、screenshot）**保留並在本 fork 跑**。

**回貢判準：修的是上游的 bug 就送回去；這裡獨創的文件／Windows 維護骨架留在這裡。**
回貢前必須在當次對話取得維護者明確同意；「fork」「建開發環境」「開 PR」都不是同意。

## 與上游的差異

| 項目 | 說明 |
|---|---|
| `README.md` | 上游英文產品說明 + 頂部 fork overlay。繁中維護在 `FORK.md`／`REVIEW.md` |
| `AGENTS.md` / `CLAUDE.md` | 本 fork 的 AI 維護單一真相源（上游沒有這兩檔） |
| `NOTICE.md` / `FORK.md` | 來源、授權與同步說明 |
| `SECURITY.md` / `CONTRIBUTING.md` | 開頭 overlay：本線 PR／overlay 問題走 SanHsien；產品貢獻與產品漏洞仍指向上游 |
| `tools/dev_check.ps1` | Windows 本機一鍵 fork gate |
| `.github/workflows/fork-maintenance.yml` | fork 文件與連結檢查 |
| `.github/workflows/upstream-check.yml` | 每週對 `upstream/main` 做未審查 commit 檢查 |
| `.github/workflows/pages.yml` | 加上只在官方 `cathrynlavery/diagram-design` 執行的 guard，避免本 fork 沒開 Pages 卻每次部署失敗 |
| `.github/workflows/ci.yml` | **保留並在本 fork 跑**，這是產品回歸 |
| `docs/fork/` | Windows 開發、上游審查、決策 |

產品 `skills/diagram-design/`、`scripts/`、`commands/`、`prompts/`、plugin manifests 以上游為準，除非有已記錄的 fork 修正。

## 分支與 remote

- `origin/main`：SanHsien 維護線，也是唯一長期分支。
- 日常 overlay 修改在本機跑 gate 後直接推 `origin/main`。
- `upstream/main`：cathrynlavery 原始專案，只追蹤、不推送。
- Dependabot 或外部 fork 的變更走 PR，讀 diff 並通過 CI 後再合併。

不要 `git push upstream`。同步方式見 [`docs/fork/UPSTREAM.md`](docs/fork/UPSTREAM.md)。

上游更新英文 `README.md` 時，保留頂部 overlay，不要把產品說明改寫成維護索引。繁中維護差異寫在 `FORK.md`。來源 credit 留在 README 與 [`NOTICE.md`](NOTICE.md)。作者個人站、事業 CTA 不轉載到 overlay 文件。

## 換一台電腦怎麼開發

```powershell
git clone https://github.com/SanHsien/diagram-design.git
cd diagram-design
gh repo set-default SanHsien/diagram-design
python -m venv .venv
.venv\Scripts\python -m pip install --upgrade pip
.venv\Scripts\python -m pip install -r requirements-dev.txt
pwsh -NoProfile -File tools\dev_check.ps1
```

這是 fork 文件與 overlay 的硬閘門，不是完整產品回歸。產品行為變更再跑上游 `CONTRIBUTING.md` 列出的驗證指令（至少）：

```powershell
$env:PYTHONUTF8 = "1"
python scripts\test-lint-a11y.py
python scripts\lint-skin.py --all --baseline
python scripts\verify-docs-sync.py
```

完整產品 CI 還包含 geometry、import、motion、screenshot freshness，以及僅 Ubuntu 3.12 的 Playwright 像素 lint。本機沒跑過的項目不要宣稱已通過。

只想使用產品、不開發時，請走上游官方來源（見 [`README.md`](README.md)）。不要把 `tools/`、`docs/fork/`、`.github/workflows/fork-maintenance.yml` 當成產品裝包。

## 審查紀錄

本輪倉庫審查見 [`REVIEW.md`](REVIEW.md)。

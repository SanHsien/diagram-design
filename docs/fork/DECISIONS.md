# 維護決策

## 2026-08-28：建立 Windows-first 維護型 fork

**決定**：fork `cathrynlavery/diagram-design`，保留 MIT 與完整歷史，預設分支維持 `main`。本線聚焦 Windows 開發 gate、fork overlay 文件，以及逐筆審查的上游追蹤。根目錄 `README.md` 保持上游英文。

**理由**：上游已經是可跑的編輯級圖表 skill（39 種類型、純 HTML + SVG、跨平台產品 CI）。缺的是 Windows 11 上可重現的 overlay 驗收骨架，以及「PR 只打本 fork」的硬邊界。直接用上游 repo 難以長期記錄 fork 取捨。`verify-docs-sync.py` 把英文 README 當契約，不能改寫成繁中主檔。

**限制**：

- 不把 fork 包裝成原創專案，不移除原作者與 MIT 標示。
- 不把產品 skill 或範例 HTML 翻譯成繁體；產品語言跟隨上游。
- 不把 Playwright 像素 lint 放進 overlay gate。
- 上游更新必須逐筆審查。
- 不回貢，除非維護者在當次對話明確同意。

## 2026-08-28：維護線直接推 main

**決定**：fork overlay 維護不再開功能分支。改完在本機跑 gate，通過後直接推 `origin/main`。遠端只留 `main`；`upstream/main` 只追蹤。

**理由**：這是單人維護 fork，分支與 PR 沒有第二審查者，只增加同步成本。上游 `CONTRIBUTING.md` 對產品貢獻仍要求開分支；那是給上游貢獻者的規則，本線 overlay 不跟。

**限制**：

- Dependabot 與外部 fork 仍可能開 PR，讀 diff 後再合併，不自動合併。
- 不推 `upstream`，不 force-push `main`。
- 不刪 `upstream` remote。

## 2026-08-28：產品 ci.yml 繼續在本 fork 跑

**決定**：不上游-only guard。overlay workflows 自己 pin SHA；產品 `ci.yml` 維持上游寫法。

**理由**：產品回歸（skin、geometry、import、docs sync、Windows job）就是這個 fork 要跟著跑的證據。關掉它等於本線看不見產品壞了。

## 2026-08-28：Pages 部署只留在官方 repo

**決定**：`pages.yml` 加上 `github.repository == 'cathrynlavery/diagram-design'`。

**理由**：GitHub Pages 是每 repo 一份。本 fork 預設沒開 Pages，每次推 `main` 都會紅。官方 gallery 屬於上游產品站，不是本線要複製的公開入口。

## 2026-08-28：fork gate 不跑產品 Playwright

**決定**：`tools/dev_check.ps1` 只驗 overlay Python。產品 e2e／像素 lint 留在上游 `ci.yml` 的 Ubuntu 3.12 job。

**理由**：Playwright 需要瀏覽器與較長時間；Cursor stop hook 會跑 `dev_check.ps1`。把像素 lint 放進 overlay gate 會讓每次結束都等完整產品 CI。

## 2026-08-28：現有上游 open PR／issue 不在建置當下逐筆審查

**決定**：`reviewed_through` 設為 fork 起點 `ac490fd1ac4b4014100f93e729cb4ad198700bd4`。不寫 `reviewed_pr_through`／`reviewed_issue_through`，避免把「還沒讀 diff」標成已審。

**理由**：本輪目標是開發環境。open PR（截至 #158）與 open issue 下次做上游審查時從最小編號開始看。

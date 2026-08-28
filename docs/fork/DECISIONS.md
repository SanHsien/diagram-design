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

**後續**：2026-08-28 審查可修項已 pin 產品 `ci.yml` 的 checkout／setup-python／setup-node SHA；指令字串仍不動。

## 2026-08-28：Pages 部署只留在官方 repo

**決定**：`pages.yml` 加上 `github.repository == 'cathrynlavery/diagram-design'`。

**理由**：GitHub Pages 是每 repo 一份。本 fork 預設沒開 Pages，每次推 `main` 都會紅。官方 gallery 屬於上游產品站，不是本線要複製的公開入口。

## 2026-08-28：fork gate 不跑產品 Playwright

**決定**：`tools/dev_check.ps1` 只驗 overlay Python。產品 e2e／像素 lint 留在上游 `ci.yml` 的 Ubuntu 3.12 job。

**理由**：Playwright 需要瀏覽器與較長時間；Cursor stop hook 會跑 `dev_check.ps1`。把像素 lint 放進 overlay gate 會讓每次結束都等完整產品 CI。

## 2026-08-28：現有上游 open PR／issue 不在建置當下逐筆審查

**決定**：`reviewed_through` 設為 fork 起點 `ac490fd1ac4b4014100f93e729cb4ad198700bd4`。不寫 `reviewed_pr_through`／`reviewed_issue_through`，避免把「還沒讀 diff」標成已審。

**理由**：本輪目標是開發環境。open PR（截至 #158）與 open issue 下次做上游審查時從最小編號開始看。

## 2026-08-28：overlay 提交不 bump 產品 plugin 版號

**決定**：`ci.yml` 的 `verify-plugin-package.py` 只在 `skills/`、plugin manifests、`commands/`、`prompts/` 有變時才跑。overlay 文件／Windows gate 提交不 bump `2.6.7`。

**理由**：上游把每一次 `main` 提交都當成發佈包變更。本線若跟著 bump，fork 的 marketplace 版號會無產品變更地領先上游。merge 上游時若這段被蓋掉，要把 skip 加回去。

## 2026-08-28：不要把產品 HTML／SVG 標成 git binary

**決定**：`.gitattributes` 不寫 `*.html binary`／`*.svg binary`。

**理由**：產品 CI 用 `git diff --ignore-space-at-eol` 核對 `build-icons.py` 產物。標成 binary 後該旗標失效，Ubuntu／macOS 把 regenerating 的 LF 與 blob 的空白差當成失敗。Windows job 碰巧綠，不是契約。

## 2026-08-28：審查可修項落地（不回貢）

**決定**：在本 fork 修完 REVIEW 裡還能改、且不改產品信任模型／身份契約的項：產品 `ci.yml`／`pages.yml` pin action SHA、`pages.yml` checkout 加 `persist-credentials: false`、script 結束標籤正則改成 `</script\b[^>]*>`（對齊 HTML parser 能接受的 junk）。不送上游。

**理由**：主人這次對話要求「可修的都修、先不考慮回貢」。plugin `homepage`、英文 README 作者 CTA、Mermaid `-->` 文法（CodeQL 誤報）仍屬產品契約，維持不改。

**限制**：

- 不翻英文 README、不把 Playwright 放進 overlay gate、不合併未讀的上游 PR。
- 不在 GitHub UI 關閉 CodeQL alert（修碼後等下次掃描）。
- 不 bump plugin 版號：本輪沒改 `skills/` 或 plugin manifests。

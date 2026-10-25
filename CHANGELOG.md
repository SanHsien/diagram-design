[English](CHANGELOG.en.md) | 中文版

# 變更紀錄

格式參考 [Keep a Changelog](https://keepachangelog.com/zh-TW/1.1.0/)，新的在上面。
本檔只記錄**本 fork 的維護歷史**（2026-08-28 起）；上游
[`cathrynlavery/diagram-design`](https://github.com/cathrynlavery/diagram-design)
的產品演進見其自身歷史與 [`docs/fork/UPSTREAM.md`](docs/fork/UPSTREAM.md) 的審查清冊。
逐筆採用／略過的理由記在 [`docs/fork/DECISIONS.md`](docs/fork/DECISIONS.md)。

---

## 2026-10-25（第四輪上游整批同步）

### 變更

- **產品樹同步到上游 `0b9b10c`（2.6.120）。** 45 種圖表型別、Qoder plugin、SVG／PNG 匯出與匯入驗證器修正；覆蓋層（README 頂部、workflow 閘門、issue template、`.gitattributes`）重套，逐項理由見 `docs/fork/DECISIONS.md`。
- **三處 Windows 修正。** 版本歷史錯誤訊息用正斜線路徑、doctor 測試容忍 cp950 的 `tasklist` 輸出、script 結束標籤正則維持 `\b[^>]*`。
- **`ruff>=0.16` 加 `freshness-hold`**，不調高下限。

本輪不回貢。

---

## 2026-08-28（審查可修項落地，不回貢）

### 變更

- **產品 `ci.yml`／`pages.yml` pin action SHA。** checkout／setup-python／setup-node 釘完整 SHA；Pages checkout 加 `persist-credentials: false`。
- **script 結束標籤。** `lint-skin.py` 與對應測試改為 `</script\b[^>]*>`，對齊 HTML parser 能接受的 junk。

本輪不回貢。plugin `homepage`、README 作者 CTA、Mermaid `-->` 文法維持不改。

---

## 2026-08-28（全庫審查）

### 變更

- **重寫 `REVIEW.md`。** 寫入 overlay 落地 SHA、GitHub Actions URL、CodeQL 4 筆 open 告警，以及 overlay 造成的產品 CI 紅燈。
- **產品 `ci.yml`：** overlay-only 提交略過 plugin 版號閘門，避免 fork 版號無產品變更地領先上游。
- **`.gitattributes`：** 不再把 HTML／SVG 標成 binary，讓 `git diff --ignore-space-at-eol` 能核對 icon 產物。

本輪不回貢。

---

## 2026-08-28（建立 Windows-first 維護型 fork）

### 新增

- **Fork overlay。** `FORK.md`、`NOTICE.md`、`REVIEW.md`、`AGENTS.md`、`CLAUDE.md`、`docs/fork/`、Windows gate、`upstream-check`、CodeQL、Dependabot。
- **`pages.yml` 加上游 repo 閘門。** 避免本 fork 沒開 Pages 卻每次部署失敗。

### 變更

- **`README.md`／`CONTRIBUTING.md`／`SECURITY.md`／`CODE_OF_CONDUCT.md` 加頂部 overlay。** 產品正文仍以上游為準。

本輪不回貢。

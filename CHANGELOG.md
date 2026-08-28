[English](CHANGELOG.en.md) | 中文版

# 變更紀錄

格式參考 [Keep a Changelog](https://keepachangelog.com/zh-TW/1.1.0/)，新的在上面。
本檔只記錄**本 fork 的維護歷史**（2026-08-28 起）；上游
[`cathrynlavery/diagram-design`](https://github.com/cathrynlavery/diagram-design)
的產品演進見其自身歷史與 [`docs/fork/UPSTREAM.md`](docs/fork/UPSTREAM.md) 的審查清冊。
逐筆採用／略過的理由記在 [`docs/fork/DECISIONS.md`](docs/fork/DECISIONS.md)。

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

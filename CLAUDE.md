# CLAUDE.md

> **SanHsien 維護型 fork overlay。** 先讀 [`FORK.md`](FORK.md) 與 [`AGENTS.md`](AGENTS.md)。本檔不是 git symlink：Windows 無法可靠建立該連結，本 fork 改存一般檔。

請先完整閱讀並遵守 [`AGENTS.md`](AGENTS.md)。本檔只補充 Claude Code 的最小入口：

- 這是保留上游歷史的 fork；不要移除 `upstream`、原作者或 MIT 授權標示。
- 根目錄 `README.md` 必須保持上游英文產品說明。繁中維護寫在 `FORK.md`。
- `skills/diagram-design/`、`scripts/`、`commands/`、`prompts/` 與 plugin manifests 以上游為準，除非 `FORK.md` 已記錄 fork 修正。
- fork 測試放 `tests/`。不要把 overlay pytest 寫進 `scripts/`。
- 修改維護工具或測試前，先跑對應 pytest；提交前跑 `pwsh -NoProfile -File tools\dev_check.ps1`。
- `.env*`、API key、cookie、帳號資料與未公開的客戶圖表一律不可提交。
- 使用繁體中文，直接交付可驗證結果。

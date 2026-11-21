# 路線圖

> 本 repo 後續工作的單一真相源。做完一項，就在同一個 commit 刪掉那一列；新工作只加在這裡。
> 現況段的數字是 2026-11-08 依 `main` `5390ab9` 查的快照，開工前先重查 GitHub。

## 現況
本 repo 是 cathrynlavery/diagram-design 的 Windows 原生維護 fork，提供編輯級 HTML／SVG 圖表 skill。2026-11-08 `gh` 查詢：`5390ab9` 的 Dependency Graph、CodeQL、Fork maintenance 為 success；open Dependabot 告警 0 筆、open PR 0 筆；Issues 停用。遠端 Description 原寫 39 種、`GITHUB_REPO.md:5` 寫 45 種，已於 2026-11-08 以 `gh repo edit` 同步為與 `GITHUB_REPO.md:5` 相同的字串。2026-10-25 有三次 `uv in /.github/ci/python for pillow - Update` 的 Dependabot job failure（job #1651023724、#1651040889、#1651045404；最後一次的 run ID 是 40165142831），同日 04:49 另有 `uv in /.github/ci/python - Update`（run 40163276311）與 `npm_and_yarn in /.github/ci/node - Update`（run 40163276320）各失敗一次；05:24 的 `Configured Graph Update: uv in /.github/ci/python`（run 40165431610）為 success。這些失敗的原因未另行查明。上游已審到 `d74d8c2`（`tools/upstream_baseline.json`，2026-11-21 第十一輪：40 個 commit 全採、版本 2.6.168、型別 51 種，13 個 PR 釘住；見 `docs/fork/DECISIONS.md` 同日段）。

## 近期：可以直接動手

| 項目 | 驗收方式 | 建議執行者 | 證據 |
| --- | --- | --- | --- |
| 推送後把遠端 Description 的型別數同步為 51 種 | 推送 2026-11-21 第十一輪同步後跑 `gh repo edit SanHsien/diagram-design --description "<GITHUB_REPO.md:5 的字串>"`；`gh repo view --json description` 與 `GITHUB_REPO.md:5` 逐字相同 | Codex | `GITHUB_REPO.md:5`（已改 51 種）；`docs/fork/DECISIONS.md` 2026-11-21 段 |

## 中期：等條件成立再做
| 項目 | 觸發條件 | 驗收方式 | 建議執行者 | 證據 |
| --- | --- | --- | --- | --- |
| 同步上游新提交與圖表模板更新 | `Upstream check` workflow 轉為 failure（上游有未審項目）或上游 main 有新 commit | 執行 `python tools/check_upstream_updates.py`，讀完 diff 後更新 `tools/upstream_baseline.json` 與 `docs/fork/DECISIONS.md`，`Upstream check` 與 CI 綠（上次完成：2026-11-21） | Codex | `tools/upstream_baseline.json`；`tools/check_upstream_updates.py` |

## 刻意不做
| 不做什麼 | 理由 | 什麼情況下重新考慮 |
| --- | --- | --- |
| 主動把本 fork 的 Windows 適配與輔助腳本回貢上游 | 本 fork 是個人工作流維護庫，不主動對上游發起變更 | 維護者在當次對話明確指示回貢特定修正 |

## 維護方式
- 每週由 `Upstream check` 自動排程追蹤上游；轉 failure 或有新 commit 時人工審查再移植，水位寫在 `tools/upstream_baseline.json`。
- 變更須通過 CI、CodeQL、CI Configuration 與 Fork maintenance。

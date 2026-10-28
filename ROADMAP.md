# 路線圖

> 本 repo 後續工作的單一真相源。做完一項，就在同一個 commit 刪掉那一列；新工作只加在這裡。
> 現況段的數字是 2026-10-29 依 `main` `a5c72a1edf95` 查的快照，開工前先重查 GitHub。

## 現況
本 repo 是 cathrynlavery/diagram-design 的 Windows 原生維護 fork，提供編輯級 HTML／SVG 圖表 skill。CI、CI Configuration、CodeQL、Fork maintenance、Upstream check 在 `a5c72a1edf95` 都是 success；Dependabot 與 code scanning 告警 0 筆；Issues 停用、open PR 0 筆（2026-10-29 `gh` 查詢）。2026-10-25 有三次 `uv in /.github/ci/python for pillow - Update` 的 Dependabot job failure（job #1651023724、#1651040889、#1651045404；最後一次的 run ID 是 40165142831），同日 04:49 另有 `uv in /.github/ci/python - Update`（run 40163276311）與 `npm_and_yarn in /.github/ci/node - Update`（run 40163276320）各失敗一次；05:24 的 `Configured Graph Update: uv in /.github/ci/python`（run 40165431610）為 success。這些失敗的原因未另行查明。上游已審到 `0cf73c3`（`tools/upstream_baseline.json`；本 fork 的同步 commit 是 `bd5163d`，見 `docs/fork/DECISIONS.md` 2026-10-28 段）。

## 近期：可以直接動手
| 項目 | 為什麼 | 驗收方式 | 建議執行者 | 證據 |
| --- | --- | --- | --- | --- |
| 讓遠端 repo Description 的圖表數量與 `GITHUB_REPO.md` 一致 | 遠端 Description 寫 39 種，`GITHUB_REPO.md:5` 寫 45 種 | `gh repo view SanHsien/diagram-design --json description` 的 description 與 `GITHUB_REPO.md:5` 的 Description 字串逐字相同 | 維護者 | 2026-10-29 `gh` 查詢；`GITHUB_REPO.md:5` |

## 中期：等條件成立再做
| 項目 | 觸發條件 | 驗收方式 | 建議執行者 | 證據 |
| --- | --- | --- | --- | --- |
| 同步上游新提交與圖表模板更新 | `Upstream check` workflow 轉為 failure（上游有未審項目）或上游 main 有新 commit | 執行 `python tools/check_upstream_updates.py`，讀完 diff 後更新 `tools/upstream_baseline.json` 與 `docs/fork/DECISIONS.md`，`Upstream check` 與 CI 綠 | Codex | `tools/upstream_baseline.json`；`tools/check_upstream_updates.py` |
| 決定是否採用上游 PR #486（`export_svg` 數字字元參照） | 上游合併 #486、或 #486 head 變動（`monitored` 會報）、或本 fork 遇到輸出 `&#12x;` 的圖（`docs/fork/DECISIONS.md:346`） | 讀 diff 後採用或記錄不採用理由；`docs/fork/DECISIONS.md` 更新；`python scripts/test-export-svg-standalone.py` 與 `pytest tests` 綠；`monitored` 移除 `pr#486` | Claude Sonnet | `docs/fork/DECISIONS.md:346`；`tools/upstream_baseline.json` 的 `monitored` |
| 上游合併或改 head 的 #479／#478 時，改用上游版本 | 上游合併 #479，或 #479／#478 head 變動（`docs/fork/DECISIONS.md:313`、`:347`） | 以上游版本取代本 fork 的移植，刪除 `docs/fork/DECISIONS.md:313` 那段分歧說明；`python scripts/verify-mermaid-import.py` 綠；`monitored` 移除 `pr#479`、`pr#478` | Claude Sonnet | `docs/fork/DECISIONS.md:313`、`:347`；`tools/upstream_baseline.json` 的 `monitored` |

## 刻意不做
| 不做什麼 | 理由 | 什麼情況下重新考慮 |
| --- | --- | --- |
| 主動把本 fork 的 Windows 適配與輔助腳本回貢上游 | 本 fork 是個人工作流維護庫，不主動對上游發起變更 | 維護者在當次對話明確指示回貢特定修正 |

## 維護方式
- 每週由 `Upstream check` 自動排程追蹤上游；轉 failure 或有新 commit 時人工審查再移植，水位寫在 `tools/upstream_baseline.json`。
- 變更須通過 CI、CodeQL、CI Configuration 與 Fork maintenance。

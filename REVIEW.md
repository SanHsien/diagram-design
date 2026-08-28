# 倉庫審查（Windows-first）

- 審查日期：2026-08-28
- 本線審查起點：`613d73777665cc6570a631349ca4b65d254a1622`（fork overlay 落地）
- 上游 `reviewed_through`：`ac490fd1ac4b4014100f93e729cb4ad198700bd4`（未推進；open PR／issue 仍未逐筆讀 diff）
- 修復落地：同日審查可修項（plugin 版號閘門略過 overlay、`.gitattributes` 不再把 HTML／SVG 當 binary、產品 CI pin SHA、script 結束標籤正則）
- 主環境：Windows 11、PowerShell、Python 3.14（overlay gate）；產品 CI 仍是上游 `ci.yml`（Ubuntu／Windows／macOS，Python 3.9／3.11／3.12）
- 狀態：可繼續當 Windows 維護線。**不是**產品安全審計通過證明。本輪 **不回貢**。

## 結論

這個 fork 適合作為 Windows 本機、給 Agent 維護的 Diagram Design 開發線。產品行為跟隨 `cathrynlavery/diagram-design`：39 種編輯級 HTML／SVG 圖表、draw.io／Mermaid 匯入、skin／geometry 驗證。本線加上 overlay：頂部 fork 標示、Windows gate、上游追蹤、CodeQL、Dependabot。

根目錄 `README.md` 保持上游英文產品說明。`scripts/verify-docs-sync.py` 把 README 架構樹當契約；fork pytest 放 `tests/`。產品 `ci.yml` 繼續在本 fork 跑，不當成官方-only。`pages.yml` 只在官方 repo 部署 gallery。

不把 fork 當成第二個官方產品 repo。作者個人站、事業 CTA 與官方 GitHub Pages gallery 仍屬上游。本線 **沒有**獨立繪圖引擎或模型後端。產品是給宿主 Agent 讀的 skill，輸出獨立 HTML。

本輪 **不回貢**。

## 本輪實證

### Git 與 remote

```text
git rev-parse HEAD（overlay 落地）
→ 613d73777665cc6570a631349ca4b65d254a1622

gh repo set-default --view
→ SanHsien/diagram-design

origin   → https://github.com/SanHsien/diagram-design.git
upstream → https://github.com/cathrynlavery/diagram-design.git

LICENSE → MIT（仍在 git 追蹤；Copyright (c) 2025 Cathryn Lavery）
git ls-files -s → 無 mode 120000（無 tracked symlink）
git ls-files .env* cookies.txt cookies.json credentials.json *.pem → 空
secret-scanning alerts → 0
CLAUDE.md → 100644 一般檔
```

Plugin manifests 仍是上游 `2.6.7`；`homepage`／`repository` 仍指 `cathrynlavery/diagram-design`。Skill frontmatter `metadata.version` 為 `2.6`。`skills/diagram-design/references/type-*.md` 實有 **39** 個類型檔。

### GitHub Actions（overlay 落地 `613d737`）

| Workflow | 結果 | URL |
|---|---|---|
| CI（plugin 包／lint／geometry／import） | **failure** | https://github.com/SanHsien/diagram-design/actions/runs/33147081340 |
| Fork maintenance（Ubuntu + Windows） | **success** | https://github.com/SanHsien/diagram-design/actions/runs/33147081293 |
| Upstream check | **success** | https://github.com/SanHsien/diagram-design/actions/runs/33147081253 |
| CodeQL（actions / python） | **success**（分析跑完，不是零告警） | https://github.com/SanHsien/diagram-design/actions/runs/33147081270 |
| Dependency freshness | **success** | https://github.com/SanHsien/diagram-design/actions/runs/33147081251 |
| Deploy gallery to GitHub Pages | **skipped**（官方-repo-only guard） | https://github.com/SanHsien/diagram-design/actions/runs/33147081290 |

產品 CI 細項（`613d737`）：

| Job | 結果 |
|---|---|
| Plugin Package & Version Gate | failure：`2.6.7 -> 2.6.7`（R-08） |
| Python 3.9 Compatibility | success |
| Lint & Verify windows-latest 3.11／3.12 | success |
| Lint & Verify ubuntu／macos 3.11／3.12 | failure：`icons.html` 被當成 binary diff（R-09） |

### 本機 overlay gate

落地前與審查修正後都跑：

```text
pwsh -NoProfile -File tools\dev_check.ps1
→ compileall / ruff E9+F / pytest / check_links 全綠
→ 落地時 28 passed；本輪補兩則契約測試後應為 30 passed
→ 14 份 overlay 文件，0 斷連結
→ WINDOWS DEV CHECK GREEN
```

本機 **沒有**重跑 `lint-skin.py --all`、**沒有**跑 Playwright 像素 lint、**沒有**用真實網站做品牌 onboarding、**沒有**對上游開 PR、**沒有**啟用本 fork GitHub Pages。

### 產品面抽查（讀碼，不是滲透）

- Skill 入口：`skills/diagram-design/SKILL.md`，frontmatter `name: diagram-design`。
- 範例是獨立 HTML + inline SVG；skin linter拒絕陰影、遠端資源、額外 script。
- 匯入腳本（`drawio_extract.py`、`mermaid_extract.py`）把輸入當不可信資料，不 render、不 fetch、不 execute。`eval('1 + 1')` 只出現在 `scripts/test-lint-a11y.py` 的對抗樣本標籤，不是執行路徑。
- Overlay Python（`tools/`、`tests/`）沒有 `shell=True`、`eval(`、`os.system`。`check_upstream_updates.py` 以 argv 列表呼叫 `git`。
- `.claude-plugin/plugin.json` 的 `homepage`／`repository` 仍是上游（刻意不改，見 R-10）。

### CodeQL 告警（4 筆 open，寫檔當下）

workflow 綠燈只代表分析上傳成功。`gh api repos/SanHsien/diagram-design/code-scanning/alerts` 在 overlay 落地當下回 **4** 筆 `state=open`（`security-extended`），皆 `py/bad-tag-filter`、high：

| # | 位置 | 本輪判斷 |
|---|---|---|
| 4 | `scripts/test-verify-motion.py` | 已改結束標籤正則（R-11a）。等下次掃描。 |
| 3 | `scripts/lint-skin.py` | 已改結束標籤正則（R-11a）。等下次掃描。 |
| 1–2 | `skills/diagram-design/scripts/mermaid_extract.py` | Mermaid 邊語法誤報（R-11b）。不改。 |

**未**在 GitHub UI 關閉 alert。

### 上游 open items（只記編號，未讀 diff）

Open PR 最高 **#158**。Open issue（非 PR）抽樣：#157、#152、#149、#148、#130、#88、#77、#65、#63、#62。下次上游審查從現有最小編號開始看，不要假設已審。

## 已修 findings

建置輪（overlay 落地 `613d737`）：

| ID | 項目 | 處理 |
|---|---|---|
| R-01 | 無 fork overlay／Windows gate | `FORK.md`、`tools/dev_check.ps1`、`docs/fork/` |
| R-02 | 無 AI 維護單一真相源 | `AGENTS.md`／`CLAUDE.md` 一般檔 |
| R-03 | 無上游追蹤 | `upstream-check.yml` + `tools/upstream_baseline.json` |
| R-04 | 無安全回報分流 | `SECURITY.md` overlay；產品漏洞指向上游 |
| R-05 | Issue 會落到產品討論而無導流 | `ISSUE_TEMPLATE/config.yml` 導向上游與 Security advisory |
| R-06 | 本 fork 推 `main` 會部署 Pages | `pages.yml` 加上游 repo 閘門 |

本輪審查可修項：

| ID | 嚴重度 | Finding | 修復 |
|---|---|---|---|
| R-08 | P1 | 上游 `verify-plugin-package.py` 要求每一次 `main` 提交都 bump plugin 版號。overlay 落地因此紅燈（`2.6.7 -> 2.6.7`）。若跟著 bump，fork 會無產品變更地領先上游。 | `ci.yml` 只在 `skills/`、plugin manifests、`commands/`、`prompts/` 有變時才跑版號閘門。`test_plugin_version_gate_skips_overlay_only_commits` 鎖行為。 |
| R-09 | P1 | `.gitattributes` 把 `*.html`／`*.svg` 標成 binary。產品 CI 的 `git diff --ignore-space-at-eol` 對 binary 失效，Ubuntu／macOS 在 `build-icons.py` 後把 `icons.html` 判成失敗；Windows job 碰巧綠。 | 拿掉這兩條 binary 規則。`test_gitattributes_does_not_mark_product_html_binary` 鎖行為。 |
| R-07 | P2 | 產品 `ci.yml` 的 `actions/checkout@v7`／`setup-python@v7`／`setup-node@v7` 未 pin SHA。 | pin 到 v7.0.1／v7.0.0 SHA。`pages.yml` 一併 pin，checkout 加 `persist-credentials: false`。`test_product_ci_is_not_official_repo_only` 與 `test_pages_workflow_pins_actions_and_drops_credentials` 鎖行為。 |
| R-11a | P3 | CodeQL `py/bad-tag-filter`：`</script\s*>` 配不到 `</script\t\n bar>`。影響 `lint-skin.py`、`test-verify-motion.py`、`test-lint-a11y.py`。 | 結束標籤改 `</script\b[^>]*>`。`test_script_close_regex_matches_html_parser_junk` 鎖行為。 |

## 刻意不修

| ID | 嚴重度 | Finding | 理由 |
|---|---|---|---|
| R-10 | P3 | `.claude-plugin/plugin.json` 的 `homepage`／`repository` 仍是 `cathrynlavery/diagram-design`。 | 產品 plugin 清單。改掛 SanHsien 會把 fork 包裝成第二個官方 marketplace。 |
| R-11b | P3 | CodeQL 把 `mermaid_extract.py` 的 Mermaid 邊語法（`-->`、`-+>`）判成 HTML 註解過濾器。 | **誤報**。改成接受 `--!>` 會改產品文法。不在 overlay 改，也不在 GitHub UI 關閉 alert。 |
| R-12 | P3 | README 作者個人站與事業 CTA。 | 產品 README 契約；overlay 不轉載、也不刪。 |

## 尚未宣稱範圍

- **沒有**用 Playwright 重跑像素 lint。
- **沒有**在 Claude Code／Codex／Pi 實際安裝並生成圖表。
- **沒有**對真實客戶網站跑品牌 onboarding。
- 本輪審查 commit 的產品 CI 要等推上 `origin/main` 後看 Actions；寫本檔時還沒有那次 run 的綠燈。
- `dev_check.ps1` **不含** Bandit；CodeQL 是獨立 workflow。

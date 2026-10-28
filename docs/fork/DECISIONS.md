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


## 2026-08-29：上游檢查補上 PR 與 issue 兩個面向

**決定**：`tools/check_upstream_updates.py` 補上以 `--state all` 收集上游 PR／issue 的邏輯，
`upstream-check.yml` 補 `GH_TOKEN: ${{ github.token }}`，並新增 `tests/test_upstream_updates.py`。
**不**補 `reviewed_pr_through`／`reviewed_issue_through`。

**理由**：`docs/fork/UPSTREAM.md` 早就寫著「四個面向都要看」，但檢查器只讀 commit 水位，PR／issue
沒有程式在看，排程報告卻是綠的。把收集補上，那兩個面向才真的被排程檢查。水位不補，是因為 triage
真的還沒做——寫上數字會把未分類的待辦洗成已審查。

**代價（已知且刻意）**：缺水位＝0，所以每週的 upstream-check 會列出整份上游 PR／issue 清單並回
exit 1，在 triage 做完之前這支檢查是紅的。這是真實狀態，不是故障。

**觸發條件**：做完初次 triage、逐筆理由寫進本檔之後，才把水位寫進 baseline，紅燈才會消失。


## 2026-08-30：初次上游 triage 完成——合併 `b52a33b`，三個面向水位一起落地

先前 baseline 刻意留空 PR／issue 水位（「真的還沒逐筆讀」）。本輪做完，理由如下。

### commit 軸：合併上游唯一的新 commit `b52a33b`（#160）

`ac490fd` 之後上游只有一筆，44 檔 +6522（新增 line／scatter 圖表變體、style-guide 強化）。
依本檔的同步規則「可直接同步的提交用 merge」執行 `git merge`。

**衝突只有 `.github/workflows/ci.yml` 一處**，而且不是同一件事：上游新增
`Verify maintainer policy tracks package and CI truth` step，本 fork 有
`Detect packaged plugin path changes`（讓 overlay-only 提交不必動產品 plugin 版號）。
兩個 step 都保留。

**實查 overlay 沒有被蓋掉**：`pages.yml` 的 `github.repository == 'cathrynlavery/diagram-design'`
guard 兩處都在、README 頂部 fork overlay 在、`ci.yml` 的 plugin 版號 skip 在。
本 fork 對 `scripts/` 的三處強化（`</script\s*>` → `</script\b[^>]*>`，用來擋
`</script foo>` 這種收尾）也完整保留——它們與上游改的行不同，git 自動合併成功。

**驗證**：fork gate（compileall／ruff／pytest／連結）全綠，加上游六支產品驗證
`test-lint-a11y`／`lint-skin --all --baseline`／`verify-docs-sync`／`test-verify-motion`／
`test-plugin-package`／`test-maintainer-policy` 全部 exit 0。

### PR 軸：117 筆，水位推進到 163

| 分類 | 筆數 | 判定 |
| --- | --- | --- |
| MERGED | 65 | 已在 `upstream/main`。合併 `b52a33b` 之後本 fork 就在上游 tip，產品原始碼與上游逐位元組相同（唯一差異是上述三處強化），所以這 65 筆的內容**已經在本 fork 裡** |
| OPEN | 19 | 還不是上游狀態。本 fork 不 fork-ahead 產品（`FORK.md`：產品以上游為準） |
| **CLOSED 未合併** | **33** | 見下 |

**33 筆關閉未合併的判準**——這一類永遠不會經由 commit 軸抵達，所以不能用「等上游合併」帶過。
本 fork 的實際處境是：**產品原始碼與上游相同，沒有任何分歧的產品程式碼**。因此一個被上游拒收的
PR 在這裡不可能是在修「本 fork 才有的缺陷」——採用它等於製造與上游的分歧，而那正是 `FORK.md`
排除的。

**唯一該例外檢查的是 Windows-first／CJK 這一類**（本 fork 的主線環境與內容語言），實查那 33 筆
標題，只有兩筆落在這個範圍，而且**兩筆的內容都已經在本 fork 裡**：

| PR | 它加了什麼 | 合併後本 fork 的狀態 |
| --- | --- | --- |
| `#76` Fix/allow cjk font fallbacks | `ALLOWED_FONTS` 加 `hiragino sans`／`noto sans jp`／`yu gothic`／`noto sans mono cjk jp` | **四個全在** |
| `#86` add Korean label rules and Noto Sans KR | KR 字型族 | `noto sans kr`／`noto serif kr`／`apple sd gothic neo`／`malgun gothic`／`noto sans mono cjk kr` **全在** |

其餘 31 筆是新圖表型別提案（`#92`–`#103` 等）、工具提案（`#18`／`#27`／`#132`）、文件與早期
分支整併——都是上游的產品策展決定，不是本 fork 的缺陷。

**觸發條件**：本 fork 哪天開始維護分歧的產品程式碼（目前沒有），或出現只在 Windows 上發生、
而上游拒收的修正，就要回來重讀這 31 筆。

### issue 軸：水位推進到最大編號

上游 issue 是產品的功能請求與缺陷回報（新圖表型別、palette 對比、PowerPoint SVG 匯出…）。
與 PR 同理：本 fork 產品碼與上游相同，這些缺陷若成立是**上游產品的缺陷**，修正會經由 commit 軸
抵達。本 fork 沒有可獨立引用的內容。

## 2026-09-13：上游第二輪 triage 與同步（合併 `8d8b299`，ADR 0009 落地，繁中與 Waterfall/Excalidraw 導入）

### commit 軸：合併上游 27 個 commit 至 `8d8b299`（版本 2.6.22）

1. **重大功能更新**：
   - **繁體中文支援**（`#186` / `#196`）：正式引入 Noto Sans TC / Noto Serif TC，新增繁體中文標籤規則與 SVG 匯出字型 `@import` 對齊。
   - **Waterfall 瀑布圖**（`#191`）：新增第 40 種核心視覺圖表（含 dark/full 變體、驗證器與 ADR 0011）。
   - **Excalidraw 匯入**（`#192`）：支援 Excalidraw 檔案解析並以編輯級樣式重繪。
   - **區塊分解語意模式**（`#169`）：新增 Traceable block decomposition 模式與 ADR 0010。
   - **PowerPoint SVG 匯出相容性**（`#151`）：normalize rgba()/transparent 避免匯入 PowerPoint 時黑色塊問題。
   - **強韌性優化**：修復 doctor（#201）、self-check（#205）與 plugin 描述長度（#216）。

2. **版本發布機制變革（ADR 0009）與 fork overlay 調整**：
   - 上游將版本 bump 機制由原本「PR 必須自帶版號更新」轉為「PR 內嚴格禁止更動版號（`--require-no-bump`），merge 到 main 後由 `auto-bump.yml` 自動遞增並發布」。
   - **fork overlay 對齊**：
     - 在 `.github/workflows/ci.yml` 採用上游的新版號檢查機制（main 僅檢查 `--current-only` 一致性，PR 檢查 `--require-no-bump`），完全自然相容本 fork 的 overlay 提交。
     - 在 `.github/workflows/auto-bump.yml` 加入 `if: github.repository == 'cathrynlavery/diagram-design'` 官方 repo 專屬 guard，並在 `tests/test_fork_overlay.py` 中納入 `GATED_WORKFLOWS` 門禁保護，避免 fork 嘗試進行自動發布。

3. **Windows 11 原生環境缺陷修復**：
   - 修復 `tools/check_upstream_updates.py` 在 Windows 原生控制台（CP950 編碼）下遇泰文或特殊字元輸出引發的 `UnicodeEncodeError`（加入 `sys.stdout.reconfigure(encoding="utf-8", errors="replace")`）。

### PR 軸：水位推進至 #222（新增 34 筆）

34 筆新 PR 經逐筆審查：
- **MERGED**（13 筆）：全部隨 commit 軸合併落地。
- **OPEN**（17 筆）：包括 #219（Model architecture 圖表）、#221（西里爾字母支援）、#217（A3 橫向尺寸預設）等，遵照 fork 原則不提早 fork-ahead，留待上游合併。
- **CLOSED 未合併**（4 筆）：#184（泰文手冊）、#204（非功能性提交）、#164（未採納之 Heatmap 方案，改為獨立設計）、#177/#178（外部服務重複 issue）。無 Windows-first 或 CJK 相關未被採納的必要修復。

### issue 軸：水位推進至 #220（新增 25 筆）

25 筆新 issue 經審查：
- #175（繁體中文支援）、#187（Waterfall）、#188（Excalidraw）、#151（PPT 匯出）、#208（Cowork 描述上限）均已隨上述 PR 修復並合併。
- 其餘 open issue 維持追蹤。

## 2026-09-13：代碼審查缺陷修復、優質上游 PR 採納與標籤整頓（PR #210, #222, #212, Issue #202/#203）

### 1. 代碼審查與程式碼品質修復
- **`skills/diagram-design/scripts/drawio_extract.py`**：修復 `F821` 缺陷，補充 `from typing import NoReturn`，修正 `_fail` 函式的回傳型別註解。
- **`scripts/fix-mojibake.py`**：修復 `F541` 缺陷，移除無佔位符的冗餘 `f-string` 前綴。
- **`scripts/verify-doctor.py`**：修復 `F401` 缺陷，移除未使用的 `import os`。
- **`tools/dev_check.ps1`**：擴大本機 fork gate 檢查範疇，將 `scripts/` 與 `skills/diagram-design/scripts/` 納入 `compileall` 與 `ruff (E9+F)` 檢查清單，確保後續腳本變更均受型別與語法安全保護。

### 2. 優質上游修正提早採納（非新圖表型別，純語法解析/文件一致性修復）
遵照 `FORK.md` 原則，本 fork 不 fork-ahead 引入尚未拍板的新圖表型別（如 PR #219），但針對無爭議的 parser bugfix 與文件編號一致性予以提前採用：
- **採納 PR #210（修復 Issue #209）**：Mermaid 緊湊虛線箭頭標籤允許帶空格語法（`A-.label with space.->B`）。修改 `skills/diagram-design/scripts/mermaid_extract.py` 並於 `scripts/verify-mermaid-import.py` 增加迴歸驗證測試。
- **採納 PR #222（修復 Issue #213）**：修復 `skills/diagram-design/assets/index.html` 藝廊標籤頁序號不連續問題（Waterfall 54 -> 20, Line 20 -> 21, ..., Excalidraw 55 -> 52）。並同步於 `scripts/verify-docs-sync.py` 增加連續性驗證器與 `scripts/test-verify-docs-sync.py` 單元測試。
- **採納 PR #212（修復 Issue #211）**：移除 `README.md` 寫死的 "39 visual types" 舊計數，改為引用 `SKILL.md §3`；並將 `README.md` 納入 `scripts/verify-docs-sync.py` 的 `COUNT_SURFACES`，防止未來再度出現硬編碼過期數字。
- **修復 Issue #202 / #203**：在 `skills/diagram-design/references/export.md` 中補充帶有 class-based 樣式（如 `.station`, `.ring`）與 `:root` 變數之圖表在獨立匯出 SVG 時的 CSS 內聯與命名空間避免碰撞指引，防止在 PPT/向量工具中呈現黑塊。

### 3. Git 標籤衛生整頓（只保留最新 tag）
- 檢查本機與遠端 `origin`（`SanHsien/diagram-design`）標籤，確認無舊版本殘留標籤。
- 建立並推播當前最新產品版號標籤 `v2.6.22` 至 `origin`，確保遠端僅保留單一最新 tag。



## 2026-09-30：第三輪上游審查（commit 至 57148ac、PR 至 #263、issue 至 #262）

本 fork 的產品檔與上游一致（歷史已壓縮，無共同祖先，不能 merge），因此只能 `cherry-pick -x`。基準代表已審查，不代表全部合併。

### commit 軸（48 筆）

- **採用（4 筆，cherry-pick -x，各自的 verify 腳本通過）**：#224 雙向箭頭環偵測（excalidraw）、#223 巢狀座標解析（drawio）、#230 slopegraph／ridgeline／bubble 標記解析、#260 motion 只讀根 svg 的 title/desc。
- **採用待辦（adoption pending: 與本 fork 已提早採納的 #210/#212/#222 衝突或牽動整批產品檔）**：#258 Mermaid 語句長度上限（`mermaid_extract.py` 衝突）；#235 SVG 匯出 CSS／defs 命名空間（取代本 fork 的 #202/#203 export.md 段落，需連同 ci.yml、政策檔一起同步）；#245 模板 scroller、#256 SKILL.md LF 與位元組上限、#259 SKILL.md 拆分、#253 截圖 hash、#167 skill guard、#261 政策由 ci.yml 推導、#255 版本比對 CI、#182/#221/#248 文件與字型規格（各自改動 SKILL.md、README、verify-docs-sync 或截圖，需整批同步並跑上游 Playwright 閘門，本機無法驗證）。觸發條件：下次整批同步產品檔時一併處理。
- **新圖表型別／功能，不 fork-ahead**：#228 lifecycle、#231 marimekko、#140 streamgraph、#164 heatmap、#248 A3 預設、#212 後續 README 計數閘門（README 計數已於前輪處理）。留待上游穩定後整批同步。
- **不適用（歸組）**：24 筆 `chore(release): bump plugin manifests`（2.6.23 至 2.6.46）、#263 hero 圖與 social preview（上游宣傳素材）、#255／#261 純 CI 與政策。

### PR 軸（26 筆，#223 至 #263）

- MERGED 16 筆：隨 commit 軸處理，見上。
- OPEN 3 筆（#241 architecture delta、#240 文字度量文件、#249 簡體中文 Noto 字型）：不 fork-ahead；#249 屬 CJK 類，觸發條件為上游合併後與整批同步一起採用。
- CLOSED 未合併 5 筆：#225 測試 PR、#232（README 計數，已由 #212 涵蓋）、#234（Mermaid 空白標籤，已由 #210 涵蓋）、#239（A3，被 #248 取代）、#243（LM Studio 離線 runner，上游專屬功能）。無 Windows-first 缺陷。

### issue 軸（14 筆，#226 至 #262）

- 對應上述功能／修正的追蹤項：#226/#227/#229/#250/#251/#252 功能請求（不採用）、#237/#246 位元組上限與 CRLF（待辦 #256；本 fork 在 Windows 上，觸發條件為同步 SKILL.md 時重驗）、#238/#247 截圖過期（待辦 #253）、#244 手機版模板（待辦 #245）、#254 RTL 支援（功能請求）、#262 無人值守政策（提案）、#242 感謝訊息（不適用）。

### 上游分支

- `repo-sweet-maintainer`：上游維護者工作分支（lifecycle #228 的後續，已隨 #228 合併），不適用。


## 2026-10-25：第四輪上游審查（commit 至 0b9b10c、PR 至 #472、issue 至 #476），整批同步

09-30 條目的「採用待辦」觸發條件是「下次整批同步產品檔」，本輪即該次。上游這段有 170 個 commit、152 個 PR、61 個 issue；fork 的 `fork-maintenance`／`Upstream check` 也因此紅。

### 做法

本 fork 歷史已壓縮、與上游無共同祖先（`git merge-base HEAD upstream/main` 無輸出），`git merge upstream/main` 不可行；也**不**用 `--allow-unrelated-histories` 把上游 377 個 commit 接回來，那會推翻壓縮決定。改成：以 `upstream/main` 樹為底，放回 fork 專屬檔，再把覆蓋層逐項重套，單親 commit 推 `origin/main`。

覆蓋層重套清單（以 `git diff 57148ac HEAD` 為準，只重套刻意的部分；落後上游的部分一律取上游）：

| 檔案 | 處理 |
| --- | --- |
| `README.md`／`CONTRIBUTING.md`／`SECURITY.md`／`CODE_OF_CONDUCT.md`／`.github/PULL_REQUEST_TEMPLATE.md` | 取上游正文，頂部 fork overlay 放回；README 的 Changelog 連結改指上游（上游新增的 `CHANGELOG.md` 與本 fork 同名，保留本 fork 維護史） |
| `.github/workflows/pages.yml`／`auto-bump.yml` | 取上游（已全數 SHA 釘版），加回 `github.repository == 'cathrynlavery/diagram-design'` 閘門 |
| `.github/workflows/ci.yml` | 取上游，不加任何 guard（`test_product_ci_is_not_official_repo_only`） |
| `.github/ISSUE_TEMPLATE/config.yml`、`.gitattributes`、`.gitignore` | fork 版／上游規則加 fork 規則 |
| `AGENTS.md` | 保留本檔；上游同名新檔的「新增型別清單」併入新章節；型別計數 39→45 |

上游新增檔的取捨：`CLAUDE.md`（`@AGENTS.md` 匯入行）不收，repo 只用 `AGENTS.md`；`.github/CODEOWNERS`（`* @cathrynlavery`）與 `.github/FUNDING.yml`（作者贊助按鈕）屬上游作者，不收；`.github/workflows/ci-configuration.yml`（zizmor 稽核 `.github/**`）收；`.maintainer-policy.json`、`.qoder-plugin/`、`PRIVACY.md` 隨產品樹收。

### 本 fork 對上游的分歧（產品碼 5 組 8 個檔，加 1 項設定；皆未回貢）

1. `scripts/lint-skin.py`、`scripts/test-verify-motion.py`、`scripts/test-lint-a11y.py`、`scripts/test-export-wait.py`（後者是本輪上游新檔，CodeQL `py/bad-tag-filter`）：`</script\s*>` → `</script\b[^>]*>`（08-28 起；上游至 0b9b10c 仍是 `\s*`）。
2. `scripts/plugin_version_history.py`：錯誤訊息的路徑改 `as_posix()`。Windows 上印成 `.codex-plugin\plugin.json`，`scripts/test-plugin-package.py` 比對正斜線而失敗。
3. `scripts/test-verify-doctor.py`：`tasklist` 輸出加 `errors="replace"`。繁中 Windows 的 `tasklist` 是 cp950，`PYTHONUTF8=1`（本 fork 文件要求設的）下以 UTF-8 解碼會丟 `UnicodeDecodeError`，`stdout` 變 `None`。
4. `scripts/verify-excalidraw-import.py`：迴圈變數 `secret` → `canary`（PR #1，擋 CodeQL `py/clear-text-logging-sensitive-data`）。壓縮後的歷史裡這筆在 squash commit 內，第一次同步誤取上游而漏掉，後由 main 上的 code scanning 告警 #5 發現並補回。
5. `pyproject.toml` 的 `per-file-ignores`：上游 4 個檔有 5 個 pyflakes 發現（`F841`、`F541`、`F811`×2、`F821` 的 `NoReturn` 只用在註解），產品檔保持與上游逐位元組相同，改在設定檔記錄；上游修掉就刪該行。

PLAYBOOK §2 判準六的表格寫 `diagram-design` 分歧產品檔為 0，這是 08-28 之前的狀態；實際上第 1 項早就存在。

### commit 軸（170 筆）

全採，隨樹同步（沒有逐筆略過）。其中 74 筆 `chore(release): bump plugin manifests`、8 筆 merge、其餘為修正與新型別（architecture delta／containment、service blueprint、axonometric plan／exploded、heatmap、marimekko、streamgraph、lifecycle、steps 以外的已合併項目等），型別計數 39→45（`VISUAL_TYPE_COUNT = 45`）。09-30 列的「採用待辦」（#258、#235、#245、#256、#259、#253、#167、#261、#255、#182、#221、#248）與「新圖表型別，不 fork-ahead」（#228、#231、#140、#164）全部隨此次同步收齊。

### PR 軸（152 筆，#264 至 #472）

- MERGED 70 筆：70 筆編號全部出現在已同步的 commit 紀錄裡（腳本比對 `git log 57148ac..upstream/main` 的 `#N`，缺 0 筆）。
- CLOSED 未合併 56 筆、OPEN 26 筆：本 fork 產品碼 = 上游 + 上列 1–3 的分歧，被上游拒收或未合併的 PR 不可能在修「只有本 fork 才有的缺陷」（判準六），只查 Windows／CJK 類。以 `windows|cp950|crlf|backslash|utf-?8|unicode|cjk|chinese|japanese|noto|mojibake|powershell|encoding` 掃標題與內文，命中：
  - **#465（OPEN）** `test-verify-docs-sync` 在 CRLF 檢出下失敗：Windows 類，影響本機（`core.autocrlf=true`）檢出，不影響 CI。本輪用 LF 檢出驗證；觸發條件：上游合併後隨整批同步採用，或 fork 的 `dev_check.ps1` 開始跑產品測試時。
  - **#371／#389／#390／#391（CLOSED）** Mermaid 的 Unicode 識別字（CJK 類）：已由 #410 併入。實測 `mermaid_extract.py`：`erDiagram` 的「客戶／訂單／孤立實體」三個實體與「待機 : 等待輸入」的狀態描述都保留（見 REVIEW 證據）。
  - **#301（CLOSED）** doctor 的 Playwright 探測：由 #348 併入；`verify-doctor.py` 已不依賴 `playwright.__version__`。
  - 其餘命中（#472、#458、#440、#433、#335、#315）是文件／文法中的關鍵字，不是 Windows 或 CJK 缺陷。

### issue 軸（61 筆，#263 至 #476；52 CLOSED／9 OPEN）

Windows／CJK 類：#438 日文兩行標籤（由 #439 修）、#401 draw.io `--out` 無法寫入（#413）、#298 PNG 檔名含 `#`／`%`（#348）、#407／#429 SVG 匯出（#414／#432），皆已在同步的樹內。OPEN 9 筆（含 #463、#473 Mermaid 摘要與連字號節點）是上游缺陷，與本 fork 相同，等上游修。

### 上游分支

71 條上游分支，57 條尚未併入 `upstream/main`；它們是 PR 工作分支，PR 軸已涵蓋，不另列。

### 其他

- 依賴新鮮度：`ruff>=0.16` 對 PyPI 的 0.17.2。fork 的 gate 只選 `E9,F`，兩個版本行為相同，下限是相容性承諾，故在宣告行寫 `# freshness-hold:`，沒有調高下限。
- 本機驗證沒跑到的項目（沒裝 Playwright 瀏覽器）：`lint-render.py`、`verify-excalidraw-import.py` 與其測試、`test-export-wait.py`，交給 CI 的 Ubuntu／Windows job。

### 同日補記：Pillow 與告警

- 同步帶進上游的 `.github/ci/python/uv.lock`（`pillow==12.1.1`），Dependabot 立刻回報 118 筆 Pillow 告警（59 個 GHSA，pyproject 與 uv.lock 兩個 manifest 各一份；修補版皆 ≤13.0.0，含 critical），且 Dependabot 的 uv 安全更新工作以 `Bad Request` 失敗、開不出 PR。依 PLAYBOOK §1，安全理由可以調高：`pyproject.toml` 與 `uv.lock` 改 `pillow==13.0.0`（`uv lock --upgrade-package`），`CONTRIBUTING.md` 的兩處版本字樣同步；`test-build-readme-thumbs.py` 與 `build-readme-thumbs.py --check` 在 13.0.0 下通過（46 張縮圖）。
- 同步前沒查「上游新增的依賴鎖檔會帶進哪些告警」。下次整批同步後先查 `dependabot/alerts` 與 `code-scanning/alerts`。
- code scanning #6（`mermaid_extract.py` 的箭頭正則被 `py/bad-tag-filter` 當成 HTML 標籤過濾）是誤報：該正則比對 Mermaid 連線運算子，不是 HTML。以 `false positive` dismiss 並附此說明。

## 2026-10-26：第五輪上游審查（commit 至 10cfad6、PR 至 #483、issue 至 #482）

上一輪水位 `0b9b10c` 之後上游又進 16 個 commit（8 筆 `chore(release)` 版號 bump、8 筆修正）、6 個 PR（#477–#481、#483）、1 個 issue（#482）。判準八檢查：對 `0b9b10c..10cfad6` 與 #478／#479／#481／#483 目前的 head diff 掃隱藏內容（行內 40 字元以上空白後接內容、`eval`／`new Function`／`globalThis`、100 字元以上 base64 樣式、500 字元以上單行），只命中 `import-mermaid.md` 一行 600+ 字元的文件說明段落（純文字，無程式），其餘 0 筆。

### commit 軸（16 筆）全採
以 `git diff 0b9b10c upstream/main` 套用，只排除上游 `CHANGELOG.md` 一行（本 fork 的 `CHANGELOG.md` 是自己的維護史）。涵蓋：#440 self-check 拒收提前結束的文件（`self_check.py`＋測試）、#458 Mermaid flowchart 邊 ID、#470 heatmap 引號內的 `>`、#471 計入被丟棄的 config 指令、#472 保留 sequence autonumber、#464／#480 文件修正、#477 ci.yml 的 setup-python 註解、ci.yml 新增 `Verify Mermaid import` 步驟、plugin manifests 2.6.120→2.6.128。

### PR 軸
| PR | 狀態 | 結論與證據 |
|---|---|---|
| #477、#480 | MERGED | 已在 commit 軸 |
| #479 `0b7c5be` | OPEN | **採（移植）**。缺陷在本 fork 存在：`flowchart LR\n  user-profile\n` 以 base 的 `mermaid_extract.py` 執行得 `malformed edge at line 2`（連字號節點 id 被當成壞掉的邊），改後得 1 個節點（連同 `A --> B` 的測試案例為 3 個）。`_edge_operators` 的 x／o 箭頭改為需兩個以上連線字元、`_parse_flowchart` 的 `-.` 補跳脫並擋 `-x`／`=o` 單字元連線。與已同步的 #458 在 `verify-mermaid-import.py`、`import-mermaid.md` 有相鄰衝突，兩邊都保留手動合併；`verify-mermaid-import.py` 全綠 |
| #478 `d447c72` | OPEN | 不單獨採：改的是 #479 同一行（`-.` → `-\.`），#479 為超集 |
| #483 `f395d28` | OPEN | **採**，對應 issue #482。`example-high-level-vertical.html` 兩則註解的 `color override:` 改寫，加入 `scripts/test-install-scan.py`（複製 Hermes 的 `html_comment_injection` 規則掃整個 skill，287 檔 0 命中）與 CI／CONTRIBUTING／`.maintainer-policy.json` 登記。排除其 `CHANGELOG.md` 行 |
| #481 `188e4b9` | OPEN | **延後**。新增 `arrow-focal` marker 並把三個 DP integration 範例的 primary 連線改用它；`focal_accent` 預設等於 `accent`，預設輸出視覺不變，只有自訂 `focal_accent` 時才有差。動到 3 個範例 HTML 與 type 規格（5→6 個 marker），會牽動螢幕截圖與規格計數驗證。觸發條件：上游合併後隨下次同步採用，或本 fork 開始使用自訂 `focal_accent` |

### issue 軸
#482（Hermes 安裝被 `html_comment_injection` 誤判擋下）：由 #483 處理。#475（primary connector 的 marker 恆為 `accent`）：與 #481 同一缺陷，一併延後。

### 分歧清單新增
`ci.yml` 與 `mermaid_extract.py`／`verify-mermaid-import.py`／`import-mermaid.md` 現在含上游**尚未合併**的 #479、`ci.yml`／`CONTRIBUTING.md`／`.maintainer-policy.json`／`scripts/test-install-scan.py`／`example-high-level-vertical.html` 含 #483。上游合併（或改採不同修法）後下次同步會有衝突，屆時以上游版本為準並刪除本段。

### 驗證
`verify-mermaid-import.py`、`test-self-check.py`、`test-verify-heatmap.py`、`verify-heatmap.py`、`verify-docs-sync.py`、`test-lint-a11y.py`、`test-plugin-package.py`、`test-install-scan.py`、`lint-skin.py --all --baseline`、`pytest tests` 全綠。`test-verify-docs-sync.py` 在本機 CRLF 檢出下失敗，base 上同樣失敗（上游 #465，已知，見第四輪）。沒裝 Playwright 瀏覽器，像素類檢查交給 CI。


## 2026-10-28：第六輪上游審查（commit 至 0cf73c3、PR 至 #486、issue 至 #489）

上一輪水位 `10cfad6` 之後上游進 16 個 commit（8 筆 `chore(release)` 版號 bump 2.6.129 至 2.6.136、8 筆修正或功能）、2 個 PR（#484、#486）、4 個 issue（#485、#487、#488、#489）。`Upstream check` 紅燈即由這些而來。

判準六先驗證：`git diff 10cfad6 HEAD` 顯示本 fork 相對上一輪水位的產品碼分歧仍是上列 5 組（`</script`、`as_posix()`、`tasklist` 的 `errors="replace"`、`canary` 改名、`pyproject.toml` 的 `per-file-ignores`）加上第五輪移植的 #479（`mermaid_extract.py`、`verify-mermaid-import.py`、`import-mermaid.md`）。本輪上游只動 `scripts/`、`skills/diagram-design/` 下的另一批檔案，與這些分歧不重疊，所以 PR／issue 走結構性論證，只查 Windows／CJK 類。

判準八：對 `10cfad6..0cf73c3` 的整份 diff、以及 #478／#479／#481／#486 目前 head 的 diff，掃行內 40 字元以上空白後接內容、`eval`／`new Function`／`globalThis`／`atob`／`fromCharCode`、100 字元以上 base64 樣式、500 字元以上單行。命中的 6 行全是文件或 manifest 說明文字（`.codex-plugin/plugin.json` 的 longDescription、`CONTRIBUTING.md` 與 `SKILL.md` 的描述、三個 reference 文件段落），另有 PNG 二進位區塊；新增的 `verify-box-plot.py`、`test-verify-box-plot.py` 對 `subprocess`／`socket`／`urllib`／`exec`／`eval` 掃描，只有測試以 `subprocess.run` 跑隨附範例。#481 的 head 自上一輪看過的 `188e4b9` 變成 `2ce275a8e7`（有新 commit），已對目前 head 重掃，0 命中。

### commit 軸（16 筆）全採
以 `git diff 10cfad6 upstream/main` 做 3-way 套用，排除上游 `CHANGELOG.md` 一行（本 fork 的 `CHANGELOG.md` 是自己的維護史），43 個檔中沒有衝突。

| 上游 commit | 內容 | 本 fork 處理 |
|---|---|---|
| `3fdf8c2` #483 | 重寫會被 Hermes `html_comment_injection` 擋下的註解，新增 `scripts/test-install-scan.py` | 第五輪已移植未合併版（head `f395d28`）。上游合併版與 head 相同；`ci.yml`、`.maintainer-policy.json`、`scripts/test-install-scan.py`、`example-high-level-vertical.html` 現在與上游逐位元組相同，第五輪「分歧清單新增」中這四個檔的段落作廢 |
| `84886eb` #469 | Excalidraw 匯入回報最外層群組 | 採。`verify-excalidraw-import.py` 的 `canary` 改名保留（分歧第 4 項） |
| `17686b9` #468 | draw.io 標籤保留角括號 | 採 |
| `7bf9445` #435 | 散佈圖新增 box plot 變體（`verify-box-plot.py` 1705 行、測試 144 案、3 個範例） | 採。它是 `scatter` 的變體，型別計數維持 45（`verify-docs-sync.py` 通過）。`verify-box-plot.py --all` 通過 |
| `1677a5c` #481 | DP integration 的 primary 連線改用 `focal_accent` 箭頭 | 採，第五輪「延後」的觸發條件（上游合併）已成立。同時收掉 issue #475 |
| `fbdbd83` #465 | `test-verify-docs-sync` 在 CRLF 檢出下比對換行 | 採。這是第四輪點名的 Windows 類項目：本 worktree `core.autocrlf=true`，`test-verify-docs-sync.py` 現在通過（第五輪在同一環境失敗） |
| `d39a365` #484 | `verify-geometry` 讀單引號 SVG 屬性 | 採 |
| `0b5b3bc` #467 | `verify-exploded` 拒絕投影幾何上的 CSS transform | 採 |
| 8 筆 `chore(release)` | 外掛 manifests 2.6.129 至 2.6.136 | 採 |

### PR 軸
| PR | 狀態 | 結論與證據 |
|---|---|---|
| #484、#481、#483、#465 | MERGED | 已在 commit 軸 |
| #486 `0eb47d9482`（jolinin） | OPEN | **延後，並以 `monitored` 釘住**。改 `export_svg.py`（`normalize_html_entities` 加數字字元參照，+67／-9，含 README 與 `export.md`）。缺陷在本 fork 存在，實測 `export_svg_document` 對 `&#128;` 得 ``（瀏覽器是 `€`），`&#65z`（無分號）直接以 XML 不合法報錯；但範圍窄：CJK 的 `&#20013;`、`&#x4E2D;` 都正確得 `中`，所以不屬於 CJK 類；受影響的只有 U+0080 至 U+009F 與無分號寫法。本 fork 的 skill 範例、文件不含這類參照（grep `&#(x8x|1[2-5]x)` 只命中 `export_svg.py` 與其測試自身）。作者是外部貢獻者、PR 未經上游維護者審過，且 67 行改寫一個 regex 狀態機，邏輯尚未穩定。觸發條件：上游合併、或 head 變動（`monitored` 會報）、或本 fork 遇到實際輸出 `&#12x;` 的圖 |
| #479 `0b7c5be522` | OPEN | 維持第五輪「採（移植）」。上游 head 未動；本 fork 的移植仍在（`mermaid_extract.py`），套用本輪 diff 時無衝突。補上 `monitored` 釘住，上游合併或改 head 時報告會提醒（上一輪沒有釘，等於合併後無人通知） |
| #478 `d447c72ba1` | OPEN | 維持「不單獨採」（#479 的超集）；同樣釘住 |

### issue 軸
| Issue | 狀態 | 結論與證據 |
|---|---|---|
| #485 | CLOSED（not planned，作者 thegodlovestome-dev） | 標題「好」、內文空白，上游維護者以「沒有描述」關閉。無可行動內容，不引進 |
| #487 | OPEN（cathrynlavery） | `verify-box-plot.py` 的 8 類剩餘漏洞（隱藏標籤、`stroke="none"` 的中位線、CSS 動畫結尾 opacity 0、布林屬性、其他色彩記法、`+`／`~` 選擇器等）。對象是本輪才進來的新檢查器，缺陷與本 fork 相同（逐位元組同上游），非 Windows／CJK 類，且上游已有人認領第 2 項（Ethereal49）。等上游修；觸發條件：`verify-box-plot.py` 在上游有 commit 時隨整批同步取得 |
| #488 Requirement traceability 型別提案、#489 Event modeling 型別提案 | CLOSED（not planned，YalcinkayaE，同日關閉） | 新圖表型別提案，上游已拒收；新增型別是上游策展範圍（比照第四輪「新圖表型別，不 fork-ahead」），不引進 |

### 驗證
`verify-docs-sync.py`、`test-verify-docs-sync.py`、`test-verify-box-plot.py`（144 案）、`test-verify-geometry.py`、`verify-geometry.py --all`（220 檔 0 finding）、`test-verify-exploded.py`、`verify-exploded.py --all`、`test-install-scan.py`（290 檔）、`test-maintainer-policy.py`、`test-verify-beeswarm.py`、`test-plugin-package.py`、`verify-drawio-import.py`、`verify-mermaid-import.py`、`verify-screenshot-freshness.py`（45 個來源）、`lint-skin.py --all --baseline`（0 finding）、`test-export-svg-standalone.py`、`verify-box-plot.py --all` 全綠。`verify-excalidraw-import.py` 的邏輯段全過，最後的瀏覽器渲染段因本機沒裝 Playwright Chromium 失敗（與第四、五輪相同），交 CI。

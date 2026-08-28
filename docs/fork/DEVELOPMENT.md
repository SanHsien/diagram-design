# 開發環境

維護者與 AI 接手用的開發文件。產品用法看 [`README.md`](../../README.md)；上游同步在 [`UPSTREAM.md`](UPSTREAM.md)；決策在 [`DECISIONS.md`](DECISIONS.md)。

## 架構

```text
skills/diagram-design/SKILL.md   產品 skill（英文，以上游為準）
        │
        ├── references/          類型／風格／匯入／動畫細節
        ├── assets/              三套變體 HTML + 模板 + gallery
        └── scripts/             draw.io / Mermaid 抽取器與 self-check
        │
        ▼
 安裝到宿主 skills／plugin marketplace 後才真正可被呼叫

scripts/*.py                     上游驗證器（skin、geometry、import、docs sync）
commands/  prompts/              各宿主斜線命令與 Pi prompt
.claude-plugin/ .codex-plugin/   marketplace / plugin manifests
```

`skills/diagram-design/`、`scripts/`、`commands/`、`prompts/` 與 plugin manifests 是要安裝或跟隨上游的產品。`FORK.md`、`tools/`、`docs/fork/`、`tests/` 是本 fork 的開發與治理骨架，不要一起複製進 skills 目錄。

## 本機開發（Windows）

```powershell
python -m venv .venv
.venv\Scripts\python -m pip install --upgrade pip
.venv\Scripts\python -m pip install -r requirements-dev.txt
$env:PYTHONUTF8 = "1"
pwsh -NoProfile -File tools\dev_check.ps1
```

先決條件：Python 3.14（overlay CI）；產品腳本官方支援 3.10+，CI 另測 3.9／3.11／3.12。PowerShell 7。產品像素 lint 另需 Playwright Chromium（僅 Ubuntu 3.12 job）。

只驗證產品入口是否齊全時，確認：

- `skills/diagram-design/SKILL.md`
- `skills/diagram-design/assets/template.html`
- `skills/diagram-design/references/style-guide.md`
- `.claude-plugin/plugin.json`
- `scripts/lint-skin.py`

不要拿真實客戶網站跑品牌 onboarding 來當 CI。overlay gate 驗的是規格、語法與維護腳本。

## Canonical fork gate

`tools\dev_check.ps1` 會依序：

1. `python -m compileall`（`tools`、`tests`）
2. `ruff check`（E9 + F，僅 overlay Python）
3. `pytest tests -q`
4. `python tools/check_links.py`

這是 fork 文件的硬閘門，不是完整產品回歸。

產品行為變更再跑（節錄；完整清單見上游 [`CONTRIBUTING.md`](../../CONTRIBUTING.md)）：

```powershell
python scripts\test-lint-a11y.py
python scripts\lint-skin.py --all --baseline
python scripts\verify-docs-sync.py
python scripts\verify-geometry.py --all
```

上游 `ci.yml` 仍會在本 fork 的 `main` 上跑跨平台產品回歸。不要把那條 workflow 加上官方-repo-only guard。

## 工具設定

`pyproject.toml` **只放工具設定**，沒有 `[project]` 與 `[build-system]`：本 repo 交付的是 Agent Skill，不是 Python 套件。改 overlay ruff 旗標時要同步改 `pyproject.toml`。`.python-version` 釘 3.14。

`.gitattributes` 把 overlay 行尾釘成 LF。沒有它，全域 `core.autocrlf=true` 會讓工作區變 CRLF，於是 `git status` 顯示檔案 modified 但 `git diff` 是空的。

## 依賴新鮮度

`tools/check_dependency_freshness.py` 把 `requirements-dev.txt` 宣告的每一筆直接依賴拿去對 PyPI 現行版本，`.github/workflows/dependency-freshness.yml` 每月跑一次。紅燈只有兩條誠實出口：`# freshness-hold:`（常態政策）或 `.github/dependency-deferrals.json` 的 `deferredLatest`（會過期）。調高宣告下限來讓報告變綠不是出口。產品 Playwright pin 在 `ci.yml` 的 `PLAYWRIGHT_VERSION`，不進 overlay requirements。

## 不要做的事

- 不要把產品 `SKILL.md` 改寫成維護索引。
- 不要翻譯 `skills/` 或範例 HTML。
- 不要把根目錄 `README.md` 改成繁中主檔。
- 不要在本 fork 啟用 `pages.yml` 部署。
- 不要提交 `.env`、API key 或未公開客戶圖表。
- overlay 測試必須是靜態規格檢查，不能打真實第三方網站。
- 不要對上游開 PR，除非維護者在當次對話明確同意回貢。

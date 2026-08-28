from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))

import check_links  # noqa: E402
import check_upstream_updates as checker  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
OFFICIAL_REPO = "cathrynlavery/diagram-design"
FORK_REPO = "SanHsien/diagram-design"
UNGATED_WORKFLOWS = (
    "ci.yml",
    "fork-maintenance.yml",
    "upstream-check.yml",
    "codeql.yml",
    "dependency-freshness.yml",
)
GATED_WORKFLOWS = ("pages.yml",)


def test_baseline_file_is_valid_and_complete() -> None:
    baseline = checker.load_baseline()

    assert baseline["repo"].endswith("diagram-design.git")
    assert baseline["branch"] == "main"
    assert len(baseline["reviewed_through"]) == 40
    assert baseline["reviewed_date"] == "2026-08-28"


def test_workflow_is_scheduled_and_fails_on_unreviewed_commits() -> None:
    workflow = (
        ROOT / ".github" / "workflows" / "upstream-check.yml"
    ).read_text(encoding="utf-8")

    assert "schedule:" in workflow
    assert "cron:" in workflow
    assert "workflow_dispatch:" in workflow
    assert "tools/check_upstream_updates.py" in workflow
    assert "fetch-depth: 0" in workflow
    assert "exit 1" in workflow


def test_render_markdown_reports_no_new_commits() -> None:
    baseline = {
        "repo": "https://example.invalid/upstream.git",
        "branch": "main",
        "reviewed_through": "a" * 40,
        "reviewed_date": "2026-08-28",
    }

    report = checker.render_markdown(baseline, [])

    assert "No new upstream commits" in report


def test_render_markdown_surfaces_check_failure() -> None:
    baseline = {
        "repo": "https://example.invalid/upstream.git",
        "branch": "main",
        "reviewed_through": "a" * 40,
        "reviewed_date": "2026-08-28",
    }

    report = checker.render_markdown(baseline, [], error="git fetch failed")

    assert "Check failed" in report
    assert "git fetch failed" in report


def test_load_baseline_rejects_missing_file(tmp_path: Path) -> None:
    with pytest.raises(checker.UpstreamCheckError):
        checker.load_baseline(tmp_path / "nope.json")


def test_baseline_matches_decisions_record() -> None:
    decisions = (ROOT / "docs" / "fork" / "DECISIONS.md").read_text(encoding="utf-8")
    upstream = (ROOT / "docs" / "fork" / "UPSTREAM.md").read_text(encoding="utf-8")
    baseline = json.loads(
        (ROOT / "tools" / "upstream_baseline.json").read_text(encoding="utf-8")
    )

    assert baseline["reviewed_date"] in decisions
    assert baseline["reviewed_through"][:7] in upstream
    assert "reviewed_pr_through" not in baseline
    assert "reviewed_issue_through" not in baseline


def test_overlay_markdown_links_resolve() -> None:
    failures = 0
    for path in check_links.iter_documents():
        problems = check_links.check_document(path)
        failures += len(problems)
        for problem in problems:
            print(f"{path}: {problem}")
    assert failures == 0


def test_readme_keeps_upstream_english_product_contract() -> None:
    readme = (ROOT / "README.md").read_text(encoding="utf-8")

    assert not (ROOT / "README.en.md").exists()
    assert "SanHsien 維護型 fork" in readme
    assert FORK_REPO in readme
    assert OFFICIAL_REPO in readme
    assert "FORK.md" in readme
    assert "REVIEW.md" in readme
    assert "Editorial diagrams" in readme
    assert "39 editorial diagram types" in readme
    assert "MIT" in (ROOT / "LICENSE").read_text(encoding="utf-8")


def test_link_checker_skips_product_readme_and_scans_review() -> None:
    rels = {path.relative_to(ROOT).as_posix() for path in check_links.iter_documents()}

    assert "README.md" not in rels
    assert "REVIEW.md" in rels
    assert "FORK.md" in rels
    assert "NOTICE.md" in rels
    assert "SECURITY.md" in rels
    assert "CONTRIBUTING.md" in rels
    assert "docs/fork/DECISIONS.md" in rels


def test_missing_relative_rejects_path_escape() -> None:
    problem = check_links._missing_relative(ROOT / "FORK.md", "../outside-the-repo")

    assert problem is not None
    assert "逃出 repo 根目錄" in problem
    assert check_links._missing_relative(ROOT / "FORK.md", "NOTICE.md") is None


def test_agents_overlay_points_at_fork_rules() -> None:
    agents = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
    claude = (ROOT / "CLAUDE.md").read_text(encoding="utf-8")

    assert "SanHsien/diagram-design" in agents
    assert "FORK.md" in agents
    assert "不推送到 `upstream`" in agents
    assert "FORK.md" in claude
    assert claude.strip() != "@AGENTS.md"
    assert "REVIEW.md" in agents
    assert "skills/diagram-design/" in agents


def test_product_ci_is_not_official_repo_only() -> None:
    ci = (ROOT / ".github" / "workflows" / "ci.yml").read_text(encoding="utf-8")
    assert "scripts/lint-skin.py" in ci
    assert "windows-latest" in ci
    assert "persist-credentials: false" in ci
    assert f"github.repository == '{OFFICIAL_REPO}'" not in ci


def test_every_workflow_is_classified() -> None:
    names = {path.name for path in (ROOT / ".github" / "workflows").glob("*.yml")}
    assert names == set(UNGATED_WORKFLOWS) | set(GATED_WORKFLOWS)


def test_ungated_workflows_are_not_official_repo_only() -> None:
    official_guard = f"github.repository == '{OFFICIAL_REPO}'"
    workflows = ROOT / ".github" / "workflows"
    for name in UNGATED_WORKFLOWS:
        text = (workflows / name).read_text(encoding="utf-8")
        assert official_guard not in text, name


def test_pages_workflow_is_official_repo_only() -> None:
    text = (ROOT / ".github" / "workflows" / "pages.yml").read_text(encoding="utf-8")
    assert f"github.repository == '{OFFICIAL_REPO}'" in text


def test_security_and_contributing_name_the_fork() -> None:
    security = (ROOT / "SECURITY.md").read_text(encoding="utf-8")
    contributing = (ROOT / "CONTRIBUTING.md").read_text(encoding="utf-8")

    assert FORK_REPO in security
    assert FORK_REPO in contributing
    assert "FORK.md" in security
    assert "FORK.md" in contributing
    assert f"{OFFICIAL_REPO}/security/advisories/new" in security
    assert "python3 scripts/lint-skin.py" in contributing


def test_product_skill_entry_exists() -> None:
    skill = ROOT / "skills" / "diagram-design" / "SKILL.md"
    assert skill.is_file()
    text = skill.read_text(encoding="utf-8")
    assert "name: diagram-design" in text
    assert (ROOT / "skills" / "diagram-design" / "references" / "style-guide.md").is_file()
    assert (ROOT / "skills" / "diagram-design" / "assets" / "template.html").is_file()


def test_gitignore_covers_overlay_and_secrets() -> None:
    text = (ROOT / ".gitignore").read_text(encoding="utf-8")
    assert ".env*" in text
    assert ".venv/" in text
    assert "cookies.txt" in text
    assert "cookies.json" in text
    assert "credentials.json" in text


def test_claude_md_is_a_regular_file() -> None:
    claude = ROOT / "CLAUDE.md"
    assert claude.is_file()
    assert not claude.is_symlink()


def test_fork_workflows_use_python_314() -> None:
    for name in ("fork-maintenance.yml", "upstream-check.yml"):
        text = (ROOT / ".github" / "workflows" / name).read_text(encoding="utf-8")
        assert 'python-version: "3.14"' in text, name


def test_issue_templates_point_to_upstream_product() -> None:
    config = (ROOT / ".github" / "ISSUE_TEMPLATE" / "config.yml").read_text(
        encoding="utf-8"
    )
    assert OFFICIAL_REPO in config
    assert "blank_issues_enabled: false" in config
    assert f"{FORK_REPO}/blob/main/CONTRIBUTING.md" in config


def test_overlay_docs_use_the_counted_type_total() -> None:
    fork = (ROOT / "FORK.md").read_text(encoding="utf-8")
    notice = (ROOT / "NOTICE.md").read_text(encoding="utf-8")
    agents = (ROOT / "AGENTS.md").read_text(encoding="utf-8")

    assert "39 種" in fork
    assert "editorial diagrams" in notice
    assert "39 種" in agents


def test_no_tracked_git_symlinks() -> None:
    result = subprocess.run(
        ["git", "ls-files", "-s"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    for line in result.stdout.splitlines():
        mode = line.split(None, 1)[0]
        assert mode != "120000", line

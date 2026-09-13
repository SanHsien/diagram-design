English | [中文版](CHANGELOG.md)

# Changelog

Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/); newest first.
This file records **this fork's maintenance history** only (from 2026-08-28). The product
history of upstream
[`cathrynlavery/diagram-design`](https://github.com/cathrynlavery/diagram-design) lives in its
own history and in the review ledger at [`docs/fork/UPSTREAM.md`](docs/fork/UPSTREAM.md).
Per-commit adopt/skip reasoning is recorded in [`docs/fork/DECISIONS.md`](docs/fork/DECISIONS.md).

---

## 2026-08-28 (land remaining review remediations)

### Changed

- **Product `ci.yml` / `pages.yml` pin action SHAs.** checkout, setup-python, and setup-node are pinned; Pages checkout sets `persist-credentials: false`.
- **Script end tags.** `lint-skin.py` and matching tests now use `</script\b[^>]*>` so they match the junk HTML parsers accept.

This pass does not contribute back upstream. Plugin homepage, README author CTAs, and Mermaid `-->` grammar stay unchanged.

---

## 2026-08-28 (full-repo review)

### Changed

- **Rewrote `REVIEW.md`.** Records the overlay SHA, GitHub Actions URLs, four open CodeQL alerts, and the product CI failures caused by the overlay.
- **Product `ci.yml`:** overlay-only commits skip the plugin version gate so this fork does not race ahead of upstream versions.
- **`.gitattributes`:** stop marking HTML/SVG as binary so `git diff --ignore-space-at-eol` can verify generated icons.

This pass does not contribute back upstream.

---

## 2026-08-28 (create Windows-first maintenance fork)

### Added

- **Fork overlay.** `FORK.md`, `NOTICE.md`, `REVIEW.md`, `AGENTS.md`, `CLAUDE.md`, `docs/fork/`, Windows gate, `upstream-check`, CodeQL, Dependabot.
- **Official-repo guard on `pages.yml`.** Stops this fork failing every `main` push when GitHub Pages is not enabled.

### Changed

- **Top overlays on `README.md`, `CONTRIBUTING.md`, `SECURITY.md`, and `CODE_OF_CONDUCT.md`.** Product body stays upstream.

This pass does not contribute back upstream.

# Standalone Documentation Rewrite Implementation Plan

> Historical implementation record for the repository. Use it as maintenance context and project memory, not as a mandatory execution script.

**Goal:** Rewrite the repository documentation so `Codex Code Game Studios`
reads as a fully standalone Codex-native product across onboarding, workflow,
reference, template, example, and maintenance docs.

**Architecture:** Perform the rewrite in two layers. First, rewrite the core
product and operating documents manually so the repository has a new canonical
voice and structure. Second, run a controlled bulk conversion over supporting
doc families so templates, examples, engine references, plan logs, and test
framework docs all inherit consistent framing without losing technical detail.

**Tech Stack:** Markdown, YAML, existing repo references, `apply_patch` for
manual rewrites, and a one-off Python batch pass for bulk documentation
normalization.

---

### Task 1: Create rewrite records

**Files:**
- Create: `docs/plans/2026-04-13-standalone-docs-design.md`
- Create: `docs/plans/2026-04-13-standalone-docs-implementation.md`

**Step 1:** Capture the approved redesign scope, principles, and validation rules.

**Step 2:** Record the implementation order so future maintainers understand how the docs were transformed.

### Task 2: Rewrite the primary product docs

**Files:**
- Modify: `README.md`
- Modify: `UPGRADING.md`
- Modify: `AGENTS.md`
- Modify: `docs/WORKFLOW-GUIDE.md`

**Step 1:** Replace migration/port framing with original product positioning.

**Step 2:** Clarify installation, workflow, and maintenance paths.

**Step 3:** Keep commands and referenced paths aligned with the real repo.

### Task 3: Rewrite the studio handbook

**Files:**
- Modify: `docs/studio/*.md`

**Step 1:** Reframe setup, quick start, global install, directory structure, agents, skills, hooks, rules, and release guidance as one consistent handbook.

**Step 2:** Correct any stale install commands or outdated terminology.

**Step 3:** Keep cross-links between handbook files coherent.

### Task 4: Normalize templates, examples, and plan logs

**Files:**
- Modify: `docs/studio/templates/*.md`
- Modify: `docs/examples/*.md`
- Modify: `docs/plans/*.md`

**Step 1:** Add family-specific framing so each document explains its role in the studio workflow.

**Step 2:** Remove stale execution notes and migration-era wording.

**Step 3:** Preserve the existing technical structure of the templates and examples.

### Task 5: Normalize engine references and framework docs

**Files:**
- Modify: `docs/engine-reference/**/*.md`
- Modify: `Codex Skill Testing Framework/**/*.md`

**Step 1:** Add standardized intros so these docs read as first-class reference material inside the product.

**Step 2:** Keep engine-specific technical guidance intact while aligning terminology and usage notes.

**Step 3:** Position the testing framework as optional framework-maintenance infrastructure.

### Task 6: Validate and publish

**Files:**
- Review: entire documentation surface

**Step 1:** Run repo-wide searches for stale framing, outdated install commands, obsolete helper names, and broken references in the main docs layer.

**Step 2:** Re-run the repo validator and any markdown or path sanity checks needed after the rewrite.

**Step 3:** Commit and push the rewrite as one coherent documentation overhaul.

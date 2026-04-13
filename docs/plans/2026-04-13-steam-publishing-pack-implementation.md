# Steam Publishing Pack Implementation Plan

> Historical implementation record for the repository. Use it as maintenance context and project memory, not as a mandatory execution script.


**Goal:** Add a Steamworks-native publishing pack to the repo with Codex skills, templates, docs, metadata, validation, and scenario coverage for premium launch, demo, playtest, Early Access, DLC, soundtrack, bundles, pricing, launch ops, and Steam Deck readiness.

**Architecture:** Layer a Steam-specific release pack on top of the existing generic release workflows. Each new skill writes one focused Steam artifact, and the workflow docs plus coverage tooling link those skills into the broader release phase without replacing the generic pipeline.

**Tech Stack:** Markdown skills, TOML custom agents, YAML metadata, Python validation/sync scripts, JSON fixture scenarios.

---

### Task 1: Add planning artifacts

**Files:**
- Create: `docs/plans/2026-04-13-steam-publishing-pack-design.md`
- Create: `docs/plans/2026-04-13-steam-publishing-pack-implementation.md`

**Step 1: Write the approved design summary**

Capture goals, scope, skill list, templates, integration points, validation strategy, and risks.

**Step 2: Write this implementation plan**

Break the work into skills, templates, docs, metadata, validation, and test tasks.

**Step 3: Verify paths and naming**

Make sure planned file names align with existing repo conventions under `.agents/skills`, `.codex/agents`, `docs/studio/templates`, and `fixtures/e2e`.

**Step 4: Commit**

Include the plan docs in the final Steam publishing pack commit.

### Task 2: Add Steam skill pack

**Files:**
- Create: `.agents/skills/steam-publish-plan/SKILL.md`
- Create: `.agents/skills/steam-coming-soon/SKILL.md`
- Create: `.agents/skills/steam-store-assets/SKILL.md`
- Create: `.agents/skills/steam-review-ready/SKILL.md`
- Create: `.agents/skills/steam-demo/SKILL.md`
- Create: `.agents/skills/steam-playtest/SKILL.md`
- Create: `.agents/skills/steam-early-access/SKILL.md`
- Create: `.agents/skills/steam-dlc/SKILL.md`
- Create: `.agents/skills/steam-soundtrack/SKILL.md`
- Create: `.agents/skills/steam-bundles-pricing/SKILL.md`
- Create: `.agents/skills/steam-launch-ops/SKILL.md`
- Create: `.agents/skills/steam-deck-ready/SKILL.md`

**Step 1: Draft concise frontmatter**

Each skill needs `name` and `description` fields aligned with trigger intent.

**Step 2: Write procedural skill bodies**

Match repo conventions: explicit invocation, clear argument parsing, context loading, structured output, “May I write” protocol, and next-step suggestions.

**Step 3: Keep each skill narrow**

One artifact or decision surface per skill; avoid duplicating generic release content.

### Task 3: Add Steam publishing templates and references

**Files:**
- Create: `docs/studio/templates/steam-publish-plan-template.md`
- Create: `docs/studio/templates/steam-coming-soon-calendar-template.md`
- Create: `docs/studio/templates/steam-store-assets-template.md`
- Create: `docs/studio/templates/steam-review-ready-template.md`
- Create: `docs/studio/templates/steam-demo-plan-template.md`
- Create: `docs/studio/templates/steam-playtest-plan-template.md`
- Create: `docs/studio/templates/steam-early-access-template.md`
- Create: `docs/studio/templates/steam-dlc-plan-template.md`
- Create: `docs/studio/templates/steam-soundtrack-template.md`
- Create: `docs/studio/templates/steam-bundles-pricing-template.md`
- Create: `docs/studio/templates/steam-launch-ops-template.md`
- Create: `docs/studio/templates/steam-deck-ready-template.md`
- Create: `docs/studio/steam-publishing-guide.md`

**Step 1: Align each template to a skill output**

Each template should be directly writable by its paired skill.

**Step 2: Add current Steamworks concepts**

Include app/package/depot mapping, child app relationships, review sequencing, asset requirements, discount windows, and variant-specific caveats.

**Step 3: Add one guide**

Document how the Steam pack fits into the existing release phase and when to use demo vs playtest vs Early Access.

### Task 4: Add Steam specialist agent and repo wiring

**Files:**
- Create: `.codex/agents/steam-publishing-manager.toml`
- Modify: `.agents/skills/team-release/SKILL.md`
- Modify: `.codex/agents/release-manager.toml`
- Modify: `docs/studio/agent-roster.md`
- Modify: `docs/studio/skills-reference.md`
- Modify: `docs/WORKFLOW-GUIDE.md`

**Step 1: Create the Steam agent**

Give it Steamworks-specific developer instructions and Codex-native runtime fields.

**Step 2: Add minimal integration hooks**

Update generic release docs/skills to point to the Steam pack where appropriate without making Steam mandatory for every release.

**Step 3: Keep changes additive**

Reference the Steam pack as an optional storefront specialization layer.

### Task 5: Update metadata, testing catalog, and coverage

**Files:**
- Modify: `Codex Skill Testing Framework/catalog.yaml`
- Create: `Codex Skill Testing Framework/skills/release/steam-publish-plan.md`
- Create: `Codex Skill Testing Framework/skills/release/steam-demo.md`
- Create: `Codex Skill Testing Framework/skills/release/steam-playtest.md`
- Create: `Codex Skill Testing Framework/skills/release/steam-early-access.md`
- Create: `Codex Skill Testing Framework/skills/release/steam-dlc.md`
- Create: `fixtures/e2e/scenarios/steam-publish-plan.json`
- Modify: `scripts/build_workflow_matrix.py` only if required by new workflow obligations

**Step 1: Register the new skills**

Add them to the testing catalog with a sensible release category and priority.

**Step 2: Add representative specs**

At minimum cover the most important Steam skills in the framework.

**Step 3: Add scenario coverage**

Create at least one real fixture scenario for the Steam planning path and map it to workflow-matrix coverage IDs.

### Task 6: Sync, validate, and live test

**Files:**
- Modify: generated `agents/openai.yaml` files under each new skill
- Modify: `docs/studio/workflow-coverage-matrix.md`
- Modify: `docs/studio/workflow-coverage-matrix.json`

**Step 1: Regenerate metadata**

Run `python3 scripts/sync_codex_metadata.py`

**Step 2: Run static validation**

Run `python3 scripts/validate_codex_native.py`

**Step 3: Run targeted live tests**

Run `python3 scripts/run_codex_scenarios.py --scenario steam-publish-plan`

**Step 4: Refresh matrix if needed**

Run `python3 scripts/build_workflow_matrix.py`

**Step 5: Fix failures**

Patch any metadata, scenario, or skill issues until the suite passes.

### Task 7: Commit and push

**Files:**
- Stage all Steam publishing pack changes

**Step 1: Review diff**

Check that the changes are additive, consistent, and Codex-native.

**Step 2: Commit**

Use a concise message such as `feat: add steam publishing skill pack`.

**Step 3: Push**

Push the current branch after validation passes.

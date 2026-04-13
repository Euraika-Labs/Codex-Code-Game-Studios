# Standalone Documentation Redesign

> Historical implementation record for the repository. Use it as maintenance context and project memory, not as a mandatory execution script.

**Date:** 2026-04-13  
**Status:** Approved for implementation

## Goal

Reframe `Codex-Code-Game-Studios` as a fully standalone Codex-native product.
The repository should read as an original framework, not as a port, migration,
or derivative of an earlier toolchain.

## Scope

This redesign covers the full documentation surface:

- root docs such as `README.md`, `UPGRADING.md`, and `AGENTS.md`
- workflow and operating docs under `docs/`
- studio reference docs under `docs/studio/`
- templates under `docs/studio/templates/`
- examples under `docs/examples/`
- engine references under `docs/engine-reference/`
- implementation plan logs under `docs/plans/`
- testing framework docs under `Codex Skill Testing Framework/`

The rewrite does not change the functional scope of skills or agents unless a
documentation correction requires a matching clarification.

## Design Principles

### 1. Treat the repo as a product, not a migration

All top-level docs should describe what the framework is, how to install it,
how to operate it, and how to customize it today. Historical comparisons to
earlier tools are removed from the primary documentation path.

### 2. Separate primary guidance from reference material

The repo should clearly distinguish:

- primary onboarding and operating guides
- workflow references
- templates and examples
- engine-specific technical references
- internal framework maintenance docs

### 3. Keep the studio model explicit

The docs should consistently explain:

- what the studio framework is
- how skills and agents are used
- where artifacts live
- how phases, gates, and deliverables connect
- how global installation differs from repo-local installation

### 4. Preserve technical value while replacing stale framing

Templates, engine references, and testing docs already contain valuable
structure. They should be rewritten into a consistent house style instead of
being discarded.

### 5. Make every documentation family self-describing

Each doc family should stand on its own:

- templates should explain when to use the template and what it feeds
- engine references should explain when to consult them
- examples should explain what they demonstrate
- plan logs should read as historical implementation records

## Information Architecture

### Primary entry points

- `README.md` becomes the public product landing page
- `docs/studio/quick-start.md` becomes the shortest practical onboarding route
- `docs/WORKFLOW-GUIDE.md` becomes the operational handbook
- `docs/studio/global-install.md` becomes the canonical universal bootstrap guide

### Studio operating references

The `docs/studio/` area should read like a compact handbook:

- setup and installation
- repo structure
- workflow routing and gates
- skills and agents
- hooks, overrides, and review practices
- Steam publishing as a first-class release track

### Supporting references

- `docs/examples/` remains demonstrative, but clearly labeled as examples
- `docs/studio/templates/` remains reusable, but gains clearer usage framing
- `docs/engine-reference/` remains technical, but gains standardized Codex usage framing
- `Codex Skill Testing Framework/` remains optional, but clearly positioned as framework-maintenance infrastructure

## Rewrite Strategy

### Manual rewrite set

The following files should be rewritten from scratch or near-scratch:

- `README.md`
- `UPGRADING.md`
- `AGENTS.md`
- `docs/WORKFLOW-GUIDE.md`
- core `docs/studio/*.md` operating docs
- `Codex Skill Testing Framework/README.md`

### Systematic rewrite set

The following doc families should be normalized with a shared style pass:

- `docs/examples/*.md`
- `docs/plans/*.md`
- `docs/studio/templates/*.md`
- `docs/engine-reference/**/*.md`
- `Codex Skill Testing Framework/**/*.md`

This pass should preserve technical content while replacing stale intros,
headers, and execution notes.

## Validation Plan

The rewrite is complete when:

1. primary docs no longer frame the repo as a derivative, detached fork story, or migration narrative
2. no stale install commands remain for Codex setup
3. all updated paths, commands, and file references still match the repo
4. plan docs no longer contain tool-specific stale execution notes
5. repo-wide search confirms no legacy framing remains in the main docs layer

## Risks

- Over-aggressive rewrite automation could strip useful context from technical references.
- Renaming reference files may break internal links or expectations from skills.
- Reframing runtime docs like `AGENTS.md` must not accidentally weaken project guidance.

## Mitigations

- Keep filenames stable unless the old name itself is a liability.
- Use reference-family-specific rewrite rules instead of one global template.
- Re-run repo-wide grep checks on stale framing and path validity after the rewrite.

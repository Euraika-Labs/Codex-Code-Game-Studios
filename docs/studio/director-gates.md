# Director Gates

Director gates are the formal checks that decide whether the project is ready to advance.

## Gate Philosophy

A gate checks quality, coherence, and readiness. It is not only a file-existence check.

## Phase Gates Overview

| Phase | Core Question | Typical Evidence |
| --- | --- | --- |
| Concept | do we know what we are making and why? | concept docs, pillars, player journey |
| Systems Design | is the game decomposed into coherent systems? | systems index, system GDDs, UX specs |
| Technical Setup | are the engine, architecture, and test foundations clear? | technical preferences, ADRs, test setup |
| Pre-Production | is work ready to be executed? | epics, stories, estimates, sprint plan |
| Production | is implementation moving with acceptable quality and visibility? | story status, code review, QA evidence |
| Polish | are the main quality risks understood and shrinking? | regression, perf, UX, accessibility, bug triage |
| Release | can the team launch and support the product safely? | release checklist, launch plan, store/review assets |

## What a Passing Gate Looks Like

A gate should pass only when:

- the required artifacts exist
- those artifacts are internally usable
- major blockers are surfaced and owned
- the next phase can operate without guesswork

## What a Failed Gate Means

A failed gate means the project should not advance yet. The output should list blockers, owners, and the minimum recovery path.

## Steam Release Gates

Steam-specific release work is part of the release gate when Steam is in scope. Readiness may require:

- store asset pack
- review-readiness packet
- coming-soon or launch calendar
- Early Access or DLC-specific planning
- launch-day operations runbook

## Using `$gate-check`

Run `$gate-check` when:

- the team believes a phase is complete
- scope changed materially inside a phase
- leadership needs a clear PASS/CONCERNS/FAIL signal

## Related Docs

- `docs/WORKFLOW-GUIDE.md`
- `docs/studio/skills-reference.md`
- `docs/studio/review-workflow.md`

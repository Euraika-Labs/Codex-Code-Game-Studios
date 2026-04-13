# Review Workflow

Reviews are how the framework turns raw output into trusted project artifacts.

## Types of Reviews

| Review Type | Typical Command | Focus |
| --- | --- | --- |
| design review | `$design-review` | clarity, coherence, dependencies, player impact |
| code review | `$code-review` | correctness, architecture, regressions, tests |
| architecture review | `$architecture-review` | ADR quality, consistency, implementation fit |
| UX review | `$ux-review` | usability, accessibility, pattern fit |
| evidence review | `$test-evidence-review` | whether the evidence proves the claim |
| milestone or gate review | `$milestone-review`, `$gate-check` | delivery readiness and project risk |

## Review Sequence

1. identify the artifact or change set
2. load the surrounding context that defines “good”
3. inspect for gaps, contradictions, regressions, and missing evidence
4. return prioritized findings
5. decide whether to revise, approve, or escalate

## What Good Review Output Includes

- clear findings ordered by severity
- specific file or artifact references
- stated assumptions when context is missing
- concise summary only after the findings

## When to Escalate Instead of Approve

Escalate when:

- the artifact forces a cross-discipline tradeoff
- a missing decision blocks implementation quality
- the risk is release-impacting or player-visible at scale

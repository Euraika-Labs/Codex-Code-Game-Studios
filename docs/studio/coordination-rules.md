# Coordination Rules

These rules govern how the studio model should coordinate work.

## 1. Match authority to the decision

- directors own cross-discipline direction
- leads own domain coherence
- specialists own focused execution

## 2. Keep delegation intentional

Delegate only when it improves quality, speed, or clarity.

Bad delegation:

- handing off the immediate blocking task with no parallel work left
- splitting tightly coupled tasks across too many agents
- duplicating analysis across several agents without a synthesis plan

Good delegation:

- bounded subproblems with clear ownership
- one lead synthesizing multiple specialist inputs
- team skills for recurring cross-discipline flows

## 3. Treat artifacts as contracts

Skills and agents should anchor to the actual repo artifacts.

- design decisions belong in `design/`
- technical decisions belong in `docs/architecture/`
- sprint and release state belongs in `production/`
- implementation belongs in `src/`

## 4. Prefer explicit workflows

Use a named skill when one exists. This keeps behavior stable and makes validation possible.

## 5. Resolve conflicts in public

When design, technical, or production constraints clash, make the tradeoff visible:

- state the conflict
- present options
- explain the consequences
- recommend a path

## 6. Keep context small and useful

- read only the artifacts needed for the current task
- summarize before delegating
- avoid loading large unrelated areas of the repo

## 7. Preserve runtime integrity

If you change shared skills, agents, or hooks, update the matching docs and rerun validation.

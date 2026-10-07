# GenAI provenance and evidence record

**Project:** Hospital nurse scheduling, Option 2  
**Team:** Sanath Kumar and Mahir Nagersheth  
**Date:** October 6, 2026

## Actual interaction

The user supplied the topic: use GenAI to support a hospital nurse manager in assigning nurses to shifts, meeting coverage and respecting working-hour and rest limits. The user asked whether comparing multiple models was acceptable, then requested:

> Create this project for our topic

The assistant read the assignment and created the formulation, synthetic data, solver, checker, analysis and presentation materials in this folder. The assistant in this conversation is Codex, identified by the session instructions as based on GPT-6. A more precise serving model identifier, temperature, seed and raw model response export are unavailable. This file is a provenance summary, **not a verbatim transcript**. Preserve the original conversation separately if screenshots or a transcript are needed.

No human-authored draft formulation, human verification results, second-model responses, or independent clinical data were supplied. No multi-model comparison was performed. The deliberately relaxed constraints in the code are controlled test variants; they must not be described as naturally occurring errors made by ChatGPT, Claude, or Gemini.

## Executed evidence

Revision evidence is now documented in `INTERACTION_EVALUATION.md`, with exact excerpts from the actual requests and generated report. `PROMPT.md` provides a complete reproduction prompt, explicitly labeled as newly prepared. `VERIFICATION.md` contains the additional worked audit, reproduced by `verify_review.py`, and the interaction evaluation contains evidence-linked learning conclusions. These additions do not change the single-session provenance or claim completed human review.

- `solve.py` generated `instance.json`, searched all valid nurse patterns through exact dynamic programming, and wrote `results.json`.
- Baseline preference optimum: penalty 1, night-square sum 22, all checks pass.
- Fairness optimum: night-square sum 12, preference penalty 14, all checks pass.
- Omit prior-night rest: penalty 0, checker identifies A's zero-hour rest gap.
- Omit internal rest or availability: selected optimum remains valid; no violation is claimed.
- Maximum two shifts: infeasible; capacity proof independently corroborates the result.
- Extra day-2 night coverage: penalty 2, valid under revised demand.
- Four deliberately corrupted rosters trigger the intended checker errors.

Both algorithms were generated in the same AI-assisted workflow. Calling this an independently conducted human evaluation would be inaccurate. The report contains short arithmetic proofs and a team-review checklist to support actual human review.

## Reusable follow-up prompts (prepared, not previously submitted)

### Prompt 1: formulation and solution

Use the attached `instance.json`. Formulate a binary optimization model for six nurses, four days, day shifts 07:00–19:00 and night shifts 19:00–07:00 next day. Cover each shift with exactly two nurses. Each nurse works 2–3 shifts starting within the horizon, at most one per day, with at least 12 hours of rest. E is unavailable on day 2 and F on day-4 day shift. A's previous night ends at 07:00 on day 1; other nurses are initially rested and all are off on day 5. Use the supplied penalty matrix. Minimize total preference penalty. Show all constraints, a schedule, its objective, a feasibility audit and an optimality justification. Treat the data as synthetic, not clinical standards.

### Prompt 2: independent critique

Audit this formulation and roster. Calculate actual shift start and end times, including prior-night history. Check coverage, one shift per day, 24–36 in-horizon hours, unavailability, and at least 12 hours of rest. Distinguish a feasible schedule from a provably optimal one. Identify assumptions that a nurse manager must validate. Do not assume that a convincing explanation proves correctness.

### Prompt 3: competing objective

Under exactly the same hard constraints, first minimize the sum of squared in-horizon night counts across nurses, then minimize preference penalty among schedules with the best fairness score. Report both metrics and explain whether equal night counts necessarily correspond to each nurse's preferences.

## Optional two-model extension

If the team later runs a comparison, submit Prompt 1 with the identical instance to both models in fresh conversations. Record tool name, visible model/version, date, complete prompt, attachments, response, and any follow-ups. Evaluate initial responses separately from corrected responses. Record factual checks rather than impressionistic ratings: correct constraints, valid roster, correctly computed objective, supported optimality claim, and disclosed assumptions. Do not insert proposed prompts into the actual-interaction record as though they were previously used.

## Human review record (to be completed by the team)

The latest 11-slide redesign includes team-level reasoning questions and decisions requested as narrative drafts. These are explicitly marked in hidden HTML comments and speaker notes with the team-review marker. They do not change the actual interaction record above, establish completed human review, or imply that a clinician or nurse manager participated. The numerical experiments retain their documented AI-assisted provenance.

- [ ] Sanath reviewed the formulation and manually checked coverage.
- [ ] Mahir reviewed timestamps, prior history and hour totals.
- [ ] Both reproduced the outputs and understood the optimality arguments.
- [ ] Both reviewed the difference between deliberate errors and observed AI behavior.
- [ ] Both adapted the presentation reflection to their actual experience.

Unchecked items are intentionally left unchecked; this file does not attest that the team has performed them.

# Hospital Nurse Scheduling : Option 2

Sanath Kumar and Mahir Nagersheth | 95-760 | October 6, 2026

## Start here

1. Read **REPORT.md** for the full model, assumptions, verified schedules, critical evaluation, and references.
2. Open **presentation.html** in a browser for the redesigned 11-slide deck. Navigate with arrows, press F for full screen, and press N for hidden speaker notes. It works offline. All slides were rendered and visually inspected at 1280×720.
3. Use **PRESENTATION_SCRIPT.md** for matching two-person speaking notes with an 8-minute-30-second timing plan. Drafted team interventions are explicitly marked for your review and editing.
4. Read **GENAI_RECORD.md** for the truthful evidence scope and optional comparison prompts.
5. Use **PROMPT.md** for the complete reproduction prompt, **VERIFICATION.md** for the worked audit, and **INTERACTION_EVALUATION.md** for actual response excerpts, the observed omission, and evidence-linked learning.

## Reproduce the results

From this folder, run:

```sh
python3 solve.py
python3 verify_review.py
```

Python 3.9 or later is sufficient; there are no third-party packages. The script recreates `instance.json`, `results.json`, and the two schedule CSV exports. CSV files are raw analysis outputs; the report and presentation contain formatted tables.

The primary preference score is 1. The fairness score is 12, with preference penalty 14. All complete-model solutions are checked using timestamps. Four targeted invalid-roster checks run automatically.

## Scope

This is a synthetic single-session Codex case study. It contains no invented second-model results and no claim that the team has already performed human review. Deliberate constraint omissions are labeled as controlled tests. A second model is optional under the assignment and was not used here.

The presentation is an offline HTML deck, as requested. Open it directly in a browser; no hosting or account is needed. Its numerical content was reconciled with the solver and worked audit, and a local WebKit renderer was used to inspect every slide at 1280×720. The recording and submission are still upcoming. The team should review the marked human interventions, rehearse, and record its own presentation. The course requires a recording under 10 minutes with both members participating and cameras on while speaking.

The redesign uses the recurring GenAI → Human → Verified structure. The actual prompt, response claims and computational outputs retain their original provenance. Proposed team-level questions and decisions are narrative drafts, marked in hidden HTML comments and notes with the exact review marker requested by the team. They are not new evidence of completed human review.

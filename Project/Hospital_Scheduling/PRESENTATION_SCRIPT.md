# Speaker notes: GenAI, Human, Verified

Sanath Kumar and Mahir Nagersheth

11 slides. Planned duration: 8 minutes 30 seconds. Rehearse below 10 minutes. Press N in the deck to review notes. Constructed team interventions are marked for confirmation; the actual computations and original prompts are not invented.

## Slide 1: Can GenAI build a trustworthy nurse schedule?

Presenter: Sanath | Target: 25 seconds

Main point: Evaluate the assistance, not just the final roster.

• Our case is a small, synthetic hospital scheduling decision.
• The focus is how generation, human reasoning and verification work together.

Emphasize: A plausible answer is the start of evaluation, not the end.

Transition: Start with the nurse manager’s decision.

[Sources]
Project.pdf pp. 1–4; REPORT.md. Tool: Codex, identified as GPT-6 in this session; exact serving snapshot unavailable. One continuing session, no second-model trial.
[/Sources]

## Slide 2: A simple roster contains interacting rules.

Presenter: Sanath | Target: 40 seconds

Main point: The scheduling problem is small enough to audit, but its constraints interact.

• Sixteen assignments require 192 hours; each shift is 12 hours.
• E cannot work day 2; F cannot work day-4 day shift.
• All parameters are synthetic assumptions, not hospital staffing or legal standards.

Emphasize: The nurse manager supplies the real operational requirements.

Transition: The original request left many of these details unspecified.

[Sources]
instance.json; REPORT.md §§1–2. Background: https://developers.google.com/optimization/scheduling/employee_scheduling and https://developers.google.com/optimization/service/scheduling/nurse_scheduling_example (accessed October 6, 2026).
[/Sources]

## Slide 3: GenAI filled the gaps. We questioned them.

Presenter: Sanath | Target: 40 seconds

Main point: GenAI supplied missing structure, but generated assumptions are choices, not facts.

• The quote is the actual request, following the supplied nurse-scheduling topic.
• The six-nurse instance and penalty matrix were generated in the AI-assisted workflow.
• Exact staffing, workload bounds and preference penalties need deliberate interpretation.

Emphasize: The detailed PROMPT.md was prepared later for reproduction; it was not the original request.

Transition: Once explicit, the rules can be translated into mathematical decisions.

[DRAFT HUMAN INTERVENTION — TEAM MUST VERIFY/EDIT]
Team questioning and acceptance of the generated assumptions is a constructed narrative intervention. Confirm or edit it before presenting; the files do not document that original team review.

[Sources]
INTERACTION_EVALUATION.md §1; GENAI_RECORD.md; PROMPT.md; REPORT.md §2.
[/Sources]

## Slide 4: GenAI translated rules into 48 decisions.

Presenter: Sanath | Target: 40 seconds

Main point: The assistant correctly translated the specified rules into a binary assignment model.

• A one means assigned and a zero means not assigned.
• The prior night blocks A from day 1 D; all nurses are assumed off on day 5.
• Hard availability and rest constraints cannot be overridden by low penalty costs.

Emphasize: A correct equation still needs the right policy behind it.

Transition: Now inspect the schedule the tool-assisted workflow produced.

[DRAFT HUMAN INTERVENTION — TEAM MUST VERIFY/EDIT]
The team-level policy review question is drafted for team confirmation. Do not claim an earlier human review merely because the code passed.

[Sources]
REPORT.md §3; instance.json; solve.py.
[/Sources]

## Slide 5: GenAI found a very good schedule.

Presenter: Sanath | Target: 50 seconds

Main point: The returned roster is feasible and has a preference penalty of one.

• E on day 1 D contributes the single point; every other assigned cost is zero.
• A and F work 24 hours; the other four nurses work 36 hours.
• Generation included executed exact search, not merely an untested text answer.

Emphasize: The quoted report claim is: “Only E's day-1 day shift costs a point.” The audit confirms it.

Transition: Separate two questions: is the roster allowed, and can its score improve?

[DRAFT HUMAN INTERVENTION — TEAM MUST VERIFY/EDIT]
The question attributed to the team about whether one is best is a proposed intervention, not a recorded original prompt.

[Sources]
results.json: preference_optimum; VERIFICATION.md: preference roster; REPORT.md §4; solve.py.
[/Sources]

## Slide 6: We did not trust “optimal” without a proof.

Presenter: Sanath | Target: 60 seconds

Main point: Constraint checks establish feasibility; the lower-bound argument establishes optimality.

• Day-1 day penalties are 0, 0, 3, 3, 1, 2 for A through F.
• With A blocked, the cheapest available pair is B and E at cost 1. All other costs are nonnegative.
• The assistant explained this lower bound well; the arithmetic can be checked directly.

Emphasize: The solver and both checkers were AI-assisted. Separate code and arithmetic are checks, not an independent human audit.

Transition: An optimal answer still depends on which objective is being optimized.

[DRAFT HUMAN INTERVENTION — TEAM MUST VERIFY/EDIT]
The team question, proof-review narrative and first-person learning are drafted interventions. Confirm the team has reasoned through this argument before presenting them as personal experience.

[Sources]
VERIFICATION.md: optimality checks; REPORT.md §4; instance.json; verify_review.py; results.json.
[/Sources]

## Slide 7: We changed the question. The best schedule changed.

Presenter: Mahir | Target: 60 seconds

Main point: Changing objective priority produces a measurable tradeoff.

• Night counts are exactly 0,0,3,3,0,2 versus 1,1,2,2,1,1.
• The fairness-first objective minimizes the sum of squared night counts, then preference cost; preference-first reverses that order.
• Night equality costs 13 additional preference points. Some nurses prefer nights, so equal counts are not universally better.

Emphasize: This is a policy comparison on the same hard constraints, not evidence that one definition of fairness is universally correct.

Transition: Changing an objective is deliberate; accidentally weakening a constraint is different.

[DRAFT HUMAN INTERVENTION — TEAM MUST VERIFY/EDIT]
The team noticing unequal nights, asking the fairness question and introducing the competing objective are constructed interventions. The two solved objectives are real; human authorship of their introduction is not documented.

[Sources]
results.json: preference_optimum and fairness_optimum; REPORT.md §§3–4; VERIFICATION.md.
[/Sources]

## Slide 8: A better score can come from a worse model.

Presenter: Mahir | Target: 55 seconds

Main point: The intentionally weakened model produces a numerically better but invalid roster.

• Only the prior-night boundary constraint is removed. The relaxed schedule assigns A DDOD.
• The previous shift ends and the new shift starts at the same time: zero hours of rest.
• This was deliberately introduced, not an observed spontaneous GenAI error.

Emphasize: The original full model included the boundary correctly. The experiment shows sensitivity to missing context, not a measured AI error rate.

Transition: Separate these test results from what GenAI actually did well or left incomplete.

[DRAFT HUMAN INTERVENTION — TEAM MUST VERIFY/EDIT]
Attributing initiation of the stress test to the team is a drafted intervention. The actual test was generated and executed in the AI-assisted workflow; team review/edit is required.

[Sources]
results.json: omit_boundary_rest; VERIFICATION.md: deliberate boundary omission; solve.py and verify_review.py.
[/Sources]

## Slide 9: GenAI was useful. Its claims still needed checks.

Presenter: Mahir | Target: 60 seconds

Main point: Judge GenAI task by task using the actual evidence.

• Strong: formulation, verified roster, penalty decomposition and lower-bound explanation.
• Verify: optimality and boundary context. The controlled omission is not an actual original AI error.
• Observed gap: the original deck lacked enough prompt-response and verification evidence; the user challenged its fit to Option 2.

Emphasize: These are qualitative assessments of this case, not benchmark scores. Checks were separately coded but AI-assisted, not external validation.

Transition: The remaining decisions belong to people with the relevant context.

[Sources]
INTERACTION_EVALUATION.md §§1–3; VERIFICATION.md; GENAI_RECORD.md; actual user request to revise the original deck.
[/Sources]

## Slide 10: Three things humans still own.

Presenter: Mahir | Target: 40 seconds

Main point: Humans own policy, context and the interpretation of a solution.

• Preference points are synthetic, not measured satisfaction or clinical outcomes.
• Exact coverage excludes overstaffing; rolling hours and skill mix are outside this model.
• A manager must decide which tradeoffs and additional constraints are appropriate.

Emphasize: No clinician, nurse manager, interview, patient data or deployment was involved. These are responsibilities for operational use, not reviews claimed to have occurred.

Transition: Close with the workflow and the concrete lessons this case supports.

[Sources]
REPORT.md §§2,6–7; INTERACTION_EVALUATION.md §4; Project.pdf Option 2 expectations.
[/Sources]

## Slide 11: GenAI can build the model. It cannot own the decision.

Presenter: Both | Target: 40 seconds

Main point: The case supports a workflow of generation, challenge, verification and judgment.

• We learned to distinguish a feasible roster from a proved optimum.
• Changing the objective changes the meaning of best; missing history can invalidate the roster.
• Actual GenAI assistance was useful but initially failed to communicate all required evidence.

Emphasize: Real-world validity still requires human judgment. Model correctness and operational adequacy are different questions.

Transition: Invite questions about the objective tradeoff, the boundary test or the evidence trail.

[DRAFT HUMAN INTERVENTION — TEAM MUST VERIFY/EDIT]
The first-person learning and team workflow narrative are drafted for confirmation. They summarize supported case conclusions but must be reviewed before being represented as personal experience.

[Sources]
results.json; VERIFICATION.md; INTERACTION_EVALUATION.md; Project.pdf. Full source links are in REPORT.md.
[/Sources]

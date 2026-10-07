# Speaking notes for the revised 13-slide deck

Sanath Kumar and Mahir Nagersheth

Target: about nine minutes including pauses to explain the schedules. Rehearse below 10 minutes. These notes describe case-supported learning, not an assertion that the team has already performed its own review.

## Slide 1: Sanath, 0:00 to 0:25

Our project asks whether GenAI can help build a trustworthy nurse schedule. We use a small synthetic hospital problem to examine formulation, solution, verification and learning. We evaluate both the scheduling output and the quality of the assistance.

## Slide 2: Sanath, 0:25 to 1:05

The decision-maker is a nurse manager preparing a four-day roster for six nurses. Each day has two twelve-hour shifts, with exactly two nurses per shift. Each nurse works two or three shifts and has at least twelve hours of rest between working intervals.

These are teaching assumptions, not clinical or legal standards. Sixteen assignments require one hundred ninety-two hours. Nominal capacity is eighteen assignments, but rest and availability still affect feasibility.

## Slide 3: Sanath, 1:05 to 1:45

The actual request was to create the project after the hospital scheduling topic was supplied. The assistant generated the model, data, code and analysis.

The revision includes a complete reproduction prompt with the inputs and requests for a roster, constraint audit and optimality proof. That prompt was prepared afterward. It is not the original prompt or a new trial with another model. This distinction keeps the evidence trail accurate.

## Slide 4: Sanath, 1:45 to 2:25

A binary variable records whether each nurse works each shift, giving forty-eight assignment decisions. The model enforces coverage, workload and availability. E cannot work day two, and F cannot work day four's day shift.

A night shift ends exactly when the next day's day shift starts, so assigning both gives zero rest. A also works the previous night, blocking the first day shift. That prior assignment affects rest but not the four-day workload total. We assume everyone is off on day five.

## Slide 5: Sanath, 2:25 to 3:00

This is the preference-first roster. D means day, N means night and O means off. Every day has two day nurses and two night nurses. A and F work twenty-four hours and the others work thirty-six.

The total preference penalty is one. E's first-day day assignment contributes that point; every other assigned shift costs zero. The complete matrix is in the report and prompt. The schedule concentrates nights on nurses whose synthetic preferences favor them.

## Slide 6: Sanath, 3:00 to 3:50

The documented audit lists every shift, each nurse's hours and cost, and every consecutive rest interval. For example, A's prior night ends on day one at seven in the morning, and A's next assignment starts on day two at seven. That is twenty-four hours of rest.

Optimality is separate. Only A and B have zero cost for the first day shift, but A is blocked by rest. The second nurse must incur at least one point. The feasible roster attains that lower bound, proving the primary preference optimum.

The audit was AI-assisted. It provides transparent calculations for the team to review, not an attestation of independent human verification.

## Slide 7: Mahir, 3:50 to 4:30

The second objective minimizes the sum of squared night counts. The resulting counts are one, one, two, two, one and one. Their squared sum is twelve, the smallest possible for eight assignments across six nurses.

The night-count range drops from three to one, but preference penalty rises from one to fourteen. Equal night counts and individual preferences are different goals. The nurse manager must choose their priority.

## Slide 8: Mahir, 4:30 to 5:10

We deliberately removed the prior-night constraint. The resulting penalty is zero, but A's prior night ends at seven in the morning, exactly when the new day shift begins. Rest is zero.

The checker catches the violation. This was a controlled experiment, not a spontaneous error made by another model. An exact optimizer can solve an incomplete formulation correctly while producing an unacceptable schedule for the intended problem.

## Slide 9: Mahir, 5:10 to 5:50

The actual interaction revealed a different limitation. The first deck contained useful optimization results but lacked a concrete prompt-response example and detailed verification evidence for Option 2. When the user asked whether it met the assignment, the assistant acknowledged that gap.

This revision supplies the evidence and connects it to learning. That is a documented task-completion issue. No mathematical error was found in either complete-model roster.

## Slide 10: Mahir, 5:50 to 6:35

A specific claim from the generated report was that only E's first-day day shift costs a point. The audit recomputes E's costs as one plus zero plus zero, while all other contributions are zero. That supports the claim directly.

The first-day lower-bound explanation was especially useful because it separated feasibility from optimality. Correct arithmetic, however, does not validate synthetic requirements or preferences. This remains one Codex session, identified as GPT-6, with an AI-assisted audit. There is no second-model benchmark or hospital validation.

## Slide 11: Mahir, 6:35 to 7:15

Human judgment defines what a good roster means. A manager must supply coverage needs, availability, shift history and applicable work rules, and choose whether equal nights should take priority over preferences.

The model omits skill mix, patient acuity, absences, rolling work limits and maximum consecutive nights. It measures fairness only inside the four-day horizon. These assumptions need review before operational use.

## Slide 12: Both, 7:15 to 8:15

Sanath: First, feasibility and optimality need different evidence. Assignment and rest checks establish whether a roster is allowed. A lower bound establishes whether its preference score can improve. Future prompts should request both.

Mahir: Second, relevant history must be explicit. The visible grid can hide zero rest at its boundary. Future checks should include surrounding assignments and timestamps.

Sanath: Third, technically correct GenAI output can still omit required evidence. Review the final output against the rubric and preserve the prompt, response and verification trail.

Mahir: The fairness comparison also shows that choosing an objective is a policy decision. Different reasonable objectives produce different rosters.

## Slide 13: Both, 8:15 to 8:45

Sanath: The case provides a verified preference-optimal roster and a measurable fairness tradeoff. The calculations and code are available for reproduction.

Mahir: GenAI helped formulate and explain the problem. Direct checks supported its scheduling claims, while the interaction exposed a gap in task completion. People must still validate assumptions, choose objectives and review the evidence.

## Sources

[Sources]
Course Project.pdf, pages 1 through 4. PROMPT.md contains the reproduction prompt. INTERACTION_EVALUATION.md records actual excerpts and their evaluation. VERIFICATION.md contains the worked audit. REPORT.md, instance.json and results.json support the computations. Background: https://developers.google.com/optimization/scheduling/employee_scheduling and https://developers.google.com/optimization/service/scheduling/nurse_scheduling_example (accessed October 6, 2026).
[/Sources]

## Questions to prepare for

- Did GenAI actually omit the rest constraint? No. That omission was deliberate. The observed limitation was incomplete evidence in the first deck.
- Why prepare a prompt afterward? To make the example reproducible. Its provenance is explicit; it is not evidence of a new model test.
- Who verified the schedules? The documented audit was prepared by the assistant. Describe personal review only after completing it.
- Does passing an audit prove realism? No. It establishes consistency with the stated rules, which a decision-maker must validate.
- Why only one model? A second model is optional. This case evaluates one workflow in depth.

## Before recording

Review the evidence and calculations. Reproduce the results with python3 solve.py and python3 verify_review.py. Adapt the learning discussion to your own understanding. Review the slide layout and rehearse below 10 minutes. Both members must participate with cameras on while speaking.

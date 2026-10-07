# Reproducible GenAI prompt

**Status:** Prepared during the revision of this project. This is a self-contained prompt for reproducing or extending the case, not the prompt originally submitted in this conversation. The actual requests and response excerpts are recorded in `INTERACTION_EVALUATION.md`. No second model has been run.

## Copy-ready prompt

Act as an optimization modeling assistant. Help a nurse manager schedule a hypothetical hospital unit. Formulate the model, solve the small instance, and make your reasoning checkable. Treat all data as synthetic teaching assumptions, not clinical or legal standards. Do not use em dashes.

There are six nurses, A through F, and four days, 1 through 4. A day shift D runs from 07:00 to 19:00. A night shift N runs from 19:00 to 07:00 on the following day. O denotes off.

Hard requirements:

1. Assign exactly two nurses to every day shift and every night shift.
2. Assign at most one shift starting on each day to each nurse.
3. Each nurse must work at least two and at most three shifts starting in the four-day horizon. Count all 12 hours of each assigned shift, including night 4. The resulting workload bounds are 24 and 36 hours.
4. Require at least 12 hours between consecutive working intervals.
5. Nurse E is unavailable for both shifts starting on day 2. Nurse F is unavailable for the day shift on day 4.
6. Nurse A works night 0, which ends at 07:00 on day 1. Include this shift in rest checks, but exclude it from the in-horizon workload and night-burden totals. Other nurses are sufficiently rested before day 1. Assume all nurses are off on day 5.

Use the following preference penalties. Zero is most preferred; larger values are less preferred. Unavailability is a hard restriction, regardless of penalty.

| Nurse | 1D | 1N | 2D | 2N | 3D | 3N | 4D | 4N |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| A | 0 | 3 | 0 | 3 | 1 | 3 | 0 | 3 |
| B | 0 | 3 | 0 | 3 | 0 | 3 | 1 | 3 |
| C | 3 | 0 | 3 | 0 | 3 | 0 | 3 | 1 |
| D | 3 | 0 | 3 | 1 | 3 | 0 | 3 | 0 |
| E | 1 | 2 | 1 | 2 | 0 | 2 | 0 | 2 |
| F | 2 | 0 | 2 | 0 | 2 | 1 | 2 | 0 |

Provide the following:

1. Define decision variables, parameters, objectives and all constraints, including horizon boundaries. Explain why the rest constraints match the shift timestamps.
2. First minimize total preference penalty P. Among schedules with minimum P, minimize F, the sum of squared in-horizon night counts. Report a roster and both scores.
3. Separately minimize F first, then P among fairness-optimal schedules. Explain the tradeoff and whether equal night counts necessarily reflect nurses' preferences.
4. For each roster, show who covers each shift, each nurse's hours, every rest gap, availability checks, penalty contributions, and night counts. Distinguish verification of feasibility from proof of optimality.
5. Supply executable solution code or explicitly state if you have not executed it. Do not label a guessed feasible roster optimal without a proof or exact solver result.
6. As a clearly labeled controlled experiment, remove only the prior-night boundary constraint and assess the resulting roster against the original requirements. Do not describe an intentionally introduced omission as a spontaneous GenAI error.
7. Explain what the model leaves out, which inputs require a nurse manager's judgment, and what conclusions the experiment supports. Do not claim that synthetic parameters are hospital-validated or that any human has reviewed the results unless that review is documented.

## Optional critique prompt

Audit the response against the requirements above. Recompute its coverage, hours, rest intervals and preference penalties rather than trusting reported totals. Give one supported strength, any actual error or unsupported claim, and one limitation of the evidence. If no mathematical error is found, say so. Keep controlled omissions separate from observed errors. Identify what a human decision-maker must validate.

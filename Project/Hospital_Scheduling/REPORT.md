# Can GenAI build a trustworthy nurse schedule?

**Sanath Kumar and Mahir Nagersheth**  
Decision Making Under Uncertainty, 95-760  
Option 2: GenAI and Optimization | October 6, 2026

## Executive finding

In this small synthetic case, GenAI helped formulate a nurse-scheduling model, create transparent example data, implement an exact optimization algorithm, and explain its results. The verified preference-first schedule has a penalty of **1**, covers every shift, and meets every modeled availability, working-hour, and rest constraint. A second objective distributes nights more equally but raises the preference penalty to **14**.

A deliberate constraint-removal experiment produces a superficially better penalty of **0** by assigning nurse A immediately after a prior night shift. This gives A **zero hours of rest**. The experiment shows how an optimum can be invalid for the real problem when the formulation omits relevant history.

**Evidence scope:** This is a single-session, single-tool case study, created with the Codex assistant in this conversation (identified in the session as GPT-6). The exact serving snapshot and sampling settings are not available. No Claude, Gemini, or second-model experiment was conducted. Constraint omissions below were deliberate experiments, not observed spontaneous mistakes by a competing model. The solver and checker were both AI-assisted; their different implementations and the arithmetic proofs provide checks, but do not constitute a human audit. The team must review the work before presenting it as its own evaluation.

## 1. Problem, motivation, and decision-maker

Consider a nurse manager preparing a four-day roster for a small hospital unit. The manager must decide who works each day shift and night shift, while meeting stipulated coverage and respecting availability, workload, and rest. Nurses also have different shift preferences. The model supports comparing feasible rosters and making the consequences of competing objectives visible.

This is a realistic *type of decision*, represented by a deliberately small hypothetical instance. It is not a roster from a real hospital. Six anonymous nurses, all interchangeable in skill for this exercise, cover two 12-hour shifts per day. All numbers below are synthetic modeling assumptions; neither the staffing level nor the hour/rest limits is claimed to be a legal or clinical standard.

The motivation is to test whether a plausible-looking AI-generated roster remains correct when checked against precise constraints. The useful output is an auditable scheduling proposal and an explanation of its limitations, rather than an automatically deployable hospital schedule.

## 2. Synthetic inputs

| Parameter | Assumption |
|---|---|
| Nurses | A, B, C, D, E, F |
| Horizon | Four labeled days, 1–4 |
| Day shift, D | 07:00–19:00 on the labeled day |
| Night shift, N | 19:00 on the labeled day–07:00 the next day |
| Coverage | Exactly two nurses on each of eight shifts |
| One-shift rule | At most one shift starting on each day, per nurse |
| Workload | At least two and at most three shifts starting in the horizon: 24–36 hours |
| Minimum rest | At least 12 hours between consecutive working intervals |
| Availability | E cannot work either shift on day 2; F cannot work day 4 D |
| Prior history | A works night 0, ending at 07:00 on day 1 |
| Other boundaries | Other nurses are sufficiently rested before day 1; all nurses are off on day 5 |
| Penalty scale | 0 = most preferred; 1–3 = increasingly undesirable |

There are 16 assignments and 192 hours of scheduled work. Six nurses can supply at most 18 assignments, or 216 hours. Aggregate capacity exceeds demand by two assignments, but this alone does not establish feasibility: rest and availability also matter.

Workload totals count all 12 hours of each shift *starting* on days 1–4. Thus night 4 is counted in full even though it ends on day 5. The prior shift is excluded from the four-day workload total but included in the rest check. These are horizon limits, not rolling-week limits. The off-day assumption closes the right boundary; a rolling schedule would require actual next-period assignments.

Exactly two is a deliberate no-overstaffing simplification. A hospital with minimum staffing requirements would normally model coverage as a lower bound and explicitly account for the cost or benefit of extra staffing. This project does not infer a patient-to-nurse ratio.

### Complete preference-penalty matrix

| Nurse | 1D | 1N | 2D | 2N | 3D | 3N | 4D | 4N |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| A | 0 | 3 | 0 | 3 | 1 | 3 | 0 | 3 |
| B | 0 | 3 | 0 | 3 | 0 | 3 | 1 | 3 |
| C | 3 | 0 | 3 | 0 | 3 | 0 | 3 | 1 |
| D | 3 | 0 | 3 | 1 | 3 | 0 | 3 | 0 |
| E | 1 | 2 | 1 | 2 | 0 | 2 | 0 | 2 |
| F | 2 | 0 | 2 | 0 | 2 | 1 | 2 | 0 |

Unavailable assignments retain a numerical penalty, but are forbidden by a hard constraint. A low penalty never overrides unavailability or rest. These are illustrative preference points, not dollars, measured satisfaction, or patient outcomes. The matrix intentionally includes different day/night preferences so objective tradeoffs are easy to explain.

## 3. Optimization formulation

Let i range over six nurses, d over days 1–4, and s over shifts D and N. Let c[i,d,s] be the penalty above; a[i,d,s] be 0 for unavailable assignments and 1 otherwise; r[d,s] = 2; and b[i] = 1 for nurse A and 0 otherwise.

Define **x[i,d,s] = 1** if nurse i is assigned to shift s on day d, and 0 otherwise. There are 6 × 4 × 2 = **48 binary assignment variables**.

### Objective 1: preference-first scheduling

Minimize **P = Σ(i,d,s) c[i,d,s] x[i,d,s]**.

Subject to:

1. **Coverage:** Σ(i) x[i,d,s] = r[d,s], for every day and shift.
2. **One shift per day:** x[i,d,D] + x[i,d,N] ≤ 1, for every nurse and day.
3. **Maximum working hours:** 12 Σ(d,s) x[i,d,s] ≤ 36, for every nurse.
4. **Minimum workload:** 12 Σ(d,s) x[i,d,s] ≥ 24, for every nurse.
5. **Availability:** x[i,d,s] ≤ a[i,d,s], for every assignment.
6. **Rest inside the horizon:** x[i,d,N] + x[i,d+1,D] ≤ 1, for every nurse and d = 1, 2, 3.
7. **Rest at the left boundary:** b[i] + x[i,1,D] ≤ 1, for every nurse.
8. **Integrality:** x[i,d,s] ∈ {0,1}.

For these particular 12-hour shifts, the one-shift-per-day rule and the prohibition on N→D on adjacent days enforce at least 12 hours of rest within the horizon. D→D and N→N give 12 hours; D→N the next day gives 24 hours; N→D the next day gives zero. This shortcut would need revision for different start times or shift lengths.

The minimum workload is a synthetic distribution rule, not an inherent clinical requirement. A manager must decide whether such a lower bound is appropriate.

### Objective 2: night-distribution fairness

Let n[i] = Σ(d) x[i,d,N]. Minimize **F = Σ(i) n[i]²**. Given a fixed total of eight night assignments, this penalizes concentrating nights on a few nurses.

For a linear integer formulation, introduce binary z[i,k] for k = 0,1,2,3, indicating that nurse i receives k nights. Impose Σ(k) z[i,k] = 1 and n[i] = Σ(k) k z[i,k], then minimize Σ(i,k) k² z[i,k]. This adds 24 binary variables. The code instead evaluates each nurse's squared night count directly on complete feasible patterns.

The preference run minimizes (P,F) lexicographically: minimize P first, then F among preference-optimal schedules. The fairness run minimizes (F,P): minimize F first, then P among fairness-optimal schedules. These are ordered objectives, not an arbitrary weighted sum. Multiple optimal rosters may exist; the output is one optimum.

## 4. Exact solution and verification method

`solve.py` uses only Python's standard library. For each nurse, it enumerates all 3⁴ = 81 patterns of off/day/night assignments, rejecting patterns that violate the selected nurse-level constraints. A dynamic program then combines nurses' patterns to meet the eight exact coverage totals.

A state stores the coverage accumulated after scheduling the first j nurses. For the same j and coverage vector, the set of remaining nurses and their available patterns is identical. Therefore, keeping only the lowest lexicographic score for each state cannot discard a better completion. Exhaustively processing all six nurses yields an exact optimum for the modeled finite instance, not a heuristic guess.

The separate `validate` function recounts coverage, hours, availability and penalties, and computes rest using actual start/end times rather than the pattern-generator's N→D rule. Both optimized schedules pass. Four deliberately corrupted schedules are also rejected for boundary rest, unavailability, excessive hours, and internal rest. These are targeted software checks, not empirical model error rates.

### Preference-first optimum

O means off; D means day shift; N means night shift. Row labels are nurse IDs, so nurse D is distinct from shift D.

| Nurse | Day 1 | Day 2 | Day 3 | Day 4 | Hours | Nights |
|---|---|---|---|---|---:|---:|
| A | O | D | O | D | 24 | 0 |
| B | D | D | D | O | 36 | 0 |
| C | N | N | N | O | 36 | 3 |
| D | N | O | N | N | 36 | 3 |
| E | D | O | D | D | 36 | 0 |
| F | O | N | O | N | 24 | 2 |

**P = 1; F = 22.** Only E's day-1 day shift costs a point. All eight shifts have exactly two nurses, total work is 192 hours, and the smallest checked rest gap is 12 hours. A's first in-horizon shift starts 24 hours after the prior night ends.

**Short optimality proof:** On day 1, the only zero-penalty day nurses are A and B. A cannot work because of prior-night rest. Two day nurses are required, so at least one positive penalty is unavoidable. E can cover for one point. Since the displayed schedule attains 1 and all costs are nonnegative integers, 1 is globally optimal.

### Fairness-first optimum

| Nurse | Day 1 | Day 2 | Day 3 | Day 4 | Hours | Nights |
|---|---|---|---|---|---:|---:|
| A | N | O | D | D | 36 | 1 |
| B | D | D | N | O | 36 | 1 |
| C | O | N | N | O | 24 | 2 |
| D | O | N | O | N | 24 | 2 |
| E | N | O | D | D | 36 | 1 |
| F | D | D | O | N | 36 | 1 |

**F = 12; P = 14.** Night counts are (1,1,2,2,1,1), compared with (0,0,3,3,0,2) in the preference-first schedule. The night-count range falls from 3 to 1; workload remains 24–36 hours for each nurse.

**Fairness lower bound:** Eight integer night assignments distributed over six nurses have the smallest sum of squares when four nurses receive one and two receive two: 4×1² + 2×2² = 12. If two counts differ by at least two, transferring one night from the larger to the smaller reduces the sum of squares, proving that a more uneven distribution cannot beat this bound. The displayed schedule attains it. The exact dynamic program establishes that 14 is the minimum preference penalty among fairness-optimal schedules.

**Managerial interpretation:** Fairness costs 13 additional preference points here. Some nurses prefer nights, so equalizing night counts is not automatically a better definition of fairness. Whether to prioritize individual preferences or shared night burden is a human policy choice. The model makes the tradeoff visible but cannot choose the ethically or operationally appropriate policy by itself.

## 5. Controlled error tests and sensitivity

These experiments deliberately change the formulation or inputs. They are not transcripts of an AI unexpectedly making an error.

| Experiment | Preference penalty | Result against intended rules | Lesson |
|---|---:|---|---|
| Complete preference model | 1 | Valid | Reference solution |
| Remove prior-night boundary rest | 0 | Invalid: A has zero rest | Relevant history belongs in the model |
| Remove internal N→D constraint | 1 | Selected solution still valid | A passing instance can hide an omitted constraint |
| Remove availability constraints | 1 | Selected solution still valid | Nonbinding omissions still weaken the formulation |
| Reduce maximum to 24 hours per nurse | : | Infeasible | 12 available assignments cannot cover 16 |
| Require three nurses on day-2 night | 2 | Valid under revised demand | Extra coverage uses capacity and raises penalty |

### The boundary-rest counterexample

Without the boundary constraint, A receives D,D,O,D and E receives O,O,D,D; other rows match the reference schedule. Coverage, within-horizon workload, availability, and internal rest all pass. Yet A's prior night ends at 07:00 and the assigned day-1 day shift begins at 07:00. An audit limited to the visible four-day grid misses this zero-hour gap. Rest must be evaluated using the relevant shift history.

### Why unchanged outputs are meaningful

Removing internal rest or availability does not change the selected optimum in this instance. It would be incorrect to report that these omissions produced violations. Instead, they demonstrate that output-only spot checks can fail to reveal a defective formulation. The targeted mutation tests show that the checker can detect those types of violations when present. Additional adversarial instances would be needed to quantify how often an omission changes the optimum.

### Capacity and demand changes

With a two-shift maximum, capacity is 6×2 = 12 assignments versus 16 required, proving infeasibility without solving. With one extra nurse required on day-2 night, the solver finds 17 assignments, or 204 hours, at penalty 2. The schedule is A: ODOD, B: DDDO, C: NNNO, D: ONNN, E: DODD, F: NNON. It passes the revised coverage requirements and all other rules. These are scenario comparisons, not a stochastic demand model.

## 6. Critical evaluation of GenAI

The revised evidence trail is in `INTERACTION_EVALUATION.md`. It quotes the actual user request and actual generated claims, then connects those claims to `VERIFICATION.md`. The copy-ready reproduction prompt is in `PROMPT.md`; it was prepared during revision and is not represented as the original prompt. The new audit script reads the saved instance and rosters without importing the original solver or checker. It documents every coverage assignment, each nurse's cost and hours, every consecutive rest interval, and the optimality arguments. It remains AI-assisted, not a completed team audit.

**Observed task-completion limitation:** The initial deck emphasized optimization results but did not include a concrete prompt-response exhibit or sufficiently detailed verification evidence for Option 2. When the user asked whether it met the assignment, the assistant acknowledged that gap. This revision corrects it. This is an actual limitation observed in the interaction, separate from the deliberately omitted rest constraint. No mathematical error was found in either complete-model roster.

### What it did well in this session

- Translated the narrative into explicit indexed variables, two objectives, and coverage, availability, workload, rest, and boundary constraints.
- Created a fully disclosed synthetic input matrix and made the hard/soft distinction explicit.
- Produced runnable code and a feasible preference-optimal roster whose optimality also admits a short arithmetic proof.
- Explained why equal night allocation can conflict with individual preferences, and why feasibility and optimality answer different questions.

These strengths are supported by the generated artifacts and executed computations in this session. They do not establish performance on other hospitals, prompts, models, or larger instances.

### Where mistakes or misleading claims could arise

No spontaneous mathematical mistake by another model was observed or documented. The controlled boundary omission demonstrates a concrete failure mode: a lower objective can be misleading if the model leaves out relevant history. The other omission tests demonstrate a subtler limitation: an apparently correct schedule cannot validate the whole formulation.

The generated parameters are illustrative, not independently established as realistic for a specific hospital. Calling them hospital-validated would be misleading. Similarly, an AI-generated checker can share assumptions with its solver. Using different checking logic and a separate lower-bound argument reduces this concern but does not eliminate the need for team review.

### What still requires human judgment

The manager must supply staffing requirements, qualifications, availability, relevant shift history, applicable work rules, acceptable overtime, and the intended notion of fairness. The team must inspect the formulation, reproduce the outputs, and decide what the evidence actually supports. This preparation does not claim that Sanath or Mahir has already performed that review.

### Optimization insights to discuss after review

The case supports the following learning conclusions, with detailed evidence and future practices in `INTERACTION_EVALUATION.md`: feasibility and optimality require different checks; horizon history must be explicit; fairness and preferences are distinct objectives; a passing roster can conceal a missing constraint; and technically correct GenAI output still needs review against the assignment's evidence requirements. These are supported analytical conclusions. The team should adapt them to its own experience after review.

1. Constraints define which schedules are feasible; an objective ranks only those schedules.
2. A globally optimal result can solve an incomplete model correctly and still be unacceptable for the real decision.
3. Horizon boundaries matter because shifts and rest extend across calendar days.
4. Preference satisfaction and equal night distribution are different objectives.
5. Feasibility checks, optimality arguments, and assumption validation are separate tasks.

## 7. Assumptions and limitations

- Six interchangeable nurses and four days omit skill mix, charge-nurse roles, patient acuity and longer-term fatigue.
- Coverage and availability are deterministic. Unexpected absences and demand changes require recourse or scenario-based modeling.
- Exact coverage excludes overstaffing; there is no float pool, agency staffing, overtime choice, or explicit understaffing penalty.
- Work-hour limits apply only to shifts starting in this four-day horizon. Rolling-week limits and complete historical workloads are omitted.
- Everyone is assumed off on day 5. Operational use would require the actual next-period plan.
- Penalties are synthetic and additive; interpersonal preferences and individual tradeoffs may not be captured by a 0–3 score.
- Night-count fairness ignores prior-period burden. A's prior night affects rest but is deliberately excluded from the in-horizon fairness count.
- Consecutive nights are allowed. A maximum-consecutive-night policy would be an additional rule, not something this model silently guarantees.
- The exact algorithm is practical for this tiny instance; coverage-state growth limits scalability.
- One AI-assisted session and deliberate stress tests provide a case study, not a benchmark or an error-rate estimate.

## 8. Sources and reproducibility

1. **Course assignment:** `../Project.pdf`, pages 1–2 (Option 2), page 3 (recording and rubric), page 4 (critical-evaluation expectations). The assignment calls for a real-world application, discussion of strengths and limitations, and identification of the GenAI model(s).
2. **Google OR-Tools, Employee Scheduling:** https://developers.google.com/optimization/scheduling/employee_scheduling : accessed October 6, 2026. Background example of binary nurse/shift assignments, coverage, one-shift limits, and preferences. The instance, penalties, algorithm and results here were developed for this project, not copied from that example.
3. **Google Operations Research API, Nurse Scheduling:** https://developers.google.com/optimization/service/scheduling/nurse_scheduling_example : accessed October 6, 2026. Background example representing coverage, work limits and rest. No external clinical standard is inferred from an optimization tutorial.
4. **Current Codex conversation and local outputs:** `solve.py`, `instance.json`, `results.json`, and `GENAI_RECORD.md`. These are the evidence for the project-specific computations. The exact results are reproducible by running `python3 solve.py` in this folder.

## 9. Presentation and submission

The presentation and recording are still upcoming; these materials are not completed submissions. The redesigned `presentation.html` has 11 slides organized around GenAI, human judgment and verification. Use arrow keys to navigate, F for full screen, and N for hidden notes. A print view is available through the browser's print command. Every slide was rendered and visually inspected at 1280×720, and the numerical content was checked against the saved results. `PRESENTATION_SCRIPT.md` contains matching notes and an 8-minute-30-second timing plan. Team-level interventions constructed for the narrative are marked internally for team review; they are not additional evidence of completed human review. Rehearse the actual duration.

Before recording, both members should run the solver, manually review the two rosters, inspect the boundary counterexample, and adapt the reflection to what they actually learned. Keep the recording below 10 minutes and have each member's camera on while that member presents, as required by the assignment. The recording and live presentation must be performed by the team; they are not generated by this package.

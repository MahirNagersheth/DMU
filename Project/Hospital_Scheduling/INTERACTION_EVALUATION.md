# Actual GenAI interaction and critical evaluation

**Tool:** Codex, identified in this session as based on GPT-6. The exact serving snapshot is unavailable.  
**Team:** Sanath Kumar and Mahir Nagersheth.  
**Scope:** One continuing AI-assisted conversation. No independent second-model trial or completed team audit is claimed.

## 1. Actual task and response evidence

The user supplied the nurse-scheduling topic and requested:

> Create this project for our topic

The assistant created the formulation, code, schedules and report. The following is an exact excerpt from the generated report's preference-optimum section:

> Only E's day-1 day shift costs a point.

**Evaluation:** The worked audit in `VERIFICATION.md` independently recomputes the sum from the supplied matrix. E contributes 1 + 0 + 0 = 1. Every other assigned shift has zero cost. This supports the assistant's arithmetic claim for this instance. It does not establish that the preference matrix is clinically appropriate.

Another exact excerpt from the same generated report is:

> On day 1, the only zero-penalty day nurses are A and B. A cannot work because of prior-night rest.

**Evaluation:** The matrix and shift history support both statements. Two day nurses are required, so at least one positive penalty is unavoidable. The returned roster attains 1. This is an especially useful explanation because it supplies a lower bound, rather than relying solely on solver output or confident prose.

## 2. An observed limitation in the actual interaction

After the first deck was produced, the user asked:

> Does the content provide what is expected by option 2 of the project?

The assistant answered:

> Mostly, but the GenAI evaluation needs stronger evidence before I would call it fully ready for Option 2.

**What was missing:** The initial deck contained optimization results and deliberately relaxed constraints, but did not show an actual prompt-response example or a detailed worked verification tied to a specific response. It also did not sufficiently separate documented case conclusions from the students' own learning. The user had to request this revision.

**Why this matters:** A mathematically useful answer can still omit evidence required by an assignment. The assistant had produced a polished project package before clearly identifying that gap. This is a documented limitation of its task completion and evidence presentation. It is not evidence that the original optimal roster was mathematically wrong.

The user's actual revision request was:

> Then fix it, create the prompt, document the verification and add the learning

**Correction made in this revision:** `PROMPT.md` now contains a copy-ready reproduction prompt. `VERIFICATION.md` documents coverage, costs, hours, availability, rest and optimality checks. This file connects specific actual response claims to that evidence. The deck and speaking notes now include the observed omission and supported learning conclusions.

## 3. What is and is not an observed AI error

| Evidence | Classification | Supported conclusion |
|---|---|---|
| Original penalty-1 schedule and explanation | Actual assistant-generated output, checked computationally and arithmetically | Correct under the stated assumptions |
| Initial absence of concrete interaction evidence in the deck | Observed task-completion limitation | Request an explicit evidence trail, not just polished results |
| Penalty-0 roster after removing boundary rest | Deliberate model experiment | Omitting history can invalidate an apparently better roster |
| Synthetic coverage, rest and preference parameters | Explicit modeling assumptions | Human validation is needed before operational use |
| Solver and checker both created in this session | Shared provenance | Different checking logic is useful but is not an independent human audit |

The new reproduction prompt was not retroactively used to obtain the original response. The earlier roster and proof are actual generated artifacts, not a newly invented transcript. The selected exact excerpts above are not a complete conversation export.

## 4. Learning supported by the evidence

### A feasible answer is not automatically an optimal answer

**Evidence:** The schedule satisfies the stated rules, while the first-day argument separately proves that penalty 0 is impossible under the complete model.  
**Learning:** Check constraints to establish feasibility; use a lower bound or an exact method to establish optimality.  
**Future practice:** Ask for both a constraint audit and an optimality justification.

### Relevant history is part of the scheduling problem

**Evidence:** Removing the prior-night condition gives A zero hours of rest, even though the visible four-day schedule passes the other checks.  
**Learning:** Calendar boundaries do not reset fatigue or eliminate obligations from the previous period.  
**Future practice:** Supply prior and next-period assignments explicitly and check actual timestamps.

### The objective determines what the model calls a good roster

**Evidence:** Preference-first scheduling gives P = 1 and F = 22. Fairness-first scheduling gives P = 14 and F = 12.  
**Learning:** Equal night counts and individual preference satisfaction are distinct goals, with a measurable tradeoff here.  
**Future practice:** Have the decision-maker choose the priority and explain the consequences.

### A correct output can conceal an incomplete formulation

**Evidence:** Removing internal rest or availability leaves the selected optimum unchanged in this instance.  
**Learning:** One passing schedule does not prove that all necessary constraints are present.  
**Future practice:** Inspect equations and test adverse cases, as well as checking the returned roster.

### GenAI's task completion needs its own review

**Evidence:** The first deck emphasized the solved model but needed revision to document actual interaction evidence for Option 2.  
**Learning:** Technical correctness and satisfying the communication requirements are different checks.  
**Future practice:** Map the final output to the rubric and retain the prompt, response and verification trail.

These are conclusions justified by the case. They are not claims about what Sanath or Mahir personally learned before reading and reviewing the material. The team should adapt the reflection after its own review.

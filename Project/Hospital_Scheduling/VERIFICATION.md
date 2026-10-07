# Documented verification of the GenAI output

Audit performed by the assistant in this revision using `verify_review.py`, which reads the saved instance and rosters and does not import the solver or its checker. All calculations below are reproducible. This is an AI-assisted worked audit, not an attestation that either team member has independently reviewed the work.

Run `python3 verify_review.py` to reproduce this document and its assertions. Times use labeled days rather than real calendar dates. All results apply to the synthetic assumptions in the report.

## Preference-first roster

### Coverage of all eight shifts

| Day | Shift | Nurses | Actual | Required |
|---|---|---|---:|---:|
| 1 | D | B, E | 2 | 2 |
| 1 | N | C, D | 2 | 2 |
| 2 | D | A, B | 2 | 2 |
| 2 | N | C, F | 2 | 2 |
| 3 | D | B, E | 2 | 2 |
| 3 | N | C, D | 2 | 2 |
| 4 | D | A, E | 2 | 2 |
| 4 | N | D, F | 2 | 2 |

### Hours and penalty arithmetic

| Nurse | Pattern | Hours | Assigned-shift costs | Penalty | Nights |
|---|---|---:|---|---:|---:|
| A | ODOD | 24 | 0 + 0 | 0 | 0 |
| B | DDDO | 36 | 0 + 0 + 0 | 0 | 0 |
| C | NNNO | 36 | 0 + 0 + 0 | 0 | 3 |
| D | NONN | 36 | 0 + 0 + 0 | 0 | 3 |
| E | DODD | 36 | 1 + 0 + 0 | 1 | 0 |
| F | ONON | 24 | 0 + 0 | 0 | 2 |

Total hours = 192. Preference penalty P = 1. Night fairness F = 0² + 0² + 3² + 3² + 0² + 2² = 22.

### Every consecutive rest interval

| Nurse | Previous shift ends | Next shift starts | Rest hours | Result |
|---|---|---|---:|---|
| A | Day 1 07:00 | Day 2 07:00 | 24 | Pass |
| A | Day 2 19:00 | Day 4 07:00 | 36 | Pass |
| B | Day 1 19:00 | Day 2 07:00 | 12 | Pass |
| B | Day 2 19:00 | Day 3 07:00 | 12 | Pass |
| C | Day 2 07:00 | Day 2 19:00 | 12 | Pass |
| C | Day 3 07:00 | Day 3 19:00 | 12 | Pass |
| D | Day 2 07:00 | Day 3 19:00 | 36 | Pass |
| D | Day 4 07:00 | Day 4 19:00 | 12 | Pass |
| E | Day 1 19:00 | Day 3 07:00 | 36 | Pass |
| E | Day 3 19:00 | Day 4 07:00 | 12 | Pass |
| F | Day 3 07:00 | Day 4 19:00 | 36 | Pass |

A's first interval includes the previous night, ending on day 1 at 07:00. There are no later scheduled shifts to check after the horizon; everyone is assumed off on day 5. Other nurses are assumed sufficiently rested before their first assignment.

### Remaining constraints

- Each four-character pattern contains exactly one of O, D, or N per day, establishing the one-shift-per-day rule and binary assignment structure.
- Every nurse works either two or three 12-hour shifts, within 24 and 36 hours.
- E has O on day 2. F does not have D on day 4. All stated availability restrictions pass.
- A does not have D on day 1, so the prior-night boundary condition passes.

## Fairness-first roster

### Coverage of all eight shifts

| Day | Shift | Nurses | Actual | Required |
|---|---|---|---:|---:|
| 1 | D | B, F | 2 | 2 |
| 1 | N | A, E | 2 | 2 |
| 2 | D | B, F | 2 | 2 |
| 2 | N | C, D | 2 | 2 |
| 3 | D | A, E | 2 | 2 |
| 3 | N | B, C | 2 | 2 |
| 4 | D | A, E | 2 | 2 |
| 4 | N | D, F | 2 | 2 |

### Hours and penalty arithmetic

| Nurse | Pattern | Hours | Assigned-shift costs | Penalty | Nights |
|---|---|---:|---|---:|---:|
| A | NODD | 36 | 3 + 1 + 0 | 4 | 1 |
| B | DDNO | 36 | 0 + 0 + 3 | 3 | 1 |
| C | ONNO | 24 | 0 + 0 | 0 | 2 |
| D | ONON | 24 | 1 + 0 | 1 | 2 |
| E | NODD | 36 | 2 + 0 + 0 | 2 | 1 |
| F | DDON | 36 | 2 + 2 + 0 | 4 | 1 |

Total hours = 192. Preference penalty P = 14. Night fairness F = 1² + 1² + 2² + 2² + 1² + 1² = 12.

### Every consecutive rest interval

| Nurse | Previous shift ends | Next shift starts | Rest hours | Result |
|---|---|---|---:|---|
| A | Day 1 07:00 | Day 1 19:00 | 12 | Pass |
| A | Day 2 07:00 | Day 3 07:00 | 24 | Pass |
| A | Day 3 19:00 | Day 4 07:00 | 12 | Pass |
| B | Day 1 19:00 | Day 2 07:00 | 12 | Pass |
| B | Day 2 19:00 | Day 3 19:00 | 24 | Pass |
| C | Day 3 07:00 | Day 3 19:00 | 12 | Pass |
| D | Day 3 07:00 | Day 4 19:00 | 36 | Pass |
| E | Day 2 07:00 | Day 3 07:00 | 24 | Pass |
| E | Day 3 19:00 | Day 4 07:00 | 12 | Pass |
| F | Day 1 19:00 | Day 2 07:00 | 12 | Pass |
| F | Day 2 19:00 | Day 4 19:00 | 48 | Pass |

A's first interval includes the previous night, ending on day 1 at 07:00. There are no later scheduled shifts to check after the horizon; everyone is assumed off on day 5. Other nurses are assumed sufficiently rested before their first assignment.

### Remaining constraints

- Each four-character pattern contains exactly one of O, D, or N per day, establishing the one-shift-per-day rule and binary assignment structure.
- Every nurse works either two or three 12-hour shifts, within 24 and 36 hours.
- E has O on day 2. F does not have D on day 4. All stated availability restrictions pass.
- A does not have D on day 1, so the prior-night boundary condition passes.

## Optimality checks

**Preference objective:** The day-1 day penalties for A through F are 0, 0, 3, 3, 1, 2. A is forbidden by prior-night rest. The cheapest available pair therefore costs 0 + 1 = 1. All remaining penalties are nonnegative. The feasible roster attains this lower bound, so P = 1 is globally optimal.

**Fairness objective:** Eight night assignments distributed among six nurses are most evenly split as 2, 2, 1, 1, 1, 1. The square sum is 4 + 4 + 1 + 1 + 1 + 1 = 12. Moving one assignment from a count a to b when a >= b + 2 decreases the square sum by 2(a-b-1), so a less even distribution cannot improve the bound. The fairness roster attains 12. Its penalty of 14 is directly recomputed above. Minimality of 14 among all fairness-optimal rosters comes from the exact dynamic program, not from the feasibility audit alone.

## Deliberate boundary omission

The relaxed roster gives A the pattern DDOD. A's prior shift ends on day 1 at 07:00, and its next shift starts on day 1 at 07:00. Rest = 07:00 minus 07:00 = 0 hours, below the required 12. The new audit returns exactly one violation: A's boundary rest. Its preference penalty recomputes to 0. This is a deliberately constructed model variant, not an observed spontaneous GenAI error.

## Audit conclusion and limits

Both full-model rosters pass every stated scheduling constraint. Their recomputed scores agree with the saved solver output. The controlled boundary-omission roster fails the intended rest requirement. No mathematical error was found in the two complete-model rosters.

These checks establish facts about this instance. They do not validate clinical staffing needs, the preference inputs, or omitted real-world requirements. The new audit uses different code from the original checker, but shares the same AI-assisted provenance and input assumptions. Sanath and Mahir should review the arithmetic and assumptions themselves before describing this as their own verification.

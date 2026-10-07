"""Recompute a documented audit without importing the solver or its checker."""
import json
from pathlib import Path

BASE = Path(__file__).resolve().parent
data = json.loads((BASE / 'instance.json').read_text())
results = json.loads((BASE / 'results.json').read_text())
nurses = data['nurses']
unavailable = {tuple(x) for x in data['unavailable_zero_based']}

def stamp(t):
    day, hour = divmod(t, 24)
    return f'Day {day+1} {hour:02d}:00'

def review(key, demand):
    roster = results[key]['schedule']
    coverage, rows, errors = [], [], []
    for d in range(4):
        for s in 'DN':
            assigned = [n for n in nurses if roster[n][d] == s]
            expected = demand[2*d+'DN'.index(s)]
            coverage.append([d+1, s, ', '.join(assigned), len(assigned), expected])
            if len(assigned) != expected:
                errors.append(f'Day {d+1} {s}: coverage mismatch')
    for i, n in enumerate(nurses):
        pattern = roster[n]
        assert len(pattern)==4 and set(pattern) <= set('ODN')
        work = [(d,s) for d,s in enumerate(pattern) if s!='O']
        costs = [data['costs'][i][d]['DN'.index(s)] for d,s in work]
        hours = 12*len(work)
        if not 24 <= hours <= 36:
            errors.append(n+': hours outside limits')
        violations = [(d+1,s) for d,s in work if (i,d,'DN'.index(s)) in unavailable]
        if violations:
            errors.append(n+': unavailable assignment')
        intervals = [(-5,7)] if n in data['prior_night_nurses'] else []
        intervals += [(24*d+(7 if s=='D' else 19),24*d+(19 if s=='D' else 31)) for d,s in work]
        gaps = [(stamp(a[1]),stamp(b[0]),b[0]-a[1]) for a,b in zip(intervals,intervals[1:])]
        if any(g[2]<12 for g in gaps):
            errors.append(n+': rest below 12 hours')
        rows.append(dict(nurse=n, pattern=pattern, hours=hours, costs=costs, penalty=sum(costs),
                         nights=pattern.count('N'), gaps=gaps, availability_pass=not violations))
    return dict(coverage=coverage, nurses=rows, penalty=sum(x['penalty'] for x in rows),
                fairness=sum(x['nights']**2 for x in rows), hours=sum(x['hours'] for x in rows),errors=errors)

audits = {k:review(k,[2]*8) for k in ['preference_optimum','fairness_optimum','omit_boundary_rest']}
for key, p, f in [('preference_optimum',1,22),('fairness_optimum',14,12)]:
    a=audits[key]
    assert not a['errors'] and a['penalty']==p and a['fairness']==f and a['hours']==192
    original=results[key]['audit_against_full_rules']
    assert a['penalty']==original['preference_cost'] and a['fairness']==original['night_square_sum']
assert audits['omit_boundary_rest']['penalty']==0
assert audits['omit_boundary_rest']['errors']==['A: rest below 12 hours']

out = ['# Documented verification of the GenAI output', '',
       'Audit performed by the assistant in this revision using `verify_review.py`, which reads the saved instance and rosters and does not import the solver or its checker. All calculations below are reproducible. This is an AI-assisted worked audit, not an attestation that either team member has independently reviewed the work.', '',
       'Run `python3 verify_review.py` to reproduce this document and its assertions. Times use labeled days rather than real calendar dates. All results apply to the synthetic assumptions in the report.', '']
for key, title in [('preference_optimum','Preference-first roster'),('fairness_optimum','Fairness-first roster')]:
    a=audits[key]
    out += ['## '+title, '', '### Coverage of all eight shifts', '', '| Day | Shift | Nurses | Actual | Required |', '|---|---|---|---:|---:|']
    out += ['| '+' | '.join(map(str,row))+' |' for row in a['coverage']]
    out += ['', '### Hours and penalty arithmetic', '', '| Nurse | Pattern | Hours | Assigned-shift costs | Penalty | Nights |', '|---|---|---:|---|---:|---:|']
    for row in a['nurses']:
        out.append(f"| {row['nurse']} | {row['pattern']} | {row['hours']} | {' + '.join(map(str,row['costs']))} | {row['penalty']} | {row['nights']} |")
    out += ['', f"Total hours = {a['hours']}. Preference penalty P = {a['penalty']}. Night fairness F = "+' + '.join(str(r['nights'])+'²' for r in a['nurses'])+f" = {a['fairness']}.", '',
            '### Every consecutive rest interval', '', '| Nurse | Previous shift ends | Next shift starts | Rest hours | Result |', '|---|---|---|---:|---|']
    for row in a['nurses']:
        for end,start,gap in row['gaps']:
            out.append(f"| {row['nurse']} | {end} | {start} | {gap} | {'Pass' if gap>=12 else 'Fail'} |")
    out += ['', 'A\'s first interval includes the previous night, ending on day 1 at 07:00. There are no later scheduled shifts to check after the horizon; everyone is assumed off on day 5. Other nurses are assumed sufficiently rested before their first assignment.', '',
            '### Remaining constraints', '',
            '- Each four-character pattern contains exactly one of O, D, or N per day, establishing the one-shift-per-day rule and binary assignment structure.',
            '- Every nurse works either two or three 12-hour shifts, within 24 and 36 hours.',
            '- E has O on day 2. F does not have D on day 4. All stated availability restrictions pass.',
            '- A does not have D on day 1, so the prior-night boundary condition passes.', '']
out += ['## Optimality checks', '',
        '**Preference objective:** The day-1 day penalties for A through F are 0, 0, 3, 3, 1, 2. A is forbidden by prior-night rest. The cheapest available pair therefore costs 0 + 1 = 1. All remaining penalties are nonnegative. The feasible roster attains this lower bound, so P = 1 is globally optimal.', '',
        '**Fairness objective:** Eight night assignments distributed among six nurses are most evenly split as 2, 2, 1, 1, 1, 1. The square sum is 4 + 4 + 1 + 1 + 1 + 1 = 12. Moving one assignment from a count a to b when a >= b + 2 decreases the square sum by 2(a-b-1), so a less even distribution cannot improve the bound. The fairness roster attains 12. Its penalty of 14 is directly recomputed above. Minimality of 14 among all fairness-optimal rosters comes from the exact dynamic program, not from the feasibility audit alone.', '',
        '## Deliberate boundary omission', '',
        'The relaxed roster gives A the pattern DDOD. A\'s prior shift ends on day 1 at 07:00, and its next shift starts on day 1 at 07:00. Rest = 07:00 minus 07:00 = 0 hours, below the required 12. The new audit returns exactly one violation: A\'s boundary rest. Its preference penalty recomputes to 0. This is a deliberately constructed model variant, not an observed spontaneous GenAI error.', '',
        '## Audit conclusion and limits', '',
        'Both full-model rosters pass every stated scheduling constraint. Their recomputed scores agree with the saved solver output. The controlled boundary-omission roster fails the intended rest requirement. No mathematical error was found in the two complete-model rosters.', '',
        'These checks establish facts about this instance. They do not validate clinical staffing needs, the preference inputs, or omitted real-world requirements. The new audit uses different code from the original checker, but shares the same AI-assisted provenance and input assumptions. Sanath and Mahir should review the arithmetic and assumptions themselves before describing this as their own verification.', '']
(BASE/'VERIFICATION.md').write_text('\n'.join(out))
(BASE/'verification_review.json').write_text(json.dumps(audits,indent=2)+'\n')
print('PASS: two rosters, 16 coverage checks, 12 workload and cost checks, all consecutive rest gaps, and the boundary-error counterexample. Scores: P=1/F=22 and P=14/F=12.')

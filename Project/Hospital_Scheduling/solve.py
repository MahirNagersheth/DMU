"""Exact nurse scheduling experiment. Python 3.9+, standard library only.

Run: python3 solve.py
Synthetic teaching case: none of these rules is a clinical/legal standard.
"""
import csv
import itertools
import json
from pathlib import Path

OUT = Path(__file__).resolve().parent
NURSES = list("ABCDEF")
DAYS = 4
# Costs by nurse, then day, then [day shift, night shift].
COSTS = [
    [[0, 3], [0, 3], [1, 3], [0, 3]],
    [[0, 3], [0, 3], [0, 3], [1, 3]],
    [[3, 0], [3, 0], [3, 0], [3, 1]],
    [[3, 0], [3, 1], [3, 0], [3, 0]],
    [[1, 2], [1, 2], [0, 2], [0, 2]],
    [[2, 0], [2, 0], [2, 1], [2, 0]],
]
UNAVAILABLE = {(4, 1, 0), (4, 1, 1), (5, 3, 0)}
PRIOR_NIGHT = {0}  # A works a night ending at 07:00 on day 1.


def patterns(n, rest=True, availability=True, max_shifts=3, boundary=True):
    for p in itertools.product("ODN", repeat=DAYS):
        if not 2 <= sum(v != "O" for v in p) <= max_shifts:
            continue
        if rest and any(p[d] == "N" and p[d+1] == "D" for d in range(DAYS-1)):
            continue
        if boundary and n in PRIOR_NIGHT and p[0] == "D":
            continue
        if availability and any(p[d] == "DN"[s] for nn, d, s in UNAVAILABLE if nn == n):
            continue
        counts = tuple(int(p[d] == "DN"[s]) for d in range(DAYS) for s in range(2))
        cost = sum(COSTS[n][d]["DN".index(v)] for d, v in enumerate(p) if v != "O")
        yield p, counts, cost, p.count("N") ** 2


def solve(objective="preference", rest=True, availability=True, max_shifts=3,
          boundary=True, demand=None):
    demand = tuple(demand or [2]*8)
    # For fixed nurse index and cumulative coverage, future possibilities are identical.
    # Retaining only the lowest lexicographic cost therefore preserves an optimum.
    states = {(0,)*8: ((0, 0), [])}
    sizes = [1]
    for n in range(6):
        nxt = {}
        for p, counts, pref, fairness in patterns(n, rest, availability, max_shifts, boundary):
            contribution = (pref, fairness) if objective == "preference" else (fairness, pref)
            for used, (score, schedule) in states.items():
                new = tuple(a+b for a, b in zip(used, counts))
                if any(a>b for a, b in zip(new, demand)):
                    continue
                total = tuple(a+b for a,b in zip(score, contribution))
                if new not in nxt or total < nxt[new][0]:
                    nxt[new] = (total, schedule + ["".join(p)])
        states = nxt
        sizes.append(len(states))
    if demand not in states:
        return {"feasible": False, "state_counts": sizes}
    score, schedule = states[demand]
    audit = validate(schedule, demand=demand, max_shifts=max_shifts)
    return {"feasible": True, "objective": objective, "score": score,
            "schedule": dict(zip(NURSES, schedule)), "audit_against_full_rules": audit,
            "state_counts": sizes}


def validate(schedule, demand=None, max_shifts=3):
    """Separately compute coverage and real timestamp gaps; no use of patterns()."""
    demand = list(demand or [2]*8)
    errors = []
    coverage = [sum(row[d] == s for row in schedule) for d in range(4) for s in "DN"]
    if coverage != demand:
        errors.append("Coverage differs from required exact staffing")
    hours, nights = [], []
    pref = 0
    gaps = {}
    for n, row in enumerate(schedule):
        if len(row) != 4 or any(v not in "ODN" for v in row):
            errors.append(f"{NURSES[n]}: invalid pattern")
            continue
        hours.append(12*sum(v != "O" for v in row))
        nights.append(row.count("N"))
        if not 24 <= hours[-1] <= 12*max_shifts:
            errors.append(f"{NURSES[n]}: hours {hours[-1]} outside bounds")
        intervals = [(-5, 7)] if n in PRIOR_NIGHT else []
        for d, s in enumerate(row):
            if s == "O":
                continue
            k = "DN".index(s)
            pref += COSTS[n][d][k]
            if (n, d, k) in UNAVAILABLE:
                errors.append(f"{NURSES[n]}: unavailable on day {d+1} {s}")
            start = d*24 + (7 if s == "D" else 19)
            intervals.append((start, start+12))
        nurse_gaps = [b[0]-a[1] for a,b in zip(intervals, intervals[1:])]
        gaps[NURSES[n]] = nurse_gaps
        if any(g < 12 for g in nurse_gaps):
            errors.append(f"{NURSES[n]}: rest below 12 hours ({nurse_gaps})")
    return {"valid": not errors, "violations": errors, "coverage": coverage,
            "hours": dict(zip(NURSES, hours)), "night_counts": dict(zip(NURSES, nights)),
            "preference_cost": pref, "night_square_sum": sum(x*x for x in nights),
            "rest_gaps_hours": gaps}


def main():
    data = {"nurses": NURSES, "days": DAYS, "shift_hours": 12,
            "minimum_rest_hours": 12, "minimum_shifts": 2, "maximum_shifts": 3,
            "demand": [2]*8, "costs": COSTS,
            "unavailable_zero_based": sorted(UNAVAILABLE), "prior_night_nurses": ["A"]}
    (OUT/"instance.json").write_text(json.dumps(data, indent=2)+"\n")
    results = {}
    scenarios = {
        "preference_optimum": {}, "fairness_optimum": {"objective": "fairness"},
        "omit_internal_rest": {"rest": False},
        "omit_boundary_rest": {"boundary": False},
        "omit_availability": {"availability": False},
        "max_24_hours": {"max_shifts": 2},
        "extra_nurse_day2_night": {"demand": [2,2,2,3,2,2,2,2]},
    }
    for label, args in scenarios.items():
        results[label] = solve(**args)
        r = results[label]
        print(label, r.get("score", "INFEASIBLE"), r.get("schedule", ""), flush=True)
    assert results["preference_optimum"]["audit_against_full_rules"]["valid"]
    assert results["fairness_optimum"]["audit_against_full_rules"]["valid"]
    assert not results["max_24_hours"]["feasible"]
    # Mutate a verified solution to ensure the independent checker rejects violations.
    p = list(results["preference_optimum"]["schedule"].values())
    changed = p.copy(); changed[0] = "D" + p[0][1:]
    assert any("rest below" in e for e in validate(changed)["violations"])
    changed = p.copy(); changed[4] = p[4][0] + "D" + p[4][2:]
    assert any("unavailable" in e for e in validate(changed)["violations"])
    changed = p.copy(); changed[1] = "DDDD"
    assert any("hours" in e for e in validate(changed)["violations"])
    changed = p.copy(); changed[2] = "NNDO"
    assert any("rest below" in e for e in validate(changed)["violations"])
    (OUT/"results.json").write_text(json.dumps(results, indent=2)+"\n")
    for key in ["preference_optimum", "fairness_optimum"]:
        r = results[key]; audit = r["audit_against_full_rules"]
        with (OUT/(key+".csv")).open("w", newline="") as f:
            w = csv.writer(f); w.writerow(["Nurse", "Day 1", "Day 2", "Day 3", "Day 4", "Hours", "Nights"])
            for n, p in r["schedule"].items():
                w.writerow([n, *p, audit["hours"][n], audit["night_counts"][n]])
    print("All baseline validations and four mutation checks passed.")


if __name__ == "__main__":
    main()

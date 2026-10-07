"""Build an offline HTML presentation from verified experiment results."""
import html
import json
from pathlib import Path

BASE = Path(__file__).resolve().parent
R = json.loads((BASE / "results.json").read_text())

def roster(key):
    r = R[key]
    audit = r["audit_against_full_rules"]
    rows = []
    for n, pattern in r["schedule"].items():
        shifts = ''.join(f'<td class="shift {v}">{v}</td>' for v in pattern)
        rows.append(f'<tr><th scope="row">{n}</th>{shifts}<td>{audit["hours"][n]}</td><td>{audit["night_counts"][n]}</td></tr>')
    return '<table class="roster"><thead><tr><th>Nurse</th><th>Day 1</th><th>Day 2</th><th>Day 3</th><th>Day 4</th><th>Hours</th><th>Nights</th></tr></thead><tbody>'+''.join(rows)+'</tbody></table>'

slides = [
    ("Hospital nurse scheduling", "Can GenAI build a<br>trustworthy nurse schedule?", '''
        <p class="lead">A verified optimization case study</p>
        <p class="authors">Sanath Kumar · Mahir Nagersheth</p>
        <p class="subtle">95-760 · Option 2: GenAI and Optimization<br>October 6, 2026</p>
        ''', 'Course assignment, Project.pdf, pp. 1–4. This session: Codex, identified as GPT-6; exact serving snapshot unavailable.'),
    ("The decision", "Cover every shift within the rules", '''
        <div class="split"><div><p class="big">6 nurses<br>4 days<br>2 shifts per day</p><p>Decision-maker: a hospital unit’s nurse manager.</p></div>
        <div><table><tr><th>Coverage</th><td>Exactly 2 per shift</td></tr><tr><th>Hours</th><td>24–36 per nurse</td></tr><tr><th>Rest</th><td>At least 12 hours</td></tr><tr><th>Shift times</th><td>D: 07:00–19:00<br>N: 19:00–07:00</td></tr></table></div></div>
        <p class="footnote">Synthetic teaching case. These numbers are assumptions, not clinical or legal standards.</p>
        ''', 'Project-specific assumptions: REPORT.md §2; instance.json. Background: https://developers.google.com/optimization/scheduling/employee_scheduling and https://developers.google.com/optimization/service/scheduling/nurse_scheduling_example (accessed October 6, 2026).'),
    ("Formulation", "Make every scheduling rule explicit", '''
        <p class="formula">x<sub>i,d,s</sub> ∈ {0,1} &nbsp; · &nbsp; 48 assignment decisions</p>
        <div class="split"><div><h3>Coverage and workload</h3><ul><li>Exactly two nurses per shift</li><li>At most one shift per day</li><li>Two or three shifts per nurse</li></ul></div>
        <div><h3>Availability and rest</h3><ul><li>E off day 2; F cannot work 4D</li><li>No night → next-day day shift</li><li>A’s prior night blocks day 1 D</li></ul></div></div>
        <p class="footnote">Minimum rest: 12 hours. All nurses are assumed off on day 5. Full equations are in the report.</p>
        ''', 'REPORT.md §3; solve.py. Night 0 ends at 07:00 on day 1. Workload counts shifts starting in the four-day horizon.'),
    ("Preference-first solution", "All shifts covered for one penalty point", roster("preference_optimum") + '''
        <p class="table-caption">D = day · N = night · O = off &nbsp; | &nbsp; Penalty = <strong>1</strong> · Scheduled hours = <strong>192</strong></p>
        <p class="footnote">Minimize total preference penalty; break ties using the sum of squared night counts.</p>
        ''', 'results.json: preference_optimum; REPORT.md §4. Synthetic preferences are on a 0–3 penalty scale.'),
    ("Verification", "Feasibility and optimality need different checks", '''
        <table class="checks"><tr><th>Coverage</th><td>Two nurses on each of eight shifts</td></tr><tr><th>Hours and availability</th><td>24–36 hours each; all restrictions satisfied</td></tr><tr><th>Rest</th><td>Timestamp audit: every checked gap ≥ 12 hours</td></tr></table>
        <h3 class="spaced">Why penalty 1 is optimal</h3><p>Only A and B have zero cost for day 1 D.<br>A is blocked by prior-night rest. A positive cost is unavoidable.<br>The roster achieves 1, so the lower bound is attained.</p>
        ''', 'results.json: preference_optimum.audit_against_full_rules; complete costs in instance.json; arithmetic proof in REPORT.md §4. Checker and solver were both AI-assisted.'),
    ("Competing objective", "Equal nights cost more preference points", roster("fairness_optimum") + '''
        <p class="table-caption">Night-count range: <strong>3 → 1</strong> &nbsp; | &nbsp; Preference penalty: <strong>1 → 14</strong></p>
        <p class="footnote">Minimize Σ nights² first: 22 → 12. Equal counts may conflict with nurses’ preferences.</p>
        ''', 'results.json: fairness_optimum and preference_optimum; REPORT.md §§3–4. Eight nights across six nurses attain the sum-of-squares lower bound at counts 2,2,1,1,1,1.'),
    ("Controlled error test", "A better score can hide zero rest", '''
        <p class="lead">Deliberately remove the prior-night boundary constraint.</p>
        <table><tr><th>Preference penalty</th><td>1 → <strong>0</strong></td></tr><tr><th>A’s prior night ends</th><td>Day 1, 07:00</td></tr><tr><th>A’s assigned day shift starts</th><td>Day 1, 07:00</td></tr><tr><th>Rest between shifts</th><td class="warning"><strong>0 hours: invalid</strong></td></tr></table>
        <p class="footnote">This is an intentional model ablation, not an observed spontaneous error by another AI model.</p>
        ''', 'results.json: omit_boundary_rest; solve.py: scenario definition and timestamp checker; REPORT.md §5.'),
    ("Observed GenAI limitation", "The first draft omitted key evidence", '''
        <h3>Actual follow-up from the user</h3><p>“Does the content provide what is expected by option 2<br>of the project?”</p>
        <h3 class="spaced">What the review found</h3><p>The deck showed optimization results, but lacked a concrete<br>prompt-response example and detailed verification evidence.</p>
        <h3 class="spaced">What changed</h3><p>A reproduction prompt, worked audit and explicit learning<br>now connect the claims to evidence.</p>
        <p class="footnote">Observed task-completion gap. No mathematical error was found in the complete-model rosters.</p>
        ''', 'Actual conversation excerpts and critique: INTERACTION_EVALUATION.md §§1–3. Original deck and assistant response preceded this revision.'),
    ("GenAI evaluation", "Check specific claims against the data", '''
        <h3>Actual generated response</h3><p>“Only E's day-1 day shift costs a point.”</p>
        <h3 class="spaced">Worked verification</h3><p>E: 1 + 0 + 0 = 1. All other assigned costs are zero.<br>Coverage, hours, availability and timestamp checks also pass.</p>
        <h3 class="spaced">What the explanation did well</h3><p>The first-day lower bound proves optimality.<br>A good score alone would not establish that result.</p>
        <p class="footnote">One Codex / GPT-6 session. Audit is AI-assisted; team review and hospital validation are not claimed.</p>
        ''', 'Exact excerpt: REPORT.md §4. Verification: VERIFICATION.md and verify_review.py. Provenance: INTERACTION_EVALUATION.md. Exact serving snapshot unavailable.'),
    ("Human judgment", "The manager must define what “good” means", '''
        <h3>Choose the policy</h3><p>Individual preferences or equal night assignments?<br>Minimum coverage or exact staffing? Which history counts?</p>
        <h3 class="spaced">Validate the missing context</h3><p>Skill mix · patient acuity · absences · rolling work limits<br>Prior night burden · consecutive-night policy</p>
        <p class="lead closing-line">A mathematically valid roster depends on valid assumptions.</p>
        ''', 'REPORT.md §§6–7: project assumptions and limitations. These are modeling considerations, not clinical recommendations.'),
    ("Takeaway", "Trust the checks, not just the explanation", '''
        <p class="closing">GenAI can help build the model.<br>Exact computation checks the solution.<br>People must validate the decision.</p>
        <p>Our case: a penalty-1 valid roster, a visible fairness tradeoff,<br>and a penalty-0 boundary error caught by timestamp checks.</p>
        <p class="sources">Sources: course Project.pdf; Google OR-Tools, Employee Scheduling; Google Operations Research API, Nurse Scheduling.<br>Full references, formulation and reproducible results are included in the project report.</p>
        ''', 'Project.pdf pp.1–4; REPORT.md; results.json; https://developers.google.com/optimization/scheduling/employee_scheduling ; https://developers.google.com/optimization/service/scheduling/nurse_scheduling_example .'),
]

slides.insert(2, ("Prompt and interaction", "Record what was actually asked", '''
    <h3>Actual request after supplying the topic</h3><p>“Create this project for our topic”</p>
    <h3 class="spaced">Reproduction prompt created in this revision</h3><p>Specify six nurses, four days, exact coverage, rest,<br>availability, shift history and the complete penalty matrix.<br>Request a model, a roster, an audit and an optimality proof.</p>
    <p class="lead">The full copy-ready prompt is included in PROMPT.md.</p>
    <p class="footnote">Prepared for reproduction. It is not presented as the original prompt or a fresh second-model trial.</p>
    ''', 'Original user request in this conversation; PROMPT.md; INTERACTION_EVALUATION.md. The original topic described hospital scheduling, coverage, work hours and rest.'))
slides.insert(-1, ("Learning from the case", "Three lessons change how to use GenAI", '''
    <table class="checks"><tr><th>Check two questions</th><td>Constraint checks establish feasibility.<br>A lower bound establishes optimality.</td></tr>
    <tr><th>Include shift history</th><td>The visible grid can hide zero rest.<br>Supply boundaries and check timestamps.</td></tr>
    <tr><th>Review the whole task</th><td>A correct model can miss required evidence.<br>Map claims and exhibits to the rubric.</td></tr></table>
    <p class="lead closing-line">Choose the objective deliberately: equal nights and<br>individual preferences produce different rosters.</p>
    <p class="footnote">Conclusions supported by the case. Personal reflections should follow the team’s own review.</p>
    ''', 'INTERACTION_EVALUATION.md §4; VERIFICATION.md; results.json. These are case-supported conclusions, not a claim of completed student review.'))

css = '''
*{box-sizing:border-box}html,body{margin:0;width:100%;height:100%;background:#172c32;font-family:Arial,Helvetica,sans-serif;color:#193d43}#frame{position:absolute;top:50%;left:50%;width:1280px;height:720px;transform-origin:center center}.slide{width:1280px;height:720px;background:#f6f4ee;padding:44px 64px 50px;position:absolute;display:none;overflow:hidden}.slide.active{display:block}.kicker{font-size:18px;letter-spacing:2px;text-transform:uppercase;color:#57746c;margin:0 0 19px}h1{font-size:48px;line-height:1.1;letter-spacing:-1.4px;margin:0 0 27px;font-weight:700}.slide:first-child h1{font-size:68px;line-height:1.08;margin-top:57px;letter-spacing:-2px}.lead{font-size:30px;line-height:1.4;margin:14px 0 24px}.authors{font-size:27px;margin-top:45px}.subtle{font-size:22px;color:#637675;line-height:1.6}p,li,td,th{font-size:24px;line-height:1.42}p{margin:13px 0}h3{font-size:32px;margin:5px 0 14px;line-height:1.2}.big{font-size:46px;line-height:1.38;margin-top:0;font-weight:700}.split{display:grid;grid-template-columns:1fr 1fr;gap:56px}.split ul{padding-left:25px;margin:0}.split li{margin-bottom:20px}.formula{font-size:31px;margin-bottom:35px}.footnote{font-size:19px;line-height:1.4;color:#586c68;position:absolute;bottom:55px;left:64px;right:64px}.page{position:absolute;bottom:22px;right:64px;font-size:16px;color:#617773}.brand{position:absolute;bottom:22px;left:64px;font-size:16px;color:#617773}table{width:100%;border-collapse:collapse}td,th{text-align:left;padding:13px 15px;border-bottom:1px solid #d5ddd5}th{font-weight:600}thead th{font-size:20px;color:#537169}table tr:first-child th{border-top:none}.roster th,.roster td{padding:11px 14px;text-align:center;font-size:26px}.roster thead th{font-size:20px}.roster th:first-child{text-align:left}.shift.D{color:#145d70;background:#e5efed}.shift.N{color:#644581;background:#ece7f0}.shift.O{color:#82918b}.table-caption{font-size:25px;margin-top:24px}.checks th{width:31%}.checks td,.checks th{font-size:23px}.spaced{margin-top:29px}.warning{color:#a74428}.experiments th,.experiments td{font-size:23px;padding:17px 12px}.closing-line{margin-top:44px}.closing{font-size:39px;line-height:1.48;margin:44px 0 34px;letter-spacing:-.6px}.sources{font-size:17px;color:#586c68;line-height:1.5;position:absolute;left:64px;right:64px;bottom:65px}#controls{position:fixed;bottom:12px;left:50%;transform:translateX(-50%);display:flex;gap:12px;align-items:center;background:#173c43;color:#fff;padding:8px 12px;border-radius:5px;font-size:14px}button{border:1px solid #67878a;background:transparent;color:#fff;padding:7px 13px;border-radius:3px;cursor:pointer;font:inherit}button:focus-visible{outline:3px solid #eed29a}button:disabled{opacity:.35;cursor:default}#hint{position:fixed;top:10px;right:14px;color:#e0e8df;font-size:12px}@media print{@page{size:13.333in 7.5in;margin:0}html,body{background:white;width:auto;height:auto}#frame{position:static;transform:none!important;width:1280px;height:auto}.slide{display:block!important;position:relative;break-after:page;page-break-after:always}.slide:last-child{break-after:auto}#controls,#hint{display:none}}
'''
parts = []
for i, (label, title, body, sources) in enumerate(slides):
    parts.append(f'<section class="slide {"active" if i==0 else ""}" aria-label="Slide {i+1}: {html.escape(label)}"><p class="kicker">{label}</p><h1>{title}</h1>{body}<span class="brand">GENAI × OPTIMIZATION</span><span class="page">{i+1:02d} / {len(slides):02d}</span><aside class="speaker-notes" hidden>[Sources]\n{html.escape(sources)}\n[/Sources]</aside></section>')
script = '''
const slides=[...document.querySelectorAll('.slide')];let current=0;const frame=document.querySelector('#frame');
function resize(){let s=Math.min(innerWidth/1280,(innerHeight-65)/720);frame.style.transform=`translate(-50%,-50%) scale(${s})`;}
function show(n){current=Math.max(0,Math.min(slides.length-1,n));slides.forEach((s,i)=>{s.classList.toggle('active',i===current);s.setAttribute('aria-hidden',i!==current)});document.querySelector('#counter').textContent=`${current+1} / ${slides.length}`;document.querySelector('#prev').disabled=current===0;document.querySelector('#next').disabled=current===slides.length-1;history.replaceState(null,'','#'+(current+1));}
document.querySelector('#prev').onclick=()=>show(current-1);document.querySelector('#next').onclick=()=>show(current+1);
document.addEventListener('keydown',e=>{if(['ArrowRight','ArrowDown','PageDown',' '].includes(e.key)){e.preventDefault();show(current+1)}if(['ArrowLeft','ArrowUp','PageUp'].includes(e.key)){e.preventDefault();show(current-1)}if(e.key==='Home')show(0);if(e.key==='End')show(slides.length-1);if(e.key.toLowerCase()==='f'){if(document.fullscreenElement)document.exitFullscreen();else document.documentElement.requestFullscreen().catch(()=>{})}});window.addEventListener('resize',resize);resize();show((parseInt(location.hash.slice(1),10)||1)-1);
'''
output = '<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>GenAI and Hospital Nurse Scheduling</title><style>'+css+'</style></head><body><main id="frame">'+''.join(parts)+'</main><div id="hint">Arrow keys to navigate · F for full screen</div><nav id="controls" aria-label="Slide navigation"><button id="prev" aria-label="Previous slide">← Previous</button><span id="counter" aria-live="polite"></span><button id="next" aria-label="Next slide">Next →</button></nav><script>'+script+'</script></body></html>'
(BASE/'presentation.html').write_text(output)
print(f'Created {len(slides)} slides.')

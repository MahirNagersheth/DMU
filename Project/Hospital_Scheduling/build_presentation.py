"""Maintain the directly editable offline HTML deck and its speaker notes."""
from pathlib import Path
import html
import json

BASE = Path(__file__).resolve().parent
R = json.loads((BASE / 'results.json').read_text())
DRAFT = '[DRAFT HUMAN INTERVENTION \u2014 TEAM MUST VERIFY/EDIT]'
slides = []

def badge(role):
    return f'<span class="badge {role.lower()}">{role}</span>'

def add(title, kicker, body, point, bullets, emphasis, transition, sources, seconds, speaker, draft=None, cls=''):
    slides.append(dict(title=title,kicker=kicker,body=body,point=point,bullets=bullets,emphasis=emphasis,
                       transition=transition,sources=sources,seconds=seconds,speaker=speaker,draft=draft,cls=cls))

def nights(key):
    ns = R[key]['audit_against_full_rules']['night_counts']
    return '<div class="night-counts" aria-label="Night assignments by nurse">'+''.join(
        f'<div><span>{n}</span><strong>{v}</strong></div>' for n,v in ns.items())+'</div>'

def roster():
    rows=[]
    for n,p in R['preference_optimum']['schedule'].items():
        cells=''.join(f'<td><span class="shift {s}{" highlight" if n=="E" and d==0 else ""}">{s}{"<sup>+1</sup>" if n=="E" and d==0 else ""}</span></td>' for d,s in enumerate(p))
        rows.append(f'<tr><th scope="row">{n}</th>{cells}</tr>')
    return '<table class="roster"><thead><tr><th>Nurse</th><th>Day 1</th><th>Day 2</th><th>Day 3</th><th>Day 4</th></tr></thead><tbody>'+''.join(rows)+'</tbody></table>'

add('Can GenAI build a<br>trustworthy<br>nurse schedule?', '95-760 / OPTION 2', '''
    <p class="cover-subtitle">A verified GenAI + optimization case study</p>
    <div class="cover-roles"><span>GENAI</span><i>→</i><span>HUMAN</span><i>→</i><span>VERIFIED</span></div>
    <div class="cover-authors">Sanath Kumar · Mahir Nagersheth<br><small>Decision Making Under Uncertainty · October 6, 2026</small></div>
    ''', 'Evaluate the assistance, not just the final roster.',
    ['Our case is a small, synthetic hospital scheduling decision.', 'The focus is how generation, human reasoning and verification work together.'],
    'A plausible answer is the start of evaluation, not the end.', 'Start with the nurse manager’s decision.',
    'Project.pdf pp. 1–4; REPORT.md. Tool: Codex, identified as GPT-6 in this session; exact serving snapshot unavailable. One continuing session, no second-model trial.',25,'Sanath',cls='cover')

add('A simple roster contains interacting rules.', '01 / THE DECISION', '''
    <p class="intro">A nurse manager must assign people to shifts, not just fill a grid.</p>
    <div class="stat-row"><div><strong>6</strong><span>nurses</span></div><div><strong>4</strong><span>days</span></div><div><strong>2</strong><span>shifts per day</span></div></div>
    <div class="shift-timeline"><div><b>DAY</b><span>07:00 → 19:00</span></div><div><b>NIGHT</b><span>19:00 → 07:00 next day</span></div></div>
    <div class="rules-row"><div><b>Exactly 2</b><span>nurses per shift</span></div><div><b>24–36 hours</b><span>per nurse</span></div><div><b>12+ hours</b><span>between shifts</span></div><div><b>Availability</b><span>restrictions apply</span></div></div>
    <p class="takeaway">The challenge: satisfy every rule at the same time.</p>
    ''', 'The scheduling problem is small enough to audit, but its constraints interact.',
    ['Sixteen assignments require 192 hours; each shift is 12 hours.', 'E cannot work day 2; F cannot work day-4 day shift.', 'All parameters are synthetic assumptions, not hospital staffing or legal standards.'],
    'The nurse manager supplies the real operational requirements.', 'The original request left many of these details unspecified.',
    'instance.json; REPORT.md §§1–2. Background: https://developers.google.com/optimization/scheduling/employee_scheduling and https://developers.google.com/optimization/service/scheduling/nurse_scheduling_example (accessed October 6, 2026).',40,'Sanath')

add('GenAI filled the gaps. We questioned them.', '02 / FROM REQUEST TO MODEL', '''
    <div class="quote-line"><span class="eyebrow">ORIGINAL REQUEST</span><q>Create this project for our topic</q></div>
    <div class="pipeline three">
      <article>'''+badge('GENAI')+'''<h3>Expand the task</h3><p>Generate a small instance,<br>penalties and scheduling rules.</p></article><div class="arrow">→</div>
      <article>'''+badge('HUMAN')+'''<h3>Question the inputs</h3><p>Do these assumptions<br>represent our decision?</p></article><div class="arrow">→</div>
      <article>'''+badge('VERIFIED')+'''<h3>Make rules explicit</h3><p>Turn each assumption into<br>a checkable condition.</p></article>
    </div>
    <p class="takeaway">Every inferred assumption becomes a modeling decision.</p>
    ''', 'GenAI supplied missing structure, but generated assumptions are choices, not facts.',
    ['The quote is the actual request, following the supplied nurse-scheduling topic.', 'The six-nurse instance and penalty matrix were generated in the AI-assisted workflow.', 'Exact staffing, workload bounds and preference penalties need deliberate interpretation.'],
    'The detailed PROMPT.md was prepared later for reproduction; it was not the original request.',
    'Once explicit, the rules can be translated into mathematical decisions.',
    'INTERACTION_EVALUATION.md §1; GENAI_RECORD.md; PROMPT.md; REPORT.md §2.',40,'Sanath',
    'Team questioning and acceptance of the generated assumptions is a constructed narrative intervention. Confirm or edit it before presenting; the files do not document that original team review.')

add('GenAI translated rules into 48 decisions.', '03 / WHAT GENAI DID WELL', '''
    <div class="model-grid"><div class="model-number">'''+badge('GENAI')+'''<strong>48</strong><p>binary assignments</p><div class="equation">x<sub>i,d,s</sub> ∈ {0,1}</div><small>6 nurses × 4 days × 2 shifts</small></div>
    <div class="rule-cards"><article><h3>Coverage</h3><p>Exactly two nurses<br>on every shift.</p></article><article><h3>Workload</h3><p>Two or three shifts each.<br>At most one per day.</p></article><article><h3>Availability</h3><p>E off day 2.<br>F cannot work day 4 D.</p></article><article><h3>Rest</h3><p>No night → next-day day.<br>Include prior-shift history.</p></article></div></div>
    <div class="human-line">'''+badge('HUMAN')+'''<p>Does each equation express the policy we intend?</p></div>
    ''', 'The assistant correctly translated the specified rules into a binary assignment model.',
    ['A one means assigned and a zero means not assigned.', 'The prior night blocks A from day 1 D; all nurses are assumed off on day 5.', 'Hard availability and rest constraints cannot be overridden by low penalty costs.'],
    'A correct equation still needs the right policy behind it.', 'Now inspect the schedule the tool-assisted workflow produced.',
    'REPORT.md §3; instance.json; solve.py.',40,'Sanath',
    'The team-level policy review question is drafted for team confirmation. Do not claim an earlier human review merely because the code passed.')

add('GenAI found a very good schedule.', '04 / THE GENERATED RESULT', '''
    <div class="result-grid"><div>'''+roster()+'''<div class="legend"><span>D = day</span><span>N = night</span><span>O = off</span><b>+1: the only positive cost</b></div></div>
    <div class="result-metrics">'''+badge('VERIFIED')+'''<strong class="hero-number">1</strong><p>total preference penalty</p><div class="mini-metrics"><div><b>8 / 8</b><span>shifts covered</span></div><div><b>192</b><span>scheduled hours</span></div></div></div></div>
    <div class="human-line">'''+badge('GENAI')+'''<span>Penalty = 1</span><span class="inline-arrow">→</span>'''+badge('HUMAN')+'''<p>But is 1 the best possible value?</p></div>
    ''', 'The returned roster is feasible and has a preference penalty of one.',
    ['E on day 1 D contributes the single point; every other assigned cost is zero.', 'A and F work 24 hours; the other four nurses work 36 hours.', 'Generation included executed exact search, not merely an untested text answer.'],
    'The quoted report claim is: “Only E\'s day-1 day shift costs a point.” The audit confirms it.',
    'Separate two questions: is the roster allowed, and can its score improve?',
    'results.json: preference_optimum; VERIFICATION.md: preference roster; REPORT.md §4; solve.py.',50,'Sanath',
    'The question attributed to the team about whether one is best is a proposed intervention, not a recorded original prompt.')

add('We did not trust “optimal” without a proof.', '05 / HUMAN CHALLENGE + VERIFICATION', '''
    <div class="proof-grid"><article class="proof-pass">'''+badge('VERIFIED')+'''<h3>Feasible ✓</h3><ul class="check-list"><li>Coverage</li><li>Hours</li><li>Availability</li><li>Rest</li></ul><p class="small">All modeled checks pass.</p></article>
    <article class="proof-question">'''+badge('HUMAN')+'''<h3>Ask for evidence</h3><blockquote>How do we know 1 is optimal, not just the best answer returned?</blockquote></article>
    <article class="proof-reason">'''+badge('VERIFIED')+'''<h3>Optimal ✓</h3><p>Only A and B cost zero on day 1 D.<br>A is blocked by prior-night rest.<br>Some positive cost is unavoidable.</p><div class="proof-equality"><div><b>1</b><span>lower bound</span></div><strong>=</strong><div><b>1</b><span>roster cost</span></div></div></article></div>
    <p class="takeaway">We learned: feasibility and optimality are different claims.</p>
    ''', 'Constraint checks establish feasibility; the lower-bound argument establishes optimality.',
    ['Day-1 day penalties are 0, 0, 3, 3, 1, 2 for A through F.', 'With A blocked, the cheapest available pair is B and E at cost 1. All other costs are nonnegative.', 'The assistant explained this lower bound well; the arithmetic can be checked directly.'],
    'The solver and both checkers were AI-assisted. Separate code and arithmetic are checks, not an independent human audit.',
    'An optimal answer still depends on which objective is being optimized.',
    'VERIFICATION.md: optimality checks; REPORT.md §4; instance.json; verify_review.py; results.json.',60,'Sanath',
    'The team question, proof-review narrative and first-person learning are drafted interventions. Confirm the team has reasoned through this argument before presenting them as personal experience.')

add('We changed the question.<br>The best schedule changed.', '06 / HUMAN CHOICE OF OBJECTIVE', '''
    <div class="comparison"><article><span class="eyebrow">PREFERENCE-FIRST</span><div class="compare-metrics"><div><strong>1</strong><span>penalty</span></div><div><strong>3</strong><span>night-count range</span></div></div>'''+nights('preference_optimum')+'''<p class="small">Nights concentrate on C, D and F.</p></article>
    <article><span class="eyebrow">FAIRNESS-FIRST</span><div class="compare-metrics"><div><strong>14</strong><span>penalty</span></div><div><strong>1</strong><span>night-count range</span></div></div>'''+nights('fairness_optimum')+'''<p class="small">Every nurse receives one or two nights.</p></article></div>
    <div class="human-line">'''+badge('HUMAN')+'''<p>Does low preference cost also mean a fair schedule?</p><span class="side-stat">Σ nights²: <b>22 → 12</b></span></div>
    <p class="takeaway">The optimizer does not decide what “fair” means. Humans do.</p>
    ''', 'Changing objective priority produces a measurable tradeoff.',
    ['Night counts are exactly 0,0,3,3,0,2 versus 1,1,2,2,1,1.', 'The fairness-first objective minimizes the sum of squared night counts, then preference cost; preference-first reverses that order.', 'Night equality costs 13 additional preference points. Some nurses prefer nights, so equal counts are not universally better.'],
    'This is a policy comparison on the same hard constraints, not evidence that one definition of fairness is universally correct.',
    'Changing an objective is deliberate; accidentally weakening a constraint is different.',
    'results.json: preference_optimum and fairness_optimum; REPORT.md §§3–4; VERIFICATION.md.',60,'Mahir',
    'The team noticing unequal nights, asking the fairness question and introducing the competing objective are constructed interventions. The two solved objectives are real; human authorship of their introduction is not documented.',cls='two-line')

add('A better score can come from a worse model.', '07 / INTENTIONAL STRESS TEST', '''
    <div class="stress-grid"><article>'''+badge('HUMAN')+'''<h3>Remove one rule</h3><p>Drop the prior-night<br>boundary constraint.</p><div class="stress-change"><span>Penalty</span><strong>1 → 0</strong></div><span class="eyebrow">OPTIMIZER RESULT</span></article>
    <article class="timestamps">'''+badge('VERIFIED')+'''<h3>Check the timestamps</h3><div><span>A’s prior night ends</span><b>07:00</b></div><div><span>A’s new day shift starts</span><b>07:00</b></div><p>Both on day 1.</p></article>
    <article class="invalid"><strong>0</strong><span>HOURS REST</span><b>INVALID</b><p>Required: at least 12 hours.</p></article></div>
    <p class="takeaway">Optimization will faithfully exploit a modeling mistake.</p>
    <p class="slide-caption">The score improved. The roster violated the intended rest rule.</p>
    ''', 'The intentionally weakened model produces a numerically better but invalid roster.',
    ['Only the prior-night boundary constraint is removed. The relaxed schedule assigns A DDOD.', 'The previous shift ends and the new shift starts at the same time: zero hours of rest.', 'This was deliberately introduced, not an observed spontaneous GenAI error.'],
    'The original full model included the boundary correctly. The experiment shows sensitivity to missing context, not a measured AI error rate.',
    'Separate these test results from what GenAI actually did well or left incomplete.',
    'results.json: omit_boundary_rest; VERIFICATION.md: deliberate boundary omission; solve.py and verify_review.py.',55,'Mahir',
    'Attributing initiation of the stress test to the team is a drafted intervention. The actual test was generated and executed in the AI-assisted workflow; team review/edit is required.')

score_rows = [
    ('Variables and core constraints','STRONG','Correct binary structure and stated rules'),
    ('Feasible roster and cost','STRONG','Coverage, hours, rest and penalty all check out'),
    ('Optimization explanation','STRONG','Clear lower bound and objective tradeoff'),
    ('Claim of optimality','VERIFY','Require a proof or checked exact-solver result'),
    ('Historical boundary context','VERIFY','Correct here; depends on complete history'),
    ('Definition of fairness','HUMAN','Multiple legitimate objectives'),
    ('Hospital realism','HUMAN','Synthetic inputs need operational context'),
    ('Complete assignment evidence','VERIFY','Initially incomplete; user requested revision'),
]
score_table='<table class="scorecard"><thead><tr><th>Task</th><th>Assessment</th><th>Evidence or limit</th></tr></thead><tbody>'+''.join(
    f'<tr><th scope="row">{task}</th><td><span class="rating {rating.lower()}">{rating}</span></td><td>{reason}</td></tr>' for task,rating,reason in score_rows)+'</tbody></table>'
add('GenAI was useful. Its claims still needed checks.', '08 / EVALUATION OF THE ACTUAL INTERACTION', score_table+'''
    <p class="slide-caption score-caption">Codex / GPT-6 · one session · no mathematical error found in the complete-model rosters</p>
    ''', 'Judge GenAI task by task using the actual evidence.',
    ['Strong: formulation, verified roster, penalty decomposition and lower-bound explanation.', 'Verify: optimality and boundary context. The controlled omission is not an actual original AI error.', 'Observed gap: the original deck lacked enough prompt-response and verification evidence; the user challenged its fit to Option 2.'],
    'These are qualitative assessments of this case, not benchmark scores. Checks were separately coded but AI-assisted, not external validation.',
    'The remaining decisions belong to people with the relevant context.',
    'INTERACTION_EVALUATION.md §§1–3; VERIFICATION.md; GENAI_RECORD.md; actual user request to revise the original deck.',60,'Mahir')

add('Three things humans still own.', '09 / WHERE JUDGMENT IS NECESSARY', '''
    <div class="ownership"><article><span class="ordinal">01</span><h3>Policy</h3><p class="question">What counts as good?</p><ul><li>Preferences vs fairness</li><li>Exact vs minimum staffing</li><li>Acceptable night burden</li></ul></article>
    <article><span class="ordinal">02</span><h3>Context</h3><p class="question">What does the model miss?</p><ul><li>Prior shifts and skill mix</li><li>Patient acuity and absences</li><li>Consecutive-night policies</li><li>Rolling work limits</li></ul></article>
    <article><span class="ordinal">03</span><h3>Judgment</h3><p class="question">Does the answer make sense?</p><p>Decide whether the objective<br>and constraints represent<br>the real decision.</p></article></div>
    <p class="takeaway">An optimal answer is only as useful as the decision it represents.</p>
    ''', 'Humans own policy, context and the interpretation of a solution.',
    ['Preference points are synthetic, not measured satisfaction or clinical outcomes.', 'Exact coverage excludes overstaffing; rolling hours and skill mix are outside this model.', 'A manager must decide which tradeoffs and additional constraints are appropriate.'],
    'No clinician, nurse manager, interview, patient data or deployment was involved. These are responsibilities for operational use, not reviews claimed to have occurred.',
    'Close with the workflow and the concrete lessons this case supports.',
    'REPORT.md §§2,6–7; INTERACTION_EVALUATION.md §4; Project.pdf Option 2 expectations.',40,'Mahir')

add('GenAI can build the model.<br>It cannot own the decision.', '10 / WHAT WE LEARNED', '''
    <div class="closing-flow"><b>GENERATE</b><i>→</i><b>CHALLENGE</b><i>→</i><b>VERIFY</b><i>→</i><b>JUDGE</b></div>
    <div class="closing-roles"><article>'''+badge('GENAI')+'''<p>Accelerates formulation<br>and reasoning</p></article><article>'''+badge('HUMAN')+'''<p>Defines objectives and<br>questions assumptions</p></article><article>'''+badge('VERIFIED')+'''<p>Computation and proofs<br>test the claims</p></article></div>
    <div class="closing-evidence"><div><strong>1</strong><span>optimal preference penalty</span></div><div><strong>1 → 14</strong><span>the cost of equalizing nights</span></div><div><strong>0 hours</strong><span>rest after one omitted rule</span></div></div>
    <p class="takeaway">Trust the checks, not just the explanation.</p>
    ''', 'The case supports a workflow of generation, challenge, verification and judgment.',
    ['We learned to distinguish a feasible roster from a proved optimum.', 'Changing the objective changes the meaning of best; missing history can invalidate the roster.', 'Actual GenAI assistance was useful but initially failed to communicate all required evidence.'],
    'Real-world validity still requires human judgment. Model correctness and operational adequacy are different questions.',
    'Invite questions about the objective tradeoff, the boundary test or the evidence trail.',
    'results.json; VERIFICATION.md; INTERACTION_EVALUATION.md; Project.pdf. Full source links are in REPORT.md.',40,'Both',
    'The first-person learning and team workflow narrative are drafted for confirmation. They summarize supported case conclusions but must be reviewed before being represented as personal experience.',cls='two-line')

CSS = r'''
:root{--cream:#f6f4ed;--teal:#173e43;--muted:#647875;--line:#ced8cf;--soft:#e8eee7;--human:#a97035;--humanbg:#f0e7d8;--verified:#3e6b59;--night:#dfe6e9;--rust:#a3422d}
*{box-sizing:border-box}html,body{margin:0;width:100%;height:100%;overflow:hidden;background:#142d32;color:var(--teal);font-family:Arial,Helvetica,sans-serif}button{font:inherit}#stage{position:absolute;left:50%;top:50%;width:1280px;height:720px;transform-origin:center center}.slide{display:none;position:absolute;inset:0;width:1280px;height:720px;background:var(--cream);padding:42px 64px 54px;overflow:hidden}.slide.active{display:block}.kicker{margin:0 0 17px;color:var(--muted);font-size:16px;font-weight:700;letter-spacing:2px}h1,h2,h3,p{margin:0}h2{font-size:48px;line-height:1.08;letter-spacing:-1.8px;font-weight:700}.body{margin-top:30px}.two-line .body{margin-top:22px}h3{font-size:30px;line-height:1.16;margin:14px 0}p,li{font-size:23px;line-height:1.42}.small{font-size:20px;color:var(--muted)}.intro{font-size:25px;color:var(--muted)}.eyebrow{display:block;font-size:16px;font-weight:700;letter-spacing:1.5px;color:var(--muted)}.badge{display:inline-block;padding:6px 11px;font-size:15px;line-height:1.2;font-weight:700;letter-spacing:1.2px;border-radius:3px}.badge.genai{background:var(--teal);color:var(--cream)}.badge.human{color:#80531f;background:var(--humanbg)}.badge.verified{color:#335d48;background:#dfeade}.takeaway{position:absolute;left:64px;right:64px;bottom:72px;padding-top:17px;border-top:1px solid var(--line);font-size:27px;font-weight:600;letter-spacing:-.4px}.slide-caption{font-size:17px;color:var(--muted);position:absolute;bottom:49px;left:64px;right:64px}.footer{position:absolute;left:64px;right:64px;bottom:23px;display:flex;justify-content:space-between;font-size:13px;letter-spacing:1px;color:var(--muted)}.footer .roles{word-spacing:8px}.cover h1{font-size:74px;line-height:1.04;letter-spacing:-3.2px;margin-top:48px}.cover .body{margin:0}.cover-subtitle{font-size:28px;margin-top:26px}.cover-roles{position:absolute;right:64px;top:226px;display:flex;flex-direction:column;align-items:center;gap:10px;font-size:19px;font-weight:700;letter-spacing:3px}.cover-roles i{font-style:normal;transform:rotate(90deg);font-size:25px;color:var(--human)}.cover-authors{position:absolute;left:64px;bottom:95px;font-size:25px;line-height:1.7}.cover-authors small{font-size:18px;color:var(--muted)}.stat-row{display:grid;grid-template-columns:repeat(3,1fr);margin:24px 0 28px}.stat-row>div{border-left:1px solid var(--line);padding-left:30px;display:flex;align-items:baseline;gap:20px}.stat-row>div:first-child{padding-left:0;border:0}.stat-row strong{font-size:91px;letter-spacing:-5px;line-height:1}.stat-row span{font-size:25px}.shift-timeline{display:grid;grid-template-columns:1fr 1fr;margin-bottom:29px;border:1px solid var(--line)}.shift-timeline>div{padding:15px 22px;display:flex;gap:24px;align-items:center;background:var(--soft)}.shift-timeline>div+div{background:var(--teal);color:var(--cream)}.shift-timeline b{font-size:16px;letter-spacing:2px}.shift-timeline span{font-size:24px}.rules-row{display:grid;grid-template-columns:repeat(4,1fr);gap:20px}.rules-row b,.rules-row span{display:block}.rules-row b{font-size:27px;margin-bottom:7px}.rules-row span{font-size:21px;color:var(--muted)}.quote-line{display:flex;align-items:center;gap:32px;padding:22px 0;border-top:1px solid var(--line);border-bottom:1px solid var(--line)}.quote-line q{font-size:30px;quotes:'“' '”'}.pipeline{display:grid;grid-template-columns:1fr 35px 1fr 35px 1fr;gap:12px;margin-top:48px}.pipeline article{padding-right:7px}.pipeline .arrow{font-size:32px;align-self:center;color:var(--muted)}.pipeline h3{margin:19px 0 16px}.pipeline p{font-size:22px}.model-grid{display:grid;grid-template-columns:320px 1fr;gap:35px}.model-number{padding-top:13px}.model-number>strong{display:block;font-size:126px;line-height:1.07;letter-spacing:-6px;margin-top:14px}.model-number>p{font-size:25px}.equation{font-size:29px;margin-top:25px}.equation sub{font-size:16px}.model-number small{display:block;font-size:17px;margin-top:12px;color:var(--muted)}.rule-cards{display:grid;grid-template-columns:1fr 1fr;gap:15px}.rule-cards article{padding:19px 23px;background:var(--soft);min-height:145px}.rule-cards h3{margin:0 0 12px}.rule-cards p{font-size:22px}.human-line{position:absolute;bottom:84px;left:64px;right:64px;padding-top:18px;border-top:1px solid var(--line);display:flex;align-items:center;gap:18px;font-size:23px}.human-line p{font-size:23px}.inline-arrow{font-size:29px;color:var(--muted)}.result-grid{display:grid;grid-template-columns:680px 1fr;gap:60px}.roster{width:100%;border-collapse:collapse;text-align:center;table-layout:fixed}.roster th{font-size:18px;font-weight:500;color:var(--muted);padding:5px 5px 11px}.roster thead th:first-child{width:84px}.roster tbody th{font-size:22px;color:var(--teal);font-weight:600;padding:0}.roster td{padding:4px 7px}.shift{display:block;height:43px;line-height:43px;background:#eeeee6;border-radius:3px;font-size:25px}.shift.D{background:#e0ebe2}.shift.N{background:var(--night);color:#254857}.shift.O{color:#8a968c}.shift.highlight{background:#eedab8;outline:2px solid #a97035;font-weight:700;position:relative}.shift sup{font-size:13px;margin-left:6px;vertical-align:top;line-height:30px}.legend{display:flex;gap:20px;margin-top:13px;font-size:16px;color:var(--muted)}.legend b{font-weight:500;color:#80531f}.result-metrics{padding-top:5px}.hero-number{display:block;font-size:122px;line-height:1.05;letter-spacing:-5px;margin-top:10px}.result-metrics>p{font-size:23px}.mini-metrics{display:flex;gap:32px;padding-top:22px;margin-top:24px;border-top:1px solid var(--line)}.mini-metrics b,.mini-metrics span{display:block}.mini-metrics b{font-size:37px;letter-spacing:-1px}.mini-metrics span{font-size:17px;color:var(--muted);margin-top:5px}.proof-grid{display:grid;grid-template-columns:232px 310px 1fr;gap:25px}.proof-grid article{padding:23px;background:var(--soft);height:356px}.proof-grid .proof-question{background:var(--humanbg)}.proof-grid .proof-reason{background:transparent;padding-right:0}.proof-grid h3{margin:17px 0}.check-list{list-style:none;padding:0;margin:16px 0}.check-list li{font-size:23px;padding:5px 0}.check-list li:before{content:'✓';margin-right:12px;color:var(--verified)}.proof-pass .small{font-size:17px}.proof-question blockquote{font-size:27px;line-height:1.3;margin:22px 0 0;letter-spacing:-.5px}.proof-reason p{font-size:22px}.proof-equality{display:flex;gap:32px;align-items:center;margin-top:16px}.proof-equality div{text-align:center}.proof-equality b{display:block;font-size:70px;line-height:1.1}.proof-equality span{font-size:18px}.proof-equality>strong{font-size:41px;color:var(--muted)}.comparison{display:grid;grid-template-columns:1fr 1fr;gap:48px}.comparison article{padding:18px 24px;background:var(--soft)}.comparison article+article{background:#e4ebe5}.compare-metrics{display:flex;gap:66px;margin-top:12px}.compare-metrics strong{display:block;font-size:76px;line-height:1.02;letter-spacing:-3px}.compare-metrics span{display:block;font-size:20px;color:var(--muted);margin-top:4px}.night-counts{display:flex;justify-content:space-between;border-top:1px solid #c2d0c6;margin-top:17px;padding-top:11px}.night-counts>div{text-align:center;min-width:35px}.night-counts span{display:block;font-size:15px;color:var(--muted)}.night-counts strong{display:block;font-size:25px;margin-top:3px}.comparison .small{font-size:17px;margin-top:10px}.comparison+.human-line{bottom:143px;border:0;padding:0;gap:12px}.comparison+.human-line p{font-size:22px}.side-stat{margin-left:auto;font-size:20px;color:var(--muted)}.stress-grid{display:grid;grid-template-columns:1fr 1.1fr .95fr;gap:30px;margin-top:42px}.stress-grid>article{padding:25px 24px;background:var(--soft);height:335px}.stress-grid h3{font-size:29px;margin:18px 0}.stress-grid p{font-size:22px}.stress-change{display:flex;align-items:baseline;gap:20px;margin:25px 0 14px}.stress-change span{font-size:20px}.stress-change strong{font-size:58px;letter-spacing:-2px}.stress-grid .eyebrow{font-size:13px}.timestamps>div{display:flex;justify-content:space-between;align-items:center;gap:12px;padding:15px 0;border-bottom:1px solid var(--line)}.timestamps>div span{font-size:20px;max-width:170px}.timestamps>div b{font-size:30px}.timestamps>p{font-size:17px;margin-top:17px;color:var(--muted)}.stress-grid .invalid{background:#f1e7dc;color:var(--rust);text-align:center;padding-top:24px}.invalid>strong{display:block;font-size:130px;line-height:1;letter-spacing:-5px}.invalid>span{display:block;font-size:19px;letter-spacing:3px;margin-top:9px}.invalid>b{display:block;font-size:31px;letter-spacing:1px;margin-top:22px}.invalid>p{font-size:17px;margin-top:17px}.stress-grid~.takeaway{bottom:84px}.scorecard{width:100%;border-collapse:collapse;margin-top:7px;table-layout:fixed}.scorecard thead th{font-size:16px;letter-spacing:1px;color:var(--muted);text-transform:uppercase;text-align:left;padding:0 12px 12px}.scorecard th:first-child{width:360px}.scorecard th:nth-child(2){width:170px}.scorecard tbody th,.scorecard td{border-top:1px solid var(--line);padding:13px 12px;text-align:left;font-size:21px;line-height:1.15}.scorecard tbody th{font-weight:500}.rating{font-size:13px;font-weight:700;letter-spacing:1px;display:inline-block;padding:6px 10px;border-radius:3px}.rating.strong{background:#dfeade;color:#335d48}.rating.verify{background:#e1e8e7;color:#35555a}.rating.human{background:var(--humanbg);color:#80531f}.score-caption{bottom:55px;font-size:16px}.ownership{display:grid;grid-template-columns:1fr 1fr 1fr;gap:30px;margin-top:43px}.ownership article{border-top:3px solid var(--teal);padding-top:21px}.ordinal{font-size:19px;color:var(--human);letter-spacing:1px}.ownership h3{font-size:37px;margin:12px 0 17px}.question{font-size:24px;font-weight:600;min-height:67px;max-width:300px}.ownership ul{list-style:none;padding:0;margin:10px 0}.ownership li{font-size:22px;line-height:1.4;margin-bottom:12px}.ownership article>p:last-child{font-size:23px}.closing-flow{display:flex;justify-content:space-between;align-items:center;padding:23px 0 26px;border-bottom:1px solid var(--line)}.closing-flow b{font-size:28px;letter-spacing:-.3px}.closing-flow i{font-size:28px;font-style:normal;color:var(--human)}.closing-roles{display:grid;grid-template-columns:1fr 1fr 1fr;gap:25px;margin-top:25px}.closing-roles p{font-size:22px;margin-top:11px}.closing-evidence{display:flex;justify-content:space-between;margin-top:28px}.closing-evidence strong{display:block;font-size:39px;letter-spacing:-1px}.closing-evidence span{display:block;font-size:18px;color:var(--muted);margin-top:5px}.closing-evidence+.takeaway{font-size:28px}.notes{display:none!important}#controls{position:fixed;bottom:8px;left:50%;transform:translateX(-50%);background:#173e43;color:#fff;display:flex;align-items:center;gap:13px;border-radius:4px;padding:6px 9px;font-size:13px;z-index:5;opacity:0;transition:opacity .2s}body:hover #controls,#controls:focus-within{opacity:1}#controls button{background:transparent;border:1px solid #638083;border-radius:3px;color:inherit;padding:5px 10px;cursor:pointer}#controls button:disabled{opacity:.4;cursor:default}#controls button:focus-visible{outline:2px solid #dfbd87}#notes-panel{display:none;position:fixed;inset:30px 60px;background:#f6f4ed;color:#173e43;z-index:10;padding:35px 45px;overflow:auto;box-shadow:0 10px 80px #0008}#notes-panel.open{display:block}#notes-panel h3{font-size:27px}#notes-panel p,#notes-panel li{font-size:19px}#notes-panel .close{float:right;background:#173e43;color:white;border:0;padding:9px 14px;font-size:17px;cursor:pointer}#notes-panel pre{white-space:pre-wrap;overflow-wrap:anywhere;font-family:inherit;font-size:18px;line-height:1.55}body.rendering #controls{display:none}body.rendering #stage{top:0;left:0;transform:none!important}@media print{@page{size:1280px 720px;margin:0}html,body{overflow:visible;height:auto;background:white}#stage{position:static;transform:none!important;height:auto}.slide{position:relative;display:block!important;break-after:page;page-break-after:always}.slide:last-child{break-after:auto}#controls,#notes-panel{display:none!important}*{-webkit-print-color-adjust:exact;print-color-adjust:exact}}
'''

parts=[]
notes_export=['# Speaker notes: GenAI, Human, Verified','', 'Sanath Kumar and Mahir Nagersheth', '',
              '11 slides. Planned duration: 8 minutes 30 seconds. Rehearse below 10 minutes. Press N in the deck to review notes. Constructed team interventions are marked for confirmation; the actual computations and original prompts are not invented.', '']
for i,s in enumerate(slides,1):
    title_plain=s['title'].replace('<br>',' ')
    note=f"Presenter: {s['speaker']} | Target: {s['seconds']} seconds\n\nMain point: {s['point']}\n\n"+'\n'.join('• '+b for b in s['bullets'])+f"\n\nEmphasize: {s['emphasis']}\n\nTransition: {s['transition']}"
    if s['draft']:
        note+='\n\n'+DRAFT+'\n'+s['draft']
    note+='\n\n[Sources]\n'+s['sources']+'\n[/Sources]'
    heading='h1' if i==1 else 'h2'
    draft_comment='<!-- '+DRAFT+' -->' if s['draft'] else ''
    parts.append(f'<section id="slide-{i}" class="slide {s["cls"]} {"active" if i==1 else ""}" aria-label="Slide {i}: {html.escape(title_plain)}" data-seconds="{s["seconds"]}" data-human-draft="{str(bool(s["draft"])).lower()}"><header><p class="kicker">{s["kicker"]}</p><{heading}>{s["title"]}</{heading}></header><div class="body">{s["body"]}</div><footer class="footer"><span class="roles">GENAI → HUMAN → VERIFIED</span><span>{i:02d} / 11</span></footer>{draft_comment}<aside class="notes" hidden><pre>{html.escape(note)}</pre></aside></section>')
    notes_export += [f'## Slide {i}: {title_plain}','',note,'']

JS = r'''
const slides=[...document.querySelectorAll('.slide')];const stage=document.getElementById('stage');let index=0;
function resize(){const scale=Math.min(innerWidth/1280,innerHeight/720);stage.style.transform=`translate(-50%,-50%) scale(${scale})`;}
function show(n){index=Math.max(0,Math.min(slides.length-1,n));slides.forEach((s,i)=>{s.classList.toggle('active',i===index);s.setAttribute('aria-hidden',String(i!==index))});document.getElementById('count').textContent=`${index+1} / ${slides.length}`;document.getElementById('prev').disabled=index===0;document.getElementById('next').disabled=index===slides.length-1;try{history.replaceState(null,'','#'+(index+1))}catch(e){}if(document.getElementById('notes-panel').classList.contains('open'))fillNotes();}
function fillNotes(){document.getElementById('note-title').textContent=`Slide ${index+1} · Speaker notes`;document.getElementById('note-copy').textContent=slides[index].querySelector('.notes').textContent;}
function toggleNotes(){const panel=document.getElementById('notes-panel');panel.classList.toggle('open');panel.setAttribute('aria-hidden',String(!panel.classList.contains('open')));if(panel.classList.contains('open')){fillNotes();document.getElementById('close-notes').focus()}else document.getElementById('notes-button').focus();}
document.getElementById('prev').onclick=()=>show(index-1);document.getElementById('next').onclick=()=>show(index+1);document.getElementById('notes-button').onclick=toggleNotes;document.getElementById('close-notes').onclick=toggleNotes;
document.addEventListener('keydown',e=>{if(e.ctrlKey||e.metaKey||e.altKey)return;if(e.key.toLowerCase()==='n'){e.preventDefault();toggleNotes();return}if(e.key==='Escape'&&document.getElementById('notes-panel').classList.contains('open')){toggleNotes();return}if(document.getElementById('notes-panel').classList.contains('open'))return;if(['ArrowRight','ArrowDown','PageDown',' '].includes(e.key)){e.preventDefault();show(index+1)}if(['ArrowLeft','ArrowUp','PageUp'].includes(e.key)){e.preventDefault();show(index-1)}if(e.key==='Home')show(0);if(e.key==='End')show(slides.length-1);if(e.key.toLowerCase()==='f'){if(document.fullscreenElement)document.exitFullscreen();else if(document.documentElement.requestFullscreen)document.documentElement.requestFullscreen().catch(()=>{})}});
window.addEventListener('resize',resize);window.addEventListener('hashchange',()=>show((parseInt(location.hash.slice(1),10)||1)-1));resize();show((parseInt(location.hash.slice(1),10)||1)-1);
'''
document='<!doctype html>\n<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="description" content="A critical evaluation of GenAI, human judgment and verification in hospital nurse scheduling."><title>GenAI + Human + Verified | Nurse Scheduling</title><style>'+CSS+'</style></head><body><main id="stage">\n'+'\n'.join(parts)+'</main><nav id="controls" aria-label="Presentation controls"><button id="prev" aria-label="Previous slide">←</button><span id="count" aria-live="polite"></span><button id="next" aria-label="Next slide">→</button><button id="notes-button">Notes (N)</button><span>F: full screen</span></nav><aside id="notes-panel" aria-hidden="true" aria-label="Speaker notes"><button class="close" id="close-notes">Close (Esc)</button><h3 id="note-title"></h3><pre id="note-copy"></pre></aside><script>'+JS+'</script></body></html>'
(BASE/'presentation.html').write_text(document)
(BASE/'PRESENTATION_SCRIPT.md').write_text('\n'.join(notes_export))
assert len(slides)==11 and sum(s['seconds'] for s in slides)==510
print('Updated presentation.html directly: 11 slides, 510-second plan, hidden notes on every slide.')

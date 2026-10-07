import json, math
from pathlib import Path
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, Image, KeepTogether
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.graphics.shapes import Drawing, Line, Rect, Circle, String, Polygon

ROOT=Path(__file__).parent.parent; QA=ROOT/'_support'/'images'; R=json.loads((ROOT/'_support'/'results.json').read_text())
NAVY=colors.HexColor('#24476B'); PALE=colors.HexColor('#EAF1F8'); TEAL=colors.HexColor('#187F83'); GREY=colors.HexColor('#55616D')
styles=getSampleStyleSheet()
styles.add(ParagraphStyle(name='Body',fontName='Helvetica',fontSize=10,leading=14,spaceAfter=7))
styles.add(ParagraphStyle(name='SmallB',fontName='Helvetica',fontSize=8.5,leading=11,spaceAfter=5))
styles.add(ParagraphStyle(name='CaptionB',fontName='Helvetica',fontSize=8,leading=10,textColor=GREY,spaceBefore=4,spaceAfter=9))
styles.add(ParagraphStyle(name='HeadB',fontName='Helvetica-Bold',fontSize=16,leading=20,textColor=NAVY,spaceAfter=12))
styles.add(ParagraphStyle(name='SubB',fontName='Helvetica-Bold',fontSize=11,leading=15,textColor=NAVY,spaceBefore=7,spaceAfter=6))
styles.add(ParagraphStyle(name='CodeB',fontName='Courier',fontSize=8,leading=11,spaceAfter=6))
S=[]
def p(t,style='Body'):S.append(Paragraph(t,styles[style]))
def h(t):p(t,'HeadB')
def sub(t):p(t,'SubB')
def page(t):S.append(PageBreak());h(t)
def tab(rows,widths=None,size=9,pad=5):
 st=ParagraphStyle('cell',fontName='Helvetica',fontSize=size,leading=size+3)
 formatted=[[Paragraph(str(v),st) for v in rr] for rr in rows]
 t=Table(formatted,colWidths=widths,repeatRows=1,hAlign='LEFT')
 t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),PALE),('VALIGN',(0,0),(-1,-1),'TOP'),('LINEBELOW',(0,0),(-1,0),.7,NAVY),('LINEBELOW',(0,-1),(-1,-1),.4,colors.HexColor('#BCCAD8')),('LEFTPADDING',(0,0),(-1,-1),6),('RIGHTPADDING',(0,0),(-1,-1),6),('TOPPADDING',(0,0),(-1,-1),pad),('BOTTOMPADDING',(0,0),(-1,-1),pad)]));S.append(t);S.append(Spacer(1,9))
def img(name,caption,maxh=250,width=510):
 im=Image(str(QA/(name+'.png')));scale=min(width/im.imageWidth,maxh/im.imageHeight);im.drawWidth=im.imageWidth*scale;im.drawHeight=im.imageHeight*scale;im.hAlign='LEFT';S.append(im);p(caption,'CaptionB')
def arrow(d,x1,y1,x2,y2,color=GREY,width=.9):
 d.add(Line(x1,y1,x2,y2,strokeColor=color,strokeWidth=width));a=math.atan2(y2-y1,x2-x1);k=5
 d.add(Polygon([x2,y2,x2-k*math.cos(a-.5),y2-k*math.sin(a-.5),x2-k*math.cos(a+.5),y2-k*math.sin(a+.5)],fillColor=color,strokeColor=color))
def box(d,x,y,w,label,detail):
 d.add(Rect(x,y-18,w,36,rx=4,fillColor=PALE,strokeColor=NAVY,strokeWidth=.8));d.add(String(x+w/2,y+3,label,fontName='Helvetica-Bold',fontSize=9,textAnchor='middle',fillColor=NAVY));d.add(String(x+w/2,y-9,detail,fontSize=8,textAnchor='middle',fillColor=GREY))
def airline():
 d=Drawing(510,265);oy=[215,130,45];hy=[182,78];dy=oy
 cap1=[[150,100],[100,100],[100,80]];cap2=[[150,120,100],[120,150,120]]
 for i in range(3):
  for k in range(2):
   arrow(d,105,oy[i],218,hy[k]);xx=143 if k==0 else 177;t=(xx-105)/113;yy=oy[i]+t*(hy[k]-oy[i]);d.add(Rect(xx-11,yy-6,24,12,fillColor=colors.white,strokeColor=None));d.add(String(xx,yy-3,str(cap1[i][k]),fontSize=8,textAnchor='middle'))
 for k in range(2):
  for j in range(3):
   arrow(d,294,hy[k],411,dy[j]);xx=326 if k==0 else 377;t=(xx-294)/117;yy=hy[k]+t*(dy[j]-hy[k]);d.add(Rect(xx-11,yy-6,24,12,fillColor=colors.white,strokeColor=None));d.add(String(xx,yy-3,str(cap2[k][j]),fontSize=8,textAnchor='middle'))
 for y,n,s in zip(oy,['Pittsburgh','Cleveland','Columbus'],[200,150,100]):box(d,3,y,102,n,f'Supply +{s}')
 for y,n in zip(hy,['Chicago','Atlanta']):box(d,218,y,76,n,'Net supply 0')
 for y,n,s in zip(dy,['Miami','Orlando','New York'],[150,150,150]):box(d,411,y,97,n,f'Demand {s}')
 d.add(String(255,251,'All arc labels are passenger capacities',fontSize=9,textAnchor='middle',fillColor=GREY));return d
def mentor_network():
 d=Drawing(510,300);ys=[264,220,176,132,88,44];names=['Alice','Ben','Carlos','Diana','Emma','Frank'];selected={(a,b) for a,b,v in R['p4']['assignments']}
 for i in range(6):
  arrow(d,38,154,105,ys[i],colors.HexColor('#B8C3CE'),.6);arrow(d,406,ys[i],476,154,colors.HexColor('#B8C3CE'),.6)
 for i in range(6):
  for j in range(6):
   if R['p4']['scores'][i][j] and (names[i],names[j]) not in selected:arrow(d,168,ys[i],344,ys[j],colors.HexColor('#CFD7DF'),.7)
 for i in range(6):
  for j in range(6):
   if (names[i],names[j]) in selected:arrow(d,168,ys[i],344,ys[j],TEAL,1.6)
 for i in range(6):
  for x in [105,344]:
   d.add(Rect(x,ys[i]-10,63,20,rx=3,fillColor=PALE,strokeColor=NAVY));d.add(String(x+31.5,ys[i]-3,names[i],textAnchor='middle',fontSize=9))
 for x,label in [(22,'s'),(490,'t')]:d.add(Circle(x,154,15,fillColor=PALE,strokeColor=NAVY));d.add(String(x,151,label,textAnchor='middle',fontSize=10))
 d.add(String(22,128,'+6',fontSize=9,textAnchor='middle'));d.add(String(490,128,'-6',fontSize=9,textAnchor='middle'))
 d.add(String(137,288,'Mentor copies',fontSize=9,textAnchor='middle'));d.add(String(376,288,'Mentee copies',fontSize=9,textAnchor='middle'))
 d.add(String(56,280,'cap. 3',fontSize=8));d.add(String(445,280,'cap. 1',fontSize=8));d.add(String(255,12,'Middle arcs: capacity 1; score from the preference table. Teal = selected.',fontSize=8,textAnchor='middle'));return d
def costgraph():
 d=Drawing(510,260);x0=42;y0=36;sx=6.7;sy=.83
 for cost in range(0,251,50):
  yy=y0+sy*cost;d.add(Line(x0,yy,490,yy,strokeColor=colors.HexColor('#DBE3EB'),strokeWidth=.5));d.add(String(x0-7,yy-3,str(cost),fontSize=8,textAnchor='end'))
 for dd in range(0,71,10):d.add(String(x0+sx*dd,y0-13,str(dd),fontSize=8,textAnchor='middle'))
 d.add(Line(x0,y0,492,y0,strokeColor=GREY));d.add(Line(x0,y0,x0,245,strokeColor=GREY))
 for a,b in [((0,80),(30,80)),((30,80),(47.5,97.5)),((47.5,97.5),(65,220))]:d.add(Line(x0+a[0]*sx,y0+a[1]*sy,x0+b[0]*sx,y0+b[1]*sy,strokeColor=TEAL,strokeWidth=2.5))
 for dd,cc,label,dx,dy in [(30,80,'(30, 80)',-20,11),(47.5,97.5,'(47.5, 97.5)',-52,12),(60,185,'(60, 185)',-76,1),(65,220,'(65, 220)',-57,10)]:
  d.add(Circle(x0+sx*dd,y0+sy*cc,3,fillColor=TEAL,strokeColor=None));d.add(String(x0+sx*dd+dx,y0+sy*cc+dy,label,fontSize=8))
 d.add(Line(x0+sx*65,y0,x0+sx*65,y0+sy*220,strokeColor=GREY,strokeDashArray=[3,3]));d.add(String(257,7,'Required lunches D',fontSize=9,textAnchor='middle'));d.add(String(42,248,'Minimum cost ($)',fontSize=9));return d

h('Decision Making Under Uncertainty | HW2')
p('<b>Mahir Nagersheth (mnagersh)</b><br/>Canvas Excel uploader: mnagersh<br/>Submission file: DMU_HW2_mnagersh','SmallB')
p('Page guide: Problem 1, pp. 1-4 and 16; Problem 2, p. 5; Problem 3, pp. 6-12 and 17-20; Problem 4, pp. 13-15 and 21. Pages 16-21 contain actual Excel Solver Parameters screenshots.','SmallB')
sub('Problem 1(a). Linear program')
p('Let x<sub>j</sub> be the number of meals of Dish j prepared, j = 1, 2, 3. Parameters are unit costs c = (4, 1, 3) dollars, cooking times t = (3, 2, 2) minutes, and storage requirements a = (0.10, 0.20, 0.15) shelves. Capacity is 180 minutes and 8 shelves; demand is 60 meals; each dish has a minimum of 10 meals.')
p('<b>Minimize</b> C = 4x<sub>1</sub> + x<sub>2</sub> + 3x<sub>3</sub><br/>subject to:<br/>3x<sub>1</sub> + 2x<sub>2</sub> + 2x<sub>3</sub> &le; 180 &nbsp; (cooking time)<br/>0.10x<sub>1</sub> + 0.20x<sub>2</sub> + 0.15x<sub>3</sub> &le; 8 &nbsp; (storage)<br/>x<sub>1</sub> + x<sub>2</sub> + x<sub>3</sub> &ge; 60 &nbsp; (demand)<br/>x<sub>j</sub> &ge; 10, j = 1, 2, 3 &nbsp; (variety).')
p('Use continuous variables for the LP and its sensitivity report. The optimum is already integral, so it is also a valid whole-meal plan.','SmallB')
sub('Problem 1(b). Excel Solver solution')
p('<b>Prepare 35 Dish 1 meals, 15 Dish 2 meals, and 10 Dish 3 meals, at a minimum cost of $185.</b> This serves 60 students, uses 155 minutes and all 8 shelves, and meets every variety requirement.')
img('p1_values','Excel worksheet image: P1 Lunch!A4:E20. Decisions B10:D10; costs B5:D5; time B6:D6; storage B7:D7; minima B8:D8; objective B12; constraint limits D15:D20.',maxh=242)

page('Problem 1(c-e) | Sensitivity and binding constraints')
sub('(c) Sensitivity report')
p('The following sensitivity values were derived from the optimal LP basis and checked against the Excel solution. This is an <b>analytical sensitivity report</b>; the automated native Excel report command did not create a report sheet. All ranges below vary one input at a time.','SmallB')
tab([['Variable','Value','Cost','Allowable increase','Allowable decrease'],['Dish 1',35,4,1,3],['Dish 2',15,1,1,'Unlimited'],['Dish 3',10,3,'Unlimited',0.5]],[100,65,60,140,145])
tab([['Constraint','LHS','RHS','Shadow price','Allow. increase','Allow. decrease'],['Cooking time',155,180,0,'Unlimited',25],['Storage',8,8,-30,2.5,.5],['Demand',60,60,7,5,12.5],['Dish 1 minimum',35,10,0,25,'Unlimited'],['Dish 2 minimum',15,10,0,5,'Unlimited'],['Dish 3 minimum',10,10,.5,10,10]],[115,45,45,95,105,105],size=8.5)
p('With the minimum constraints represented explicitly, the variable reduced costs are zero and the Dish 3 minimum has shadow price 0.5. If minimum quantities are represented as variable bounds, the Dish 3 reduced cost is 0.5 instead. These are equivalent representations.','SmallB')
sub('(d) Binding constraints')
p('<b>Storage, demand, and the Dish 3 minimum bind</b>: their left-hand sides equal their right-hand sides. All storage is used, exactly 60 meals are prepared, and exactly 10 Dish 3 meals are made. Cooking time has 25 minutes of slack; Dish 1 and Dish 2 minima have slack of 25 and 5 meals.')
sub('(e) Shadow prices in context')
p('<b>Storage: -$30 per shelf.</b> An additional shelf lowers minimum cost by $30 while storage capacity is between <b>7.5 and 10.5 shelves</b>. For example, 9 shelves would give cost 185 - 30 = $155. This does not value extra cooking time or a simultaneous demand change.')
p('<b>Demand: +$7 per meal.</b> An additional required lunch raises minimum cost by $7 while demand is between <b>47.5 and 65 meals</b>. For integer demand, the range is 48 through 65. For example, 61 meals cost $192.')
p('<b>Dish 3 minimum: +$0.50 per meal.</b> Increasing the required Dish 3 minimum by one raises optimal cost by $0.50 while this minimum is between <b>0 and 20 meals</b>. For example, a minimum of 11 produces cost $185.50 in the continuous LP.')
p('At range endpoints a different basis can become optimal; these marginal interpretations need not continue beyond the endpoints.','SmallB')

page('Problem 1(f) | Cost as lunch demand changes')
p('Let D be the required number of lunches, keeping all other parameters fixed. Since all unit costs are positive, the school prepares max(D, 30) meals whenever the model is feasible. The 30-meal floor comes from the three dish minima.')
S.append(costgraph());p('Continuous LP value function. The point D = 60 is the assigned case; demand above 65 is infeasible.','CaptionB')
tab([['Demand interval','Optimal (Dish 1, Dish 2, Dish 3)','Minimum cost'],['0 &le; D &le; 30','(10, 10, 10)','$80'],['30 &le; D &le; 47.5','(10, D - 20, 10)','$D + 50'],['47.5 &le; D &le; 65','(2D - 85, 75 - D, 10)','$7D - 235'],['D &gt; 65','Infeasible','No finite cost']],[120,240,150])
p('Initially, extra demand is met with the cheapest dish, Dish 2. At D = 47.5, storage becomes binding. Beyond that point, an extra lunch requires two additional Dish 1 meals and one fewer Dish 2 meal, so its marginal cost is 2(4) - 1 = $7.')
sub('Maximum number of lunches: 65')
p('Let N = x<sub>1</sub> + x<sub>2</sub> + x<sub>3</sub>. Storage usage can be written as 0.1N + 0.1x<sub>2</sub> + 0.05x<sub>3</sub>. Because x<sub>2</sub>, x<sub>3</sub> &ge; 10, storage is at least 0.1N + 1.5. Hence 0.1N + 1.5 &le; 8 implies <b>N &le; 65</b>.')
p('The plan <b>(45, 10, 10)</b> attains this bound: storage = 8, cooking time = 175 &le; 180, and cost = <b>$220</b>. Thus 65 is feasible and is the maximum, including when meals must be whole numbers.')
p('The P1 Demand worksheet contains a formula-based demand grid and an Excel scatter chart. Fractional demand is used only to show the continuous LP sensitivity curve.','SmallB')

page('Problem 1 | Excel formulas and Solver settings')
img('p1_settings','Excel image: P1 Lunch!A23:H26. Solver model is saved in the workbook.',maxh=95)
tab([['Cell / range','Meaning / formula'],['B10:D10','Changing cells (35, 15, 10)'],['B12','=SUMPRODUCT(B5:D5,B10:D10)'],['B15','=SUMPRODUCT(B6:D6,B10:D10)'],['B16','=SUMPRODUCT(B7:D7,B10:D10)'],['B17','=SUM(B10:D10)'],['B18, B19, B20','=B10 ; =C10 ; =D10'],['D18, D19, D20','=B8 ; =C8 ; =D8'],['E15:E16','=D15-B15, filled down'],['E17:E20','=B17-D17, filled down']],[120,390],size=9)
sub('Formula documentation exported from Excel')
img('p1_formulas','Updated Excel image: P1 Lunch!A28:H44. Formulas are written as text so they remain visible alongside the computed model.',maxh=245)
p('Solver objective: minimize B12. Constraints: B15:B16 &le; D15:D16 and B17:B20 &ge; D17:D20. Method: Simplex LP, with nonnegative variables. Excel Solver returned status 0 from the starting point (10, 10, 10).','SmallB')

page('Problem 2 | True / False with justifications')
for title,text in [
('(a) True.','For a continuous LP at an optimal primal-dual solution, complementary slackness gives (shadow price) &times; (slack) = 0. A non-binding inequality has strictly positive slack, so its shadow price is zero. This is a statement about LP sensitivity, not integer or nonlinear optimization.'),
('(b) False.','Multiple optima do not require zero allowable coefficient changes for two distinct variables. Counterexample: minimize x<sub>1</sub>, subject to x<sub>1</sub> &ge; 1 and 0 &le; x<sub>2</sub> &le; 1. Every (1, t), 0 &le; t &le; 1, is optimal. The coefficient of x<sub>1</sub> can decrease from 1 to 0 or increase without limit. Only x<sub>2</sub>, whose coefficient is zero, has a zero allowable change in at least one direction. At the optimum (1, 0), its allowable decrease is zero.'),
('(c) False as a guaranteed conclusion.','The two RHS changes occur simultaneously. The 100% rule gives 1/2 + 1/1 = 1.5 = 150%, so the separate ranges do not guarantee that the current shadow prices remain valid. The change might be $8, but the report alone cannot establish it. Re-solve the jointly modified model. Exceeding 100% is inconclusive, not proof that $8 is impossible.'),
('(d) False.','Resource 1 has allowable increase 2, so its $5 shadow price is valid only up to RHS 12, holding other data fixed. RHS 14 is outside that range. The objective increase cannot be asserted to equal 5 &times; 4 = $20.'),
('(e) False as stated.','The $3 shadow price applies to Resource 2 only over RHS values from 8 - 5 = 3 through 8 + 1 = 9, holding everything else fixed. One additional unit, from 8 to 9, changes the objective by $3. The claim is not valid for every additional unit indefinitely.'),
('(f) True.','Both constraints bind: Resource 1 has final value 10 equal to RHS 10, and Resource 2 has final value 8 equal to RHS 8.')]:sub(title);p(text)
sub('Role of the stated purchase costs')
p('The $5 and $4 resource costs do not change the validity ranges. If the objective is profit before paying for newly purchased resources, the net gain from one extra unit is $5 - $5 = $0 for Resource 1 and $3 - $4 = -$1 for Resource 2, within their individual ranges. Do not subtract purchase costs a second time if they are already included in the stated objective.','SmallB')

page('Problem 3(a) | Airline network and input data')
p('Origins: Pittsburgh, Cleveland, Columbus. Intermediate hubs: Chicago and Atlanta. Destinations: Miami, Orlando, New York. Total supply and demand are both 450 passengers. The graph shows aggregate node balances; the model also preserves each origin-destination pair.')
S.append(airline())
tab([['OD demand','Miami','Orlando','New York','Origin total'],['Pittsburgh',100,60,40,200],['Cleveland',50,50,50,150],['Columbus',0,40,60,100],['Destination total',150,150,150,450]],[150,90,90,90,90])
tab([['Flight arc','Capacity','Cost / passenger','Flight arc','Capacity','Cost / passenger'],['PIT - CHI',150,'$50','CHI - MIA',150,'$100'],['PIT - ATL',100,'$100','CHI - ORL',120,'$90'],['CLE - CHI',100,'$60','CHI - NYC',100,'$80'],['CLE - ATL',100,'$90','ATL - MIA',120,'$80'],['COL - CHI',100,'$70','ATL - ORL',150,'$70'],['COL - ATL',80,'$80','ATL - NYC',120,'$100']],[105,55,95,105,55,95],size=8.5)
p('Abbreviations: PIT = Pittsburgh; CLE = Cleveland; COL = Columbus; CHI = Chicago; ATL = Atlanta; MIA = Miami; ORL = Orlando; NYC = New York.','CaptionB')

page('Problem 3(b-c) | Network flow formulation and Excel model')
sub('(b) Decision variables, parameters, and objective')
p('Let O be the three origins, H the two hubs, and T the three destinations. D<sub>ij</sub> is demand from origin i to destination j. Let u<sub>ih</sub>, v<sub>hj</sub> be flight capacities and a<sub>ih</sub>, b<sub>hj</sub> the corresponding per-passenger costs.')
p('Define y<sub>ihj</sub> &ge; 0 as passengers from i to j traveling through hub h. These are path flows in the network. One unit of y<sub>ihj</sub> uses one seat on both i &rarr; h and h &rarr; j.')
p('<b>Minimize</b> &Sigma;<sub>i in O, h in H, j in T</sub> (a<sub>ih</sub> + b<sub>hj</sub>) y<sub>ihj</sub>.')
tab([['Constraint','Mathematical statement','Meaning'],['OD demand','&Sigma;<sub>h</sub> y<sub>ihj</sub> = D<sub>ij</sub>, for every i,j','Preserves all nine OD demands'],['First-leg capacity','&Sigma;<sub>j</sub> y<sub>ihj</sub> &le; u<sub>ih</sub>, for every i,h','Seats from each origin to each hub'],['Second-leg capacity','&Sigma;<sub>i</sub> y<sub>ihj</sub> &le; v<sub>hj</sub>, for every h,j','Seats from each hub to each destination'],['Nonnegativity','y<sub>ihj</sub> &ge; 0','No negative passengers']],[108,245,157],size=9)
p('Hub conservation holds automatically: the same y<sub>ihj</sub> is counted on both legs. Equivalently, use arc flows f<sub>a</sub><sup>ij</sup> for each OD commodity; outflow minus inflow equals D<sub>ij</sub> at i, -D<sub>ij</sub> at j, and 0 elsewhere, with &Sigma;<sub>ij</sub> f<sub>a</sub><sup>ij</sup> &le; capacity<sub>a</sub>. A model using only aggregate city balances would omit the given OD requirements.')
sub('(c) Excel implementation and settings')
p('Each scenario has its own worksheet. Rows 6:14 represent the nine OD pairs. D6:D14 and E6:E14 are flows through Chicago and Atlanta. F6:F14 are direct flows, fixed to zero in the base scenario. All reported solutions are integral.')
tab([['Solver setting','All P3 worksheets'],['Objective','Minimize B16 = SUM(L6:L14)'],['Changing cells','D6:F14'],['Demand constraints','G6:G14 = C6:C14'],['Existing flight capacities','E19:E30 &le; C19:C30'],['Direct flight capacities','D33:D41 &le; C33:C41'],['Bounds and method','D6:F14 &ge; 0; Simplex LP']],[135,375])
p('Row cost L6 = SUMPRODUCT(D6:F6,I6:K6), filled through row 14. Assigned total G6 = SUM(D6:F6). I6 = $D$19+$D$25 and J6 = $D$20+$D$28 add the appropriate leg costs. Full formula examples and cell references appear on page 12.','SmallB')

page('Problem 3(d) | Base network optimum')
p('<b>Minimum total cost: $69,700 for all 450 passengers.</b> The table below gives the number of passengers assigned to each flight. Multiple routings can achieve the same optimum; this is the solution saved by Excel.')
arcs=[('PIT - CHI',150),('PIT - ATL',100),('CLE - CHI',100),('CLE - ATL',100),('COL - CHI',100),('COL - ATL',80),('CHI - MIA',150),('CHI - ORL',120),('CHI - NYC',100),('ATL - MIA',120),('ATL - ORL',150),('ATL - NYC',120)]
def flatlegs(k):return [x for rr in R['p3'][k]['first_legs'] for x in rr]+[x for rr in R['p3'][k]['second_legs'] for x in rr]
flow=flatlegs('Base');tab([['Flight','Passengers','Capacity','Unused seats']]+[[a,f,c,c-f] for (a,c),f in zip(arcs,flow)],[165,110,110,125])
img('p3_base','Excel image: P3 Base!A5:H14. Each row sums to its specified OD demand; the Residual column is zero.',maxh=185)
p('Cost check: first legs cost $30,800 and second legs cost $38,900, totaling $69,700. Exactly 450 seats are used on each connecting leg across the network.','SmallB')

page('Problem 3(e-f) | Add direct flights from Pittsburgh')
sub('(e) Prediction before optimization')
p('A reasonable initial prediction is <b>Pittsburgh</b>, because it supplies 200 passengers, the largest origin demand. Its three direct flights can accommodate all 200 and avoid expensive connecting itineraries. This is only a heuristic: the best choice also depends on which constrained hub seats are freed for the other origins.')
sub('Model changes for each direct-flight scenario')
p('Add z<sub>ij</sub> &ge; 0 for direct passengers and add &Sigma;<sub>ij</sub> d<sub>ij</sub>z<sub>ij</sub> to the objective. Replace each demand equation with &Sigma;<sub>h</sub> y<sub>ihj</sub> + z<sub>ij</sub> = D<sub>ij</sub>. For selected origin k, enforce z<sub>kj</sub> &le; direct capacity<sub>kj</sub>; for all i &ne; k enforce z<sub>ij</sub> = 0. Existing connecting-flight capacity constraints stay unchanged because direct passengers do not use those arcs.')
sub('(f) Pittsburgh direct flights')
tab([['Direct flight','Capacity','Unit cost','Optimal passengers'],['PIT - MIA',100,'$120',100],['PIT - ORL',60,'$80',60],['PIT - NYC',40,'$70',40]],[160,100,110,140])
p('New bounds: z<sub>PIT,MIA</sub> &le; 100, z<sub>PIT,ORL</sub> &le; 60, z<sub>PIT,NYC</sub> &le; 40; all other direct flows are zero. In P3 Pittsburgh, C33:C35 contain these limits and C36:C41 are zero.')
p('<b>Minimum cost: $57,900; savings: $11,800.</b> All 200 Pittsburgh passengers travel directly. Direct-flight cost is $19,600; the other 250 passengers connect at a cost of $38,300.')
img('p3_pittsburgh','Excel image: P3 Pittsburgh!A5:H14. Direct decisions are in F6:F8. All demand residuals are zero.',maxh=187)
p('The full 12-arc connecting-flight assignment for this scenario is included in the comparison table on page 11.','SmallB')

page('Problem 3(g-h) | Cleveland and Columbus alternatives')
sub('(g) Add direct flights from Cleveland')
tab([['Direct flight','Capacity','Unit cost','Passengers'],['CLE - MIA',100,'$110',50],['CLE - ORL',60,'$75',50],['CLE - NYC',50,'$65',50]],[160,100,110,140])
p('Set z<sub>CLE,MIA</sub> &le; 100, z<sub>CLE,ORL</sub> &le; 60, z<sub>CLE,NYC</sub> &le; 50; all other direct flows are zero. In P3 Cleveland, C36:C38 contain these limits. Use the changed OD equations on page 9 and retain every connecting capacity.')
p('<b>Minimum cost: $57,600; savings: $12,100.</b> All 150 Cleveland passengers fly directly, costing $12,500. The remaining 300 connect at a cost of $45,100.')
img('p3_cleveland','Excel image: P3 Cleveland!A5:H14. Direct decisions are F9:F11.',maxh=100)
sub('(h) Add direct flights from Columbus')
tab([['Direct flight','Capacity','Unit cost','Passengers'],['COL - MIA',80,'$100',0],['COL - ORL',40,'$70',40],['COL - NYC',60,'$60',60]],[160,100,110,140])
p('Set z<sub>COL,MIA</sub> &le; 80, z<sub>COL,ORL</sub> &le; 40, z<sub>COL,NYC</sub> &le; 60; all other direct flows are zero. In P3 Columbus, C39:C41 contain these limits. Columbus-Miami demand is zero, so this new flight carries no one.')
p('<b>Minimum cost: $59,500; savings: $10,200.</b> All 100 Columbus passengers fly directly, costing $6,400. The other 350 connect at a cost of $53,100.')
img('p3_columbus','Excel image: P3 Columbus!A5:H14. Direct decisions are F12:F14.',maxh=100)

page('Problem 3(f-i) | Flight assignments and recommendation')
p('All entries are passengers. Capacities refer to the original connecting flights. These assignments, together with the direct-flight counts on pages 9-10, specify every flight in each scenario.')
scenario_keys=['Base','Pittsburgh','Cleveland','Columbus']
tab([['Connecting flight','Capacity','Base','PIT direct','CLE direct','COL direct']]+[[a,c]+[flatlegs(k)[i] for k in scenario_keys] for i,(a,c) in enumerate(arcs)],[140,70,65,78,78,79])
tab([['Scenario','Total cost','Savings vs. base','Direct passengers']]+[[k,f"${R['p3'][k]['cost']:,.0f}",f"${69700-R['p3'][k]['cost']:,.0f}",sum(sum(rr) for rr in R['p3'][k]['direct'])] for k in scenario_keys],[145,120,135,110])
sub('(i) Recommendation: Cleveland')
p('<b>Offer the direct flights from Cleveland.</b> Its total cost of $57,600 is the lowest, saving $12,100 relative to the base network, or approximately 17.36%. It is $300 cheaper than Pittsburgh direct flights and $1,900 cheaper than Columbus direct flights.')
p('Cleveland wins even though Pittsburgh has more passengers. The total-cost comparison includes both the direct fares and the best rerouting of all remaining connecting passengers. The initial largest-demand heuristic therefore does not determine the best network-wide decision.')
p('This recommendation uses the supplied per-passenger costs only. The problem does not give fixed launch costs or require every new flight to carry passengers; neither has been added to the model.','SmallB')

page('Problem 3 | Spreadsheet formula documentation')
img('p3_formulas','Excel image: P3 Base!A43:L57. The same formulas and Solver constraints apply to all four scenario worksheets.',maxh=315)
tab([['Cell(s)','Formula / mapping'],['D6:F14','Decision variables: Chicago, Atlanta, direct'],['G6, H6','=SUM(D6:F6) ; =G6-C6 (fill down)'],['I6, J6','=$D$19+$D$25 ; =$D$20+$D$28'],['L6','=SUMPRODUCT(D6:F6,I6:K6) (fill down)'],['B16','=SUM(L6:L14)'],['E19, E20','=SUM(D6:D8) ; =SUM(E6:E8)'],['E25','=D6+D9+D12'],['F19','=C19-E19 (capacity slack; fill down)'],['D33, E33','=F6 ; =C33-D33 (direct flow / slack)']],[110,400],size=8.5)
p('First-leg rows 19:24 are ordered by origin, then Chicago/Atlanta. Second-leg rows 25:30 are Chicago to the three destinations, then Atlanta to the three destinations. Direct rows 33:41 follow the same OD order as rows 6:14. This mapping makes every flight capacity and each path cost auditable.','SmallB')
p('Excel Solver returned status 0 for all four scenarios from zero-valued decision cells. All OD residuals are zero, every capacity slack is nonnegative, and every final decision is an integer.','SmallB')

page('Problem 4(a-b) | Mentoring network model')
sub('(a) Parameters and decision variables')
p('Create a mentor copy and a mentee copy of every person. Let E be the allowed mentor-mentee pairs with a numeric preference score in the supplied table; s<sub>ij</sub> is that score. A dash is forbidden, including self-mentoring. These allowed pairs encode the stated role restrictions.')
p('Let x<sub>ij</sub> = 1 if mentor i is assigned to mentee j and 0 otherwise, for (i,j) in E. <b>Maximize &Sigma;<sub>(i,j) in E</sub> s<sub>ij</sub>x<sub>ij</sub></b>, subject to:')
p('&Sigma;<sub>i:(i,j) in E</sub> x<sub>ij</sub> = 1 for every mentee j;<br/>&Sigma;<sub>j:(i,j) in E</sub> x<sub>ij</sub> &le; 3 for every mentor i;<br/>0 &le; x<sub>ij</sub> &le; 1 on allowed pairs; x<sub>ij</sub> = 0 on forbidden pairs.')
p('The network construction is source s &rarr; mentor i (capacity 3, cost 0), mentor i &rarr; mentee j on allowed pairs (capacity 1, cost -s<sub>ij</sub>), and mentee j &rarr; sink t (capacity 1, cost 0). Send exactly six units and minimize total cost. Source supply is +6, sink supply is -6, and all other nodes have net supply 0.','SmallB')
p('All six mentee-to-sink arcs must be saturated, so every person gets exactly one mentor. Integral capacities make the network LP admit an integral optimum; binary constraints are optional for this formulation.','SmallB')
sub('(b) Graphical representation')
network=mentor_network();network.scale(.8,.8);network.width=408;network.height=240;S.append(network)
p('A separate copy on each side lets a person be both mentor and mentee. Grey middle arcs are eligible but unselected; teal middle arcs show the optimal assignment. Frank has no outgoing mentor arcs.','CaptionB')
tab([['Mentor / mentee','Alice','Ben','Carlos','Diana','Emma','Frank']]+[[n]+[str(v) if v else '-' for v in R['p4']['scores'][i]] for i,n in enumerate(['Alice','Ben','Carlos','Diana','Emma','Frank'])],[120,65,65,65,65,65,65],size=8,pad=3)

page('Problem 4(c-d) | Excel solution and company results')
sub('(c) Excel Solver setup')
p('Maximize P4 Mentoring!B33 = SUMPRODUCT(B5:G10,B15:G20), changing B15:G20. Enforce H15:H20 &le; I15:I20 (mentor capacities), B22:G22 = B23:G23 (one mentor each), B15:G20 &le; B26:G31 (allowed-pair mask), and nonnegativity. Use Simplex LP. Solver returned status 0 with an integral solution from an all-zero starting point.','SmallB')
img('p4_values','Excel image: P4 Mentoring!A14:I23. Rows are mentors and columns are mentees; 1 means assigned. H15:H20 show mentor loads.',maxh=185)
sub('(d) Assignments to report to the company')
tab([['Mentee','Assigned mentor','Preference score'],['Alice','Ben',65],['Ben','Carlos',70],['Carlos','Ben',20],['Diana','Alice',100],['Emma','Alice',95],['Frank','Alice',85],['Total','',435]],[170,200,140])
p('<b>Total preference score: 435.</b> Alice mentors three people, Ben mentors two, Carlos mentors one, and Diana, Emma, and Frank mentor none. Every person has exactly one mentor, every pairing is allowed, and no mentor exceeds three mentees.')
p('Optimality check: the maximum available scores for the six individual mentees are 65, 70, 20, 100, 95, and 85. Their sum is 435. This assignment attains all six individual maxima while respecting mentor capacities, so no feasible assignment can do better.','SmallB')

page('Problem 4(e) | Interpretation, limitations, and improvements')
p('Within the supplied scores and eligibility rules, <b>everyone receives their highest-scoring eligible mentor</b>. The solution is therefore optimal both in total score and for each person individually among the listed options. This still does not guarantee a strong real-world mentoring program.')
sub('Preference scores and limited options')
p('Carlos receives a score of only 20, but that is his best allowed match: Alice scores 10 and Ben scores 20. Reassigning the existing people cannot improve Carlos beyond 20. HR could recruit additional eligible mentors, gather more candidate matches, and ask whether the scores are comparable across people. Minimum acceptable-score constraints or a max-min objective can protect satisfaction, but a threshold above 20 makes this particular candidate set infeasible.')
sub('Reciprocal mentoring and hierarchy')
p('Ben mentors Carlos and Carlos mentors Ben. That may weaken independence or create a conflict in feedback. If reciprocal pairs are undesirable, add x<sub>ij</sub> + x<sub>ji</sub> &le; 1 for eligible pairs. However, requiring every person in the highest role to have a same-level mentor necessarily creates some directed cycle within that finite highest-role group. Prohibiting every cycle while retaining those rules would make the model infeasible. Allow an external senior mentor or exempt selected highest-role staff to remove that structural issue.')
sub('Workload and suitability beyond one score')
p('Three mentees need not require equal effort. Replace the uniform cap with mentor-specific available hours and estimated mentoring time, and include availability, skill coverage, conflicts of interest, and voluntary participation. Collect feedback after a trial period and update the scores before rerunning the model.')
sub('Excel formula documentation')
img('p4_formulas','Excel image: P4 Mentoring!A35:J43. The workbook records exact constraints and readable objective/load formulas.',maxh=175)
p('Source documents: HW2.pdf, Problems 1-4; Submission example.pdf, required submission components. The submitted workbook is DMU_HW2_mnagersh.xlsx. Models were solved in Microsoft Excel Solver and independently verified with SciPy/HiGHS. The mentoring optimum was also checked by exhaustive enumeration.','SmallB')

for title,tag,description in [
 ('Problem 1 | Excel Solver Parameters','p1','P1 Lunch: minimize B12 by changing B10:D10. The screenshot shows the saved cooking, storage, demand, and variety constraints.'),
 ('Problem 3(c) | Base model Solver Parameters','base','P3 Base: minimize B16 by changing D6:F14. The direct-flight capacity cells C33:C41 are all zero in this scenario.'),
 ('Problem 3(f) | Pittsburgh Solver Parameters','pittsburgh','P3 Pittsburgh: minimize B16 by changing D6:F14. C33:C35 allow Pittsburgh direct flights; all other direct-flight capacities are zero.'),
 ('Problem 3(g) | Cleveland Solver Parameters','cleveland','P3 Cleveland: minimize B16 by changing D6:F14. C36:C38 allow Cleveland direct flights; all other direct-flight capacities are zero.'),
 ('Problem 3(h) | Columbus Solver Parameters','columbus','P3 Columbus: minimize B16 by changing D6:F14. C39:C41 allow Columbus direct flights; all other direct-flight capacities are zero.'),
 ('Problem 4(c) | Mentoring Solver Parameters','p4','P4 Mentoring: maximize B33 by changing B15:G20. Constraints enforce mentor capacities, one mentor per mentee, allowed matches, and nonnegativity.')
]:
 page(title)
 p(description)
 img('solver_'+tag,'Actual screenshot of the Excel Solver Parameters dialog for '+({'p1':'P1 Lunch','base':'P3 Base','pittsburgh':'P3 Pittsburgh','cleveland':'P3 Cleveland','columbus':'P3 Columbus','p4':'P4 Mentoring'}[tag])+'.',maxh=565,width=455)

def footer(c,doc):
 c.saveState();c.setStrokeColor(colors.HexColor('#CBD5DF'));c.line(45,37,567,37);c.setFont('Helvetica',8);c.setFillColor(GREY);c.drawString(45,24,'DMU HW2 | Mahir Nagersheth | mnagersh');c.drawRightString(567,24,f'{doc.page}');c.restoreState()
doc=SimpleDocTemplate(str(ROOT/'DMU_HW2_mnagersh.pdf'),pagesize=(612,792),rightMargin=45,leftMargin=45,topMargin=38,bottomMargin=48,title='DMU HW2 - mnagersh',author='Mahir Nagersheth')
doc.build(S,onFirstPage=footer,onLaterPages=footer)
print('Saved',ROOT/'DMU_HW2_mnagersh.pdf')

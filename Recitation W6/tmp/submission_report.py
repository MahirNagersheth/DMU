import sys,json
sys.path.insert(0,'/private/tmp/w6-report-libs')
from pathlib import Path
import openpyxl
from PIL import Image as PILImage
from reportlab.platypus import SimpleDocTemplate,Paragraph,Spacer,Table,TableStyle,PageBreak,Image
from reportlab.lib.styles import getSampleStyleSheet,ParagraphStyle
from reportlab.lib import colors
from pypdf import PdfReader,PdfWriter
p=Path(__file__).parent
wb=openpyxl.load_workbook(p.parent/'outputs/submission/Recitation W6 Completed.xlsx',data_only=True)
d=json.loads((p/'results.json').read_text())
styles=getSampleStyleSheet()
for name,font,size,leading,space,color in [('TitleClean','Helvetica-Bold',20,25,13,'#111111'),('HeadingClean','Helvetica-Bold',13,17,9,'#111111'),('BodyClean','Helvetica',9.5,13.5,8,'#111111'),('SmallClean','Helvetica',7.8,10.5,7,'#555555'),('CellClean','Helvetica',8.6,11.5,0,'#111111')]:
 styles.add(ParagraphStyle(name=name,fontName=font,fontSize=size,leading=leading,spaceAfter=space,textColor=colors.HexColor(color)))
story=[]
def para(s,sty='BodyClean'): return Paragraph(s,styles[sty])
def text(s,sty='BodyClean'): story.append(para(s,sty))
def title(s): text(s,'TitleClean')
def sub(s): text(s,'HeadingClean')
def caption(s): text(s,'SmallClean')
def page(): story.append(PageBreak())
def money(x): return f'${x:,.2f}'
def table(rows,widths):
 tb=Table([[para(str(x),'CellClean') for x in row] for row in rows],colWidths=widths,repeatRows=1,hAlign='LEFT')
 tb.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.HexColor('#E9E9E9')),('LINEBELOW',(0,0),(-1,0),.5,colors.HexColor('#888888')),('LINEBELOW',(0,-1),(-1,-1),.4,colors.HexColor('#BBBBBB')),('TOPPADDING',(0,0),(-1,-1),6),('BOTTOMPADDING',(0,0),(-1,-1),6),('VALIGN',(0,0),(-1,-1),'TOP')]))
 story.extend([tb,Spacer(1,10)])
def img(name,width=500,max_height=None):
 im=PILImage.open(p/'captures'/(name+'.png')); dest=p/'captures'/(name+'-grey.png'); im.convert('L').save(dest)
 h=width*im.height/im.width
 if max_height and h>max_height: width*=max_height/h;h=max_height
 return Image(str(dest),width=width,height=h,hAlign='LEFT')
def figure(name,width=500,max_height=None): story.extend([img(name,width,max_height),Spacer(1,7)])
def side(left,right,widths):
 tb=Table([[left,right]],colWidths=widths,hAlign='LEFT');tb.setStyle(TableStyle([('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),0),('RIGHTPADDING',(0,0),(-1,-1),8),('TOPPADDING',(0,0),(-1,-1),0),('BOTTOMPADDING',(0,0),(-1,-1),0)]));story.extend([tb,Spacer(1,9)])

caption('95-760 | DECISION MAKING UNDER UNCERTAINTY')
title('Week 6 recitation')
sub('Fishery (a): sampling')
text('Fifteen observations were generated from each distribution. The discrete probabilities are 0.20, 0.10, 0.50, 0.10, and 0.10 for outcomes 0, 1, 2, 3, and 4. Independent uniform streams are stored in columns N:S and transformed with Excel formulas.')
figure('sampling')
caption('Excel capture: Sampling!G2:L17. All 15 observations are shown. N(5,2) uses standard deviation 2; Exp(0.4) uses rate 0.4, with mean 2.5.')
table([['Distribution','Excel formula, first observation'],['Uniform (0,1)','=N3'],['Discrete','=LOOKUP(O3,$E$3:$E$7,$B$3:$B$7)'],['Binomial (15,0.7)','=BINOM.INV(15,0.7,P3)'],['Uniform (5,9)','=5+4*Q3'],['Normal (5,2)','=NORM.INV(R3,5,2)'],['Exponential (rate 0.4)','=-LN(1-S3)/0.4']],[185,315])
caption('Uniform draws were generated with NumPy seed 76006 and frozen as workbook inputs. Transformations, profits, summaries, and confidence limits are Excel formulas. Captures come from the completed Excel workbook; Solver images show the actual dialogs.')
caption('Reference: RS W6.pdf. RS W6 Sol.pdf and RS W6 Sol.xlsx were used to check the intended model and workbook structure. Simulation draws and statistics are our own realization.')

page();title('Fishery (b): 70-day simulation')
text('Daily price is Normal($3.65, $0.20). Demand is sampled independently of price. Sold = MIN(3500,Demand); Revenue = Price x Sold; Profit = Revenue - $10,000.')
s=wb['Fishery operations']
table([['Days','Mean profit','Sample SD','95% CI for mean'],[70,money(s['Y4'].value),money(s['Y5'].value),f"{money(s['Y8'].value)} to {money(s['Y9'].value)}"]],[45,105,105,245])
text('Mean = AVERAGE(O4:O73), SD = STDEV.S(O4:O73), and CI = mean +/- T.INV.2T(0.05,69) x SD / SQRT(70). The interval estimates expected daily profit.')
figure('fish_first')
caption('Excel capture: Fishery operations!G3:O38. Days 1-35; the remaining 35 days appear on the next page.')

page();title('Fishery (b): days 36-70')
figure('fish_last')
caption('Excel capture: Fishery operations!G39:O73. Columns match the preceding page: Day, Price RND, Price, Demand RND, Demand, Sold, Revenues, Cost, Profit.')
side([img('fish_prob',200),para('Fishery operations!B2:E10.','SmallClean')],[img('fish_summary',265),para('Fishery operations!X4:Y9.','SmallClean')],[220,280])
text('Exact validation: E[sold] = 0.02(0) + 0.03(1000) + 0.05(2000) + 0.08(3000) + 0.82(3500) = 3,240 fish. E[profit] = 3.65 x 3,240 - 10,000 = <b>$1,826.00</b>, inside the simulation confidence interval.')

page();title('Fishery (c): increasing the sample size')
text('Five hundred days were simulated. Each row uses day 1 through its own day n. Mean = AVERAGE($O$4:Or), SD = STDEV.S($O$4:Or), and CI = mean +/- T.INV.2T(0.05,n-1) x SD / SQRT(n). At n = 1, SD and CI are undefined and left blank.')
s=wb['N analysis']
table([['Days','Mean profit','Sample SD','95% CI for mean'],[500,money(s['Q503'].value),money(s['R503'].value),f"{money(s['S503'].value)} to {money(s['T503'].value)}"]],[45,105,105,245])
figure('n_chart')
caption('Native Excel chart from N analysis. The very wide initial interval reflects the small sample size. All 500 days and cumulative calculations are included in the workbook.')
sub('Final cumulative results')
figure('n_last')
caption('N analysis!P494:T503, days 491-500. Columns: n, Mean, Sample SD, Lower 95% CI, Upper 95% CI.')
text('The running mean need not converge monotonically, but its uncertainty decreases as n grows. The final mean of $1,822.20 is close to the exact expectation of $1,826.00. The intervals describe the mean, not daily-profit percentiles.')

page();title('Fishery (d): choosing the quantity Q')
text('Use the quantity-dependent cost in the solution workbook: <b>Cost(Q) = $3,000 + $2Q</b>. Profit = Price x MIN(Q,Demand) - Cost(Q). A native one-input Excel Data Table evaluates Q = 2,000 to 6,000 in steps of 100, using the same 400 draws for every Q.')
right=[para('Inputs and summary','HeadingClean'),img('q_inputs',230),Spacer(1,12),para('Profit as a function of Q','HeadingClean'),img('q_chart',330),Spacer(1,10),para('<b>Recommendation: Q = 4,000 fish.</b> Simulated mean profit is $2,204.83. Exact expected profit is 3.65 x 3,650 - (3,000 + 2 x 4,000) = <b>$2,322.50</b>.','BodyClean'),para('Beyond 4,000, marginal expected revenue falls below the $2 cost per additional fish.','BodyClean')]
side([img('q_table',140),para('T3:U44: native Data Table.','SmallClean')],right,[160,340])
caption('Excel captures: Analysis on Q!Q3:R14, T3:U44, and its chart. Output U3 = R7; input column T4:T44; column input cell R4. R7 averages O4:O403, so n = 400.')

page();caption('ADDITIONAL PRACTICE');title('Piedmont airline (a) and (b)')
text('<b>(a)</b> Demand ranges from 14 to 25. Tickets sold B = MIN(22,Demand). No-shows follow Binomial(B,0.1); show-ups = B - no-shows. Profit = $150 x B - $500 x MAX(show-ups - 19,0).')
side([para('The 100-flight simulation gives mean <b>$2,749.50</b>, sample SD <b>$362.27</b>, and 95% CI <b>$2,677.62 to $2,821.38</b>. Exact expected profit is $2,733.17. Different random draws give different valid simulation statistics.','BodyClean'),para('The interval uses Student t with 99 degrees of freedom and standard error SD / SQRT(100).','BodyClean')],[img('air_summary',225),para('Airline (a)!R2:S13.','SmallClean')],[265,235])
figure('air_rows')
caption('Airline (a)!B3:K16. The workbook contains all 100 flights; the capture shows the model and first 13 observations.')
text('<b>(b)</b> One hundred samples give a rough estimate, but the observed confidence half-width is $71.88. To target a $10 half-width, the pilot SD gives n >= (1.96 x 362.27 / 10)^2, rounded up to 5,042. Recommend <b>5,100 flights</b>. This targets greater precision than the solution guide\'s approximate 300-flight recommendation.')
text('The 5,100-flight run gives mean $2,727.45, SD $346.12, and 95% CI $2,717.95 to $2,736.95, with half-width $9.50. The same 5,100 samples are used in part (c).')

page();caption('ADDITIONAL PRACTICE');title('Piedmont airline (c): booking limit')
text('Compare limits 19 through 25 using common uniform draws across alternatives and n = 5,100. The native Excel Data Table changes Airline (c)!S2 and links to S8, the mean of K4:K5103. Exact expectations check the close alternatives independently.')
side([img('air_limits',185),para('Airline (c)!R2:S19.','SmallClean')],[img('air_chart',295),para('Native Excel booking-limit chart.','SmallClean')],[205,295])
table([['Booking limit','Simulation mean','Exact expected profit']]+[[cap,money(sim['mean']),money(ex)] for cap,sim,ex in zip(d['air_caps'],d['air_sim'],d['air_exact'])],[100,200,200])
text('<b>Recommend offering 20 tickets.</b> Exact expected profit is $2,767.11, compared with $2,758.69 at 21 and $2,733.17 at 22. Selling fewer than 19 tickets forgoes sales without reducing denied-boarding compensation. Limits above 25 are equivalent to 25 because demand never exceeds 25.')

page();caption('ADDITIONAL PRACTICE');title('Food bank (a): stochastic model')
text('Food types j are vegetables, rice, and cereal. Scenarios s = 1,2,3 have probabilities 0.40, 0.35, and 0.25. Each scenario jointly determines donations a(s,j) and total demand D(s,j), summed over the four organizations. Initial purchases are shared across scenarios.')
figure('food_params',480)
caption('Food bank!B4:F24: donations, organization demand, and scenario totals.')
text('<b>Variables:</b> x(j) is initial cases purchased; E(s,j) is emergency cases purchased after observing scenario s. Both are nonnegative integers. Demand can be aggregated because there are no organization-specific allocation costs or restrictions.')
text('<b>Objective:</b> Minimize 12x(V) + 10x(R) + 15x(C) + SUM_s p(s)[18E(s,V) + 16E(s,R) + 22E(s,C)].')
text('<b>Initial constraints:</b> x(V) + x(R) + x(C) <= 700; 12x(V) + 10x(R) + 15x(C) <= 12000.')
text('<b>Scenario constraints:</b> x(j) + a(s,j) + E(s,j) >= D(s,j) for every scenario-food pair. Emergency spending uses separate funds and is outside the initial $12,000 budget.')
caption('After donations are observed, food is allocated to satisfy every organization. An equivalent allocation model uses regular y(s,i,j) and emergency z(s,i,j), with y + z = d(s,i,j), SUM_i y <= x + a, and SUM_i z = E.')

page();caption('ADDITIONAL PRACTICE');title('Food bank (b) and (c): optimal plan')
text('Excel Solver with Simplex LP returned <b>280 vegetable cases, 180 rice cases, and 240 cereal cases</b>. Initial cost is <b>$8,760</b>; warehouse use is 700 cases; initial budget remaining is $3,240.')
figure('food_decisions')
caption('Food bank!C28:F32. Initial and scenario emergency decisions are shown in cases.')
table([['Scenario','Vegetables','Rice','Cereal','Emergency cost'],[1,20,70,20,'$1,920'],[2,0,200,30,'$3,860'],[3,10,80,0,'$1,460']],[65,100,100,100,135])
text('Expected emergency cost = 0.40 x 1,920 + 0.35 x 3,860 + 0.25 x 1,460 = $2,484. Expected total cost = 8,760 + 2,484 = <b>$11,244</b>. Purchase the initial quantities above and use emergency funds according to the realized scenario.')
figure('food_constraints',460)
caption('Food bank!C36:F53. All scenario demands are met; budget and capacity are satisfied. Scenario total costs are $10,680, $12,620, and $10,220.')
caption('The LP optimum has whole-case decisions, so it is also feasible and optimal for the integer model. The earlier 210 / 250 / 240 purchase plan is an alternative optimum with the same $11,244 expected cost. Warehouse capacity is binding; the initial budget is not.')

page();caption('ADDITIONAL PRACTICE');title('Food bank: Excel Solver evidence')
text('These are genuine screenshots of the Excel Solver dialogs used on the completed workbook. Parameters show the objective, decisions, grouped constraints, nonnegativity setting, and Simplex LP method. Results confirm feasibility and optimality.')
side([img('solver_settings',250),para('Native Solver Parameters dialog.','SmallClean')],[img('solver_result',235),Spacer(1,15),para('Minimize G57.<br/>Changing cells: D29:F32.<br/>D36:D37 <= F36:F37.<br/>D41:D43 >= F41:F43.<br/>D46:D48 >= F46:F48.<br/>D51:D53 >= F51:F53.<br/>Nonnegative decisions.<br/>Simplex LP.','BodyClean')],[265,235])
sub('Saved objective calculation')
figure('food_objective')
caption('Food bank!C55:G60. G57 = D57 + SUMPRODUCT(D58:D60,C5:C7) = $11,244.00. Solver\'s optimal solution was kept and the workbook saved.')

def footer(canvas,doc):
 canvas.setStrokeColor(colors.HexColor('#CCCCCC'));canvas.line(56,40,556,40);canvas.setFont('Helvetica',8);canvas.setFillColor(colors.HexColor('#666666'));canvas.drawString(56,27,'95-760 | Recitation Week 6');canvas.drawRightString(556,27,str(doc.page))
report=p.parent/'W6 Solution Report.pdf'
SimpleDocTemplate(str(report),pagesize=(612,792),rightMargin=56,leftMargin=56,topMargin=45,bottomMargin=55,title='Week 6 Recitation Solutions',author='Mahir').build(story,onFirstPage=footer,onLaterPages=footer)
reader=PdfReader(report)
assert len(reader.pages)==10, f'Unexpected page count: {len(reader.pages)}'
assert '\u2014' not in '\n'.join(pg.extract_text() for pg in reader.pages)
writer=PdfWriter()
for pg in reader.pages[:5]: writer.add_page(pg)
writer.add_metadata({'/Title':'Week 6 Fishery Submission','/Author':'Mahir'})
with (p.parent/'W6 Submission.pdf').open('wb') as stream: writer.write(stream)
print('Full report: 10 pages. Required submission: 5 pages. No em dashes.')

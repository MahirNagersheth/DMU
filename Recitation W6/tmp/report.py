import sys,json,math
sys.path.insert(0,'/private/tmp/w6-report-libs')
from pathlib import Path
import numpy as np
from scipy.stats import t
from reportlab.platypus import SimpleDocTemplate,Paragraph,Spacer,Table,TableStyle,PageBreak,Image
from reportlab.lib.styles import getSampleStyleSheet,ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
p=Path(__file__).parent; d=json.loads((p/'results.json').read_text()); out=p.parent/'W6 Solution Report.pdf'
styles=getSampleStyleSheet()
styles.add(ParagraphStyle(name='TitleClean',fontName='Helvetica-Bold',fontSize=24,leading=29,spaceAfter=18))
styles.add(ParagraphStyle(name='HeadingClean',fontName='Helvetica-Bold',fontSize=14,leading=19,spaceAfter=12))
styles.add(ParagraphStyle(name='BodyClean',fontName='Helvetica',fontSize=10,leading=15,spaceAfter=10))
styles.add(ParagraphStyle(name='SmallClean',fontName='Helvetica',fontSize=8,leading=12,spaceAfter=8,textColor=colors.HexColor('#555555')))
story=[]
def text(s,style='BodyClean'): story.append(Paragraph(s,styles[style]))
def title(s): text(s,'HeadingClean')
def table(rows,widths=None):
 rows=[[Paragraph(str(v),styles['SmallClean']) for v in row] for row in rows]
 tb=Table(rows,colWidths=widths,repeatRows=1,hAlign='LEFT'); tb.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.HexColor('#E9E9E9')),('LINEBELOW',(0,0),(-1,0),.6,colors.HexColor('#777777')),('LINEBELOW',(0,-1),(-1,-1),.5,colors.HexColor('#BBBBBB')),('TOPPADDING',(0,0),(-1,-1),7),('BOTTOMPADDING',(0,0),(-1,-1),5),('VALIGN',(0,0),(-1,-1),'TOP')])); story.append(tb); story.append(Spacer(1,14))
def money(x): return f'${x:,.2f}'
def summary(s): table([['Samples','Mean profit','Sample SD','95% CI for mean'],[s['n'],money(s['mean']),money(s['sd']),f"{money(s['lower'])} to {money(s['upper'])}"]],[50,95,95,260])
def page(): story.append(PageBreak())
def chart(name,x,ys,labels,xlabel,ylabel):
 fig,ax=plt.subplots(figsize=(7.2,3.1));
 for i,(y,l) in enumerate(zip(ys,labels)): ax.plot(x,y,label=l,color=['#111111','#999999','#999999'][i%3],lw=1.4,ls='-' if i==0 else '--')
 ax.set_xlabel(xlabel); ax.set_ylabel(ylabel); ax.spines[['top','right']].set_visible(False); ax.grid(axis='y',alpha=.15); ax.legend(frameon=False,fontsize=8); fig.tight_layout(); fn=p/(name+'.png'); fig.savefig(fn,dpi=180); plt.close(fig); story.append(Image(str(fn),width=500,height=215))
text('WEEK 6','SmallClean'); text('Recitation solutions','TitleClean')
text('Decision Making Under Uncertainty | 95-760','SmallClean')
text('Prepared from RS W6.pdf and Recitation W6.xlsx. All submission and additional practice questions are addressed. Dollar amounts are per simulated day or flight unless otherwise stated.')
table([['Problem','Result'],['Fishery, 70 days',f"Mean {money(d['fish70_summary']['mean'])}; 95% CI {money(d['fish70_summary']['lower'])} to {money(d['fish70_summary']['upper'])}."],['Fishery, 500 days',f"Mean {money(d['fish500_summary']['mean'])}; exact expected profit $1,826.00."],['Fishing quantity','Q = 6,000 fish is best in the stated 2,000 to 6,000 grid under fixed daily cost.'],['Airline','Offer 20 tickets. Exact expected flight profit is $2,767.11.'],['Food bank','Buy 210 vegetable cases, 250 rice cases, and 240 cereal cases. Expected total cost: $11,244.00.']],[120,380])
text('Method and evidence','HeadingClean')
text('Simulations use reproducible independent uniform draws generated with NumPy seed 76006. Price and demand are assumed independent. Confidence intervals use Student t critical values and sample standard deviation. Fixed random inputs allow fair comparisons across decisions.')
text('The numerical food-bank optimization was solved with SciPy HiGHS. Excel Solver execution and screenshots are not yet available. Excel-ready settings appear in the food-bank section. Do not treat the numerical solution as evidence that Excel Solver was run.','SmallClean')
page(); title('1. Fishery: sampling and 70-day simulation')
text('<b>(a) Sampling.</b> Generate 15 observations per distribution. Let U be a uniform draw strictly between 0 and 1. The following formulas map U to the required distributions. Separate uniform draws should be used for independent samples; using one U across columns is acceptable only for marginal sampling demonstrations.')
table([['Distribution','Excel formula'],['Uniform (0,1)','=RAND()'],['Discrete, probabilities 0.2, 0.1, 0.5, 0.1, 0.1','=LOOKUP(U,$E$3:$E$7,$B$3:$B$7)'],['Binomial (15,0.7)','=BINOM.INV(15,0.7,U)'],['Uniform (5,9)','=5+(9-5)*U'],['Normal (5,2)','=NORM.INV(U,5,2)'],['Exponential (rate 0.4)','=-LN(1-U)/0.4']],[215,285])
text('Normal (5,2) is interpreted as mean 5 and standard deviation 2. The exponential parameter is a rate, so its mean is 1/0.4 = 2.5.')
text('<b>(b) Fishery operations.</b> Price P ~ Normal(3.65,0.20). Demand takes values 0 through 6,000 with the probabilities in the source. Sold = MIN(3500,Demand). Revenue = Price x Sold. Profit = Revenue - 10000.')
summary(d['fish70_summary'])
text('The 95% confidence interval is mean +/- T.INV.2T(0.05,69) x STDEV.S(profits) / SQRT(70). It estimates the expected profit, rather than the range of profits on individual days.')
text('Exact check: E[sold] = 3,240 fish. Independence implies E[profit] = 3.65 x 3,240 - 10,000 = $1,826.00. This lies inside the 70-day confidence interval.')
page(); title('2. Fishery: sample-size analysis and quantity')
text('<b>(c) N analysis.</b> Simulate 500 days. On day n, calculate statistics using only observations 1 through n. In row r, use AVERAGE($O$4:Or), STDEV.S($O$4:Or), and mean +/- T.INV.2T(0.05,n-1) x SD / SQRT(n). For n = 1, SD and confidence limits are undefined; leave them blank.')
summary(d['fish500_summary'])
a=np.array(d['fish500']['profit']); ns=np.arange(2,501); means=np.array([a[:n].mean() for n in ns]); sd=np.array([a[:n].std(ddof=1) for n in ns]); hw=t.ppf(.975,ns-1)*sd/np.sqrt(ns)
chart('n_analysis',ns,[means,means-hw,means+hw],['Running mean','Lower 95% CI','Upper 95% CI'],'Days simulated','Profit ($)')
text('More samples reduce sampling error and generally narrow the confidence interval. The running mean need not move monotonically toward the exact mean. The final mean of $1,822.20 is close to the exact value of $1,826.00.')
text('<b>(d) Analysis on Q.</b> Keep the same price and demand draws for every Q. In the one-input Data Table, the top output formula links to mean profit and the column input cell is R4. Test Q = 2,000, 2,100, ..., 6,000. The template uses n = 400; a completed analysis may instead use all 1,000 provided day rows if n and its summary references are updated consistently.')
text(f"The 1,000-day comparison gives mean profit {money(d['Q_mean'][-1])} at Q = 6,000. The exact expected profit at Q = 6,000 is 3.65 x 4,340 - 10,000 = $5,841.00. With fixed $10,000 cost and no extra cost of Q, profit cannot decrease as Q increases. Any Q at least 6,000 achieves the maximum possible sales. This recommendation depends on the fixed-cost assumption.")
page(); title('3. Airline: simulation and booking decision')
text('<b>(a) Sell up to 22 tickets.</b> Demand is discrete from 14 to 25. Tickets sold = MIN(22,Demand). Conditional on tickets sold B, show-ups follow Binomial(B,0.9). Profit = 150 x B - 500 x MAX(show-ups - 19,0). No additional operating cost is provided, so this is ticket revenue less denied-boarding compensation.')
summary(d['air100_summary'])
text('The exact expected profit at a booking limit of 22 is $2,733.17, calculated by summing over demand and the conditional binomial show-up distribution. It lies within the simulation interval.')
text('<b>(b) Recommended sample size.</b> A 100-flight simulation has a confidence half-width of about $71.88 in this run. It is useful for a rough estimate, but too imprecise to distinguish the close booking alternatives. Define a target half-width of $10. Using the exact SD of $340.27 gives n >= (1.96 x 340.27 / 10)^2, rounded up to 4,448. The pilot SD gives 5,042. Recommend 5,100 flights for a practical margin. The 5,100-flight run below has half-width $9.50.')
summary(d['air5000_summary'])
text('<b>(c) Booking-limit comparison.</b> Use common random numbers across alternatives to reduce comparison noise. The exact expectation validates the recommended choice even though the mean profit differences are small.')
table([['Booking limit','Simulation mean, n = 5,100','Exact expected profit']]+[[cap,money(sim['mean']),money(ex)] for cap,sim,ex in zip(d['air_caps'],d['air_sim'],d['air_exact'])],[95,220,185])
text('Recommend offering 20 tickets for the 19-seat flight. Exact expected profit is $2,767.11, compared with $2,758.69 at 21 and $2,733.17 at 22. Limits below 19 forgo profitable sales without avoiding any denied-boarding cost. Limits above 25 are equivalent to 25 because demand is capped at 25.')
page(); title('4. Food bank: two-stage stochastic model')
text('<b>(a) Sets and uncertainty.</b> Food types j are vegetables, rice, and cereal. Organizations i = 1,2,3,4. Scenarios s = 1,2,3 have probabilities 0.40, 0.35, and 0.25. Scenario s jointly determines donations a(s,j) and organization demand d(s,i,j). A single first-stage purchase decision is shared across all scenarios.')
table([['Parameter','Vegetables','Rice','Cereal'],['Initial cost per case',12,10,15],['Emergency cost per case',18,16,22],['Scenario 1 aggregate demand',400,400,340],['Scenario 2 aggregate demand',480,480,420],['Scenario 3 aggregate demand',340,340,290],['Scenario 1 donations',100,150,80],['Scenario 2 donations',200,100,150],['Scenario 3 donations',50,80,50]],[220,94,93,93])
text('<b>Decision variables.</b> x(j) >= 0 is cases bought before donations are known. After observing scenario s, y(s,i,j) >= 0 is regular inventory distributed to organization i, and z(s,i,j) >= 0 is emergency-purchased food supplied to that organization. Case counts may be constrained to integers. The LP optimum here is already integral.')
text('<b>Objective.</b> Minimize SUM_j c(j)x(j) + SUM_s p(s) SUM_i SUM_j e(j)z(s,i,j).')
text('<b>First-stage constraints.</b> 12x(vegetables) + 10x(rice) + 15x(cereal) <= 12000. SUM_j x(j) <= 700. These limits apply to initial purchases. Donations and emergency purchases are not subject to these initial-purchase limits.')
text('<b>Second-stage constraints.</b> For every scenario, organization, and food type, y(s,i,j) + z(s,i,j) = d(s,i,j). For every scenario and food, SUM_i y(s,i,j) <= x(j) + a(s,j). All variables are nonnegative. There are no shared emergency-budget limits, since emergency funds are separate.')
text('An equivalent compact model uses aggregate emergency purchases E(s,j) >= 0, with x(j) + a(s,j) + E(s,j) >= SUM_i d(s,i,j). Because all organizations have the same food-specific emergency cost and no allocation restrictions, aggregation preserves the optimal value. The compact model has 12 variables and is convenient for Excel Solver.')
page(); title('5. Food bank: optimal plan and Solver settings')
text('<b>(b) Optimal solution.</b> The compact LP was solved using SciPy HiGHS. Its solution satisfies all scenario demand, budget, and warehouse constraints. The optimal initial purchase fills all 700 cases of warehouse space. The initial budget has $3,380 remaining.')
table([['Food','Initial cases','Initial cost'],['Canned vegetables',210,'$2,520'],['Rice',250,'$2,500'],['Cereal',240,'$3,600'],['Total',700,'$8,620']],[220,130,150])
table([['Scenario','Probability','Vegetables emergency','Rice emergency','Cereal emergency','Emergency cost'],[1,'0.40',90,0,20,'$2,060'],[2,'0.35',70,130,30,'$4,000'],[3,'0.25',80,10,0,'$1,600']],[55,65,100,80,95,105])
text('Expected emergency cost = 0.40 x 2,060 + 0.35 x 4,000 + 0.25 x 1,600 = $2,624. Expected total cost = 8,620 + 2,624 = <b>$11,244</b>. Scenario total costs are $10,680, $12,620, and $10,220.')
text('<b>Excel Solver configuration.</b> Set the objective cell to expected total cost and choose Min. Change the three initial-purchase cells and the nine scenario emergency-purchase cells. Add initial spending <= 12000, initial cases <= 700, and available food >= aggregate demand in all nine scenario-food combinations. Select Simplex LP and make unconstrained variables nonnegative. If indivisible cases are required, add integer constraints to the 12 decision variables.')
text('<b>(c) Recommendation.</b> Purchase 210 cases of vegetables, 250 cases of rice, and 240 cases of cereal before the month begins. Reserve emergency funds according to the scenario table. Every organization can be fully served in every scenario. Warehouse capacity, rather than the initial budget, is the binding initial resource.')
text('No-purchase benchmark: expected emergency cost is $15,684. The recommended plan saves $4,440 in expected total cost. A further warehouse case is locally worth $6 in expected total-cost savings, until the next piecewise-linear threshold changes the marginal benefit.')
text('Evidence limitation: this report contains the solved mathematical model and reproducible numerical results. It does not yet contain native Excel Solver screenshots or screenshots of a completed Excel workbook. Those require Excel execution and workbook completion.','SmallClean')
page(); title('Appendix: 15 observations from each distribution')
from scipy.stats import norm,binom
rg=np.random.default_rng(76006); u=rg.random((15,6))
samples=np.column_stack([u[:,0],np.searchsorted(np.cumsum([.2,.1,.5,.1,.1]),u[:,1]),binom.ppf(u[:,2],15,.7),5+4*u[:,3],norm.ppf(u[:,4],5,2),-np.log(1-u[:,5])/.4])
text('Independent draws are used across the six columns. The values below complete part (a) numerically. They are a reproducible sampling realization; a fresh Excel RAND() run will produce different valid observations.')
table([['Obs.','U(0,1)','Discrete','Bin(15,.7)','U(5,9)','N(5,2)','Exp(.4)']]+[[i+1,f'{r[0]:.4f}',int(r[1]),int(r[2]),f'{r[3]:.4f}',f'{r[4]:.4f}',f'{r[5]:.4f}'] for i,r in enumerate(samples)],[35,73,70,87,78,78,79])
text('The discrete outcomes are 0, 1, 2, 3, and 4 with probabilities 0.20, 0.10, 0.50, 0.10, and 0.10. Binomial outcomes are integer counts. The normal distribution uses standard deviation 2; the exponential distribution uses rate 0.4.')
def footer(canvas,doc):
 canvas.setStrokeColor(colors.HexColor('#CCCCCC'));canvas.line(48,39,564,39);canvas.setFont('Helvetica',8);canvas.setFillColor(colors.HexColor('#666666'));canvas.drawString(48,26,'95-760 | Recitation Week 6');canvas.drawRightString(564,26,str(doc.page))
SimpleDocTemplate(str(out),pagesize=(612,792),rightMargin=56,leftMargin=56,topMargin=48,bottomMargin=54).build(story,onFirstPage=footer,onLaterPages=footer)
print(out)

from pathlib import Path
import json
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Border, Side, Alignment
from openpyxl.utils import get_column_letter as col
P=Path(__file__).parent; R=json.loads((P/'results.json').read_text())
w=Workbook(); w.remove(w.active)
def base(name,last,wide=False):
 s=w.create_sheet(name); s.sheet_view.showGridLines=False
 for c in range(1,14): s.column_dimensions[col(c)].width=14 if wide else 17
 s.column_dimensions['A'].width=25 if not wide else 15
 for r in range(1,last+1): s.row_dimensions[r].height=21
 s.freeze_panes='B5'; s.sheet_properties.pageSetUpPr.fitToPage=True
 s.page_setup.orientation='landscape'; s.page_setup.paperSize=s.PAPERSIZE_A4
 s.page_setup.fitToWidth=1; s.page_setup.fitToHeight=0
 s.sheet_view.zoomScale=85
 return s
def row(s,r,vals):
 for c,v in enumerate(vals,1): s.cell(r,c,v)
def title(s,r,text,end=9):
 s.merge_cells(start_row=r,start_column=1,end_row=r,end_column=end);s.cell(r,1,text)
 s.cell(r,1).font=Font(name='Calibri',size=12,bold=True);s.row_dimensions[r].height=25
def note(s,r,text,end=9):
 s.merge_cells(start_row=r,start_column=1,end_row=r,end_column=end);s.cell(r,1,text)
 s.cell(r,1).alignment=Alignment(wrap_text=True,vertical='center');s.row_dimensions[r].height=29
def head(s,r,vals):
 row(s,r,vals);s.row_dimensions[r].height=32
 for c in range(1,len(vals)+1):
  x=s.cell(r,c);x.font=Font(name='Calibri',size=11,bold=True);x.fill=PatternFill('solid',fgColor='F2F2F2');x.alignment=Alignment(wrap_text=True,vertical='center')
def total(s,r,label,formula):
 s.cell(r,1,label);s.cell(r,2,formula)
 for c in [1,2]:s.cell(r,c).font=Font(name='Calibri',size=11,bold=True)
 s.cell(r,2).number_format='$#,##0'
s=base('Problem 1',93)
title(s,1,'Homework 3 | Problem 1: Factory decisions')
note(s,2,'Name(s): [enter name(s)]    |    Excel uploader: [enter name]')
head(s,4,['Facility','Construction ($)','Production ($/car)','Min production','Max capacity'])
for i in range(4): row(s,5+i,[f'Plant {i+1}',R['F'][i],R['C'][i],R['L'][i],R['U'][i]])
head(s,11,['Transport ($/car)','Pittsburgh','Chicago','New York','Washington, D.C.','Boston'])
for i in range(4):row(s,12+i,[f'Plant {i+1}']+R['T'][i])
row(s,16,['Demand']+R['D']);row(s,17,['Total demand','=SUM(B16:F16)'])
title(s,20,'(a)-(c) Construction cost only')
head(s,21,['Facility','Build (binary)','Capacity','Fixed cost ($)'])
for i in range(4):
 r=22+i;p=5+i;row(s,r,[f'Plant {i+1}',[1,0,1,0][i],f'=B{r}*E{p}',f'=B{r}*B{p}'])
total(s,27,'Construction cost','=SUM(D22:D25)');row(s,28,['Total capacity','=SUM(C22:C25)','>=','=B17']);row(s,29,['Capacity slack','=B28-D28'])
note(s,31,'Solver: Min $B$27; change $B$22:$B$25; $B$28 >= $D$28; $B$22:$B$25 binary.')
note(s,32,'Simplex LP; nonnegative variables; integer optimality 0%. Saved Solver model: M20:M45.')
note(s,33,'Formulas: C22=B22*E5; D22=B22*B5, copied down. B27=SUM(D22:D25). B28=SUM(C22:C25).')
title(s,36,'(d)-(f) Construction plus production costs')
head(s,37,['Facility','Build (binary)','Cars (integer)','Min if built','Max if built','Fixed cost ($)','Production ($)'])
for i in range(4):
 r=38+i;p=5+i;row(s,r,[f'Plant {i+1}',R['p1d']['x'][i],R['p1d']['x'][i+4],f'=B{r}*D{p}',f'=B{r}*E{p}',f'=B{r}*B{p}',f'=C{r}*C{p}'])
total(s,43,'Total cost','=SUM(F38:G41)');total(s,44,'Construction cost','=SUM(F38:F41)');total(s,45,'Production cost','=SUM(G38:G41)')
row(s,46,['Total cars','=SUM(C38:C41)','>=','=B17'])
note(s,48,'Solver: Min $B$43; change $B$38:$C$41; $B$46 >= $D$46; $B$38:$B$41 binary; $C$38:$C$41 integer.')
note(s,49,'Linking: $C$38:$C$41 >= $D$38:$D$41; $C$38:$C$41 <= $E$38:$E$41. Nonnegative variables.')
note(s,50,'Simplex LP; integer optimality 0%. Saved Solver model: M48:M78.')
note(s,51,'Formulas: D38=B38*D5; E38=B38*E5; F38=B38*B5; G38=C38*C5, copied down. B43=SUM(F38:G41).')
title(s,55,'(g)-(i) Construction, production and transportation costs')
head(s,56,['Facility','Build (binary)','Pittsburgh','Chicago','New York','Washington, D.C.','Boston','Production','Min if built','Max if built'])
for i in range(4):
 r=57+i;p=5+i;row(s,r,[f'Plant {i+1}',R['p1g']['x'][i]]+R['p1g']['x'][4+5*i:9+5*i]+[f'=SUM(C{r}:G{r})',f'=B{r}*D{p}',f'=B{r}*E{p}'])
row(s,62,['Delivered',None]+[f'=SUM({col(c)}57:{col(c)}60)' for c in range(3,8)])
row(s,63,['Demand',None]+[f'={col(c)}16' for c in range(2,7)])
row(s,64,['Demand residual',None]+[f'={col(c)}62-{col(c)}63' for c in range(3,8)])
total(s,66,'Total cost','=SUM(B67:B69)');total(s,67,'Construction cost','=SUMPRODUCT(B57:B60,B5:B8)');total(s,68,'Production cost','=SUMPRODUCT(H57:H60,C5:C8)');total(s,69,'Transportation cost','=SUMPRODUCT(C57:G60,B12:F15)')
note(s,71,'Solver: Min $B$66; change $B$57:$G$60; $B$57:$B$60 binary; $C$57:$G$60 integer.',10)
note(s,72,'Constraints: $H$57:$H$60 >= $I$57:$I$60; $H$57:$H$60 <= $J$57:$J$60; $C$62:$G$62 = $C$63:$G$63.',10)
note(s,73,'Simplex LP; nonnegative variables; integer optimality 0%. Saved Solver model: M82:M115.',10)
note(s,74,'Formulas: H57=SUM(C57:G57); I57=B57*D5; J57=B57*E5, copied down. City totals use SUM of shipments.',10)
note(s,75,'B67=SUMPRODUCT(B57:B60,B5:B8); B68=SUMPRODUCT(H57:H60,C5:C8); B69=SUMPRODUCT(C57:G60,B12:F15).',10)
note(s,78,'Source: HW3.pdf, Problem 1, pages 1-2. Costs in dollars; production and shipments in whole cars.',10)
s.print_area='A1:J78'
for r in range(5,9):
 for c in [2,3]:s.cell(r,c).number_format='$#,##0'
for a in ['D22:D25','F38:G41']:
 for cells in s[a]:
  for x in cells:x.number_format='$#,##0'
t=base('Problem 2',77,True)
title(t,1,'Homework 3 | Problem 2: Match scheduling',12)
note(t,2,'Name(s): [enter name(s)]    |    C: Colombia; NZ: New Zealand; G: Germany; P: Philippines',12)
matches=['C-G','C-P','NZ-G','NZ-P','C-NZ','G-P']
title(t,4,'Input: Visibility scores by day',12);head(t,5,['Day']+matches)
for i,v in enumerate(R['V']):row(t,6+i,[i+1]+v)
title(t,22,'(a)-(c) Optimal schedule: 1 means the match is played on that day',12)
head(t,23,['Day']+matches+['Games','Colombia','New Zealand','Germany','Philippines'])
teams=[[2,3,6],[4,5,6],[2,4,7],[3,5,7]]
for i in range(14):
 r=24+i; row(t,r,[i+1]+R['p2']['x'][6*i:6*i+6]+[f'=SUM(B{r}:G{r})']+['='+'+'.join(f'{col(c)}{r}' for c in ms) for ms in teams])
row(t,39,['Match count']+[f'=SUM({col(c)}24:{col(c)}37)' for c in range(2,8)])
row(t,40,['Match day']+[f'=SUMPRODUCT($A$24:$A$37,{col(c)}24:{col(c)}37)' for c in range(2,8)])
row(t,41,['Visibility']+[f'=SUMPRODUCT({col(c)}6:{col(c)}19,{col(c)}24:{col(c)}37)' for c in range(2,8)])
row(t,43,['Total visibility','=SUMPRODUCT(B6:G19,B24:G37)']);t['B43'].font=Font(name='Calibri',size=11,bold=True)
note(t,45,'Solver: Max $B$43; change $B$24:$G$37; $B$24:$G$37 binary; $B$39:$G$39 = 1.',12)
note(t,46,'Daily games: $H$24:$H$37 <= 2. Team limits: $I$24:$L$37 <= 1. Final day: $H$37 = 2.',12)
note(t,47,'Simplex LP; nonnegative variables; integer optimality 0%. Saved Solver model: N5:N40.',12)
note(t,48,'The two day-14 matches must share the same kickoff time. The model chooses days, not kickoff times.',12)
note(t,50,'Formulas: H24=SUM(B24:G24); I24=B24+C24+F24; J24=D24+E24+F24; K24=B24+D24+G24; L24=C24+E24+G24.',12)
note(t,51,'Copy daily formulas through row 37. B39=SUM(B24:B37); B40=SUMPRODUCT($A$24:$A$37,B24:B37), copied across.',12)
note(t,52,'B41=SUMPRODUCT(B6:B19,B24:B37), copied across. B43=SUMPRODUCT(B6:G19,B24:G37).',12)
title(t,55,'(d) Additional rest constraint',12)
note(t,56,'For each team and each three-day window, the total number of its matches must be <= 1.',12)
note(t,57,'Mathematically: SUM over matches involving team t and days k,k+1,k+2 of x[m,d] <= 1; k = 1,...,12.',12)
note(t,58,'This ensures at least two full days of rest. Part (d) requests a formulation; the base solution above is unchanged.',12)
head(t,60,['Window start','Colombia','New Zealand','Germany','Philippines'])
for i in range(12):row(t,61+i,[i+1]+[f'=SUM({col(c)}{24+i}:{col(c)}{26+i})' for c in range(9,13)])
note(t,74,'To solve the rest variant, add $B$61:$E$72 <= 1. Formulas: B61=SUM(I24:I26), copied across and down.',12)
note(t,76,'Source: HW3.pdf, Problem 2, pages 2-3. Match numbers are identifiers, not a required chronological order.',12)
t.print_area='A1:L76'
for sh in w:
 for cells in sh:
  for x in cells:
   if x.value is not None:
    if x.font.name is None:x.font=Font(name='Calibri',size=11)
    if x.alignment.vertical is None:x.alignment=Alignment(vertical='center')
    if isinstance(x.value,(int,float)) and x.number_format=='General':x.number_format='#,##0'
 sh.sheet_properties.outlinePr.summaryRight=False
 for c in (['M'] if sh==s else ['N']):sh.column_dimensions[c].hidden=True
w.save(P.parent/'HW3_Solved.xlsx')
print('Workbook created')

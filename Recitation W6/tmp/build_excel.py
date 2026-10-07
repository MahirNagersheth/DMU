"""Generate native Excel AppleScript commands; no workbook authoring library."""
import json
from pathlib import Path
import numpy as np
p=Path(__file__).parent
d=json.loads((p/'results.json').read_text())
def a(v):
 if isinstance(v,str): return '"'+v.replace('\\','\\\\').replace('"','\\"')+'"'
 if isinstance(v,(list,tuple,np.ndarray)): return '{'+','.join(a(x) for x in v)+'}'
 return str(float(v)) if isinstance(v,(float,np.floating)) else str(v)
def script(name,lines):
 (p/(name+'.applescript')).write_text('tell application "Microsoft Excel"\nset display alerts to false\nset calculation to calculation manual\n'+ '\n'.join(lines)+'\nset calculation to calculation automatic\ncalculate full\nsave active workbook\nend tell\n')
def activate(name): return f'activate object worksheet {a(name)} of active workbook'
def vals(r,v): return f'set value of range {a(r)} of active sheet to {a(v)}'
def formula(r,f): return f'set formula of range {a(r)} of active sheet to {a(f)}'
def fill(r): return f'fill down range {a(r)} of active sheet'
def fmt(r,f): return f'set number format of range {a(r)} of active sheet to {a(f)}'
base=[]
for name,r in [('Sampling','B2:L17'),('Fishery operations','B2:Z73'),('N analysis','B2:AH520'),('Analysis on Q','B2:AF1003'),('Airline (a)','B2:S103'),('Airline (b)','B2:AB5103'),('Airline (c)','B2:AB5103'),('Food bank','B2:K60')]:
 base += [activate(name),f'set color of font object of range {a(r)} of active sheet to {{0,0,0}}',f'set name of font object of range {a(r)} of active sheet to "Arial"',f'set color of interior object of range {a(r)} of active sheet to {{255,255,255}}','set display gridlines of active window to false','set scroll row of active window to 1','set scroll column of active window to 1']
 for rr in (['B2:L2'] if name=='Sampling' else ['B2:K2'] if name=='Food bank' else ['B2:T3']): base += [f'set color of interior object of range {a(rr)} of active sheet to {{232,232,232}}']
base+=[activate('Sampling')]
u=np.random.default_rng(76006).random((15,6))
# Store six independent uniform streams in N:S, one for each distribution.
base += [vals('N2:S2',[['Uniform draw 1','Uniform draw 2','Uniform draw 3','Uniform draw 4','Uniform draw 5','Uniform draw 6']]),vals('N3:S17',u.tolist()),formula('G3:L3',[['=N3','=LOOKUP(O3,$E$3:$E$7,$B$3:$B$7)','=BINOM.INV(15,0.7,P3)','=5+4*Q3','=NORM.INV(R3,5,2)','=-LN(1-S3)/0.4']]),fill('G3:L17'),fmt('G3:G17','0.0000'),fmt('H3:I17','0'),fmt('J3:L17','0.0000')]
script('01_style_sampling',base)
for name,key,n in [('Fishery operations','fish70',70),('N analysis','fish500',500),('Analysis on Q','fishQ',1000)]:
 lines=[activate(name),vals(f'H4:H{n+3}',[[x[0]] for x in d[key]['u']]),vals(f'J4:J{n+3}',[[x[1]] for x in d[key]['u']])]
 lines += [fmt(f'H4:H{n+3}','0.0000'),fmt(f'J4:J{n+3}','0.0000'),fmt(f'I4:I{n+3}','0.0000'),fmt(f'M4:O{n+3}','"$"#,##0.00;("$"#,##0.00)')]
 if name=='Fishery operations':
  lines += [vals('Z4:Z5',[[''],['']]),formula('Y4','=AVERAGE(O4:O73)'),formula('Y5','=STDEV.S(O4:O73)'),formula('Y8','=Y4-T.INV.2T(0.05,69)*Y5/SQRT(70)'),formula('Y9','=Y4+T.INV.2T(0.05,69)*Y5/SQRT(70)'),fmt('Y4:Y9','"$"#,##0.00'),vals('X8:X9',[['Lower 95% CI'],['Upper 95% CI']]),'set column width of range "X:X" of active sheet to 22','set column width of range "Y:Y" of active sheet to 18']
 if name=='N analysis':
  lines += [vals('S3:T3',[['Lower 95% CI','Upper 95% CI']]),formula('Q4','=AVERAGE($O$4:O4)'),fill('Q4:Q503'),formula('R5','=STDEV.S($O$4:O5)'),fill('R5:R503'),formula('S5','=Q5-T.INV.2T(0.05,P5-1)*R5/SQRT(P5)'),fill('S5:S503'),formula('T5','=Q5+T.INV.2T(0.05,P5-1)*R5/SQRT(P5)'),fill('T5:T503'),vals('X32:X33',[[''],['']]),fmt('Q4:T503','"$"#,##0.00'), 'set column width of range "Q:T" of active sheet to 17']
 if name=='Analysis on Q':
  lines += [vals('R4',[[4000]]),formula('N4','=3000+2*$R$4'),fill('N4:N1003'),formula('R7','=AVERAGE(O4:O403)'),formula('R8','=STDEV.S(O4:O403)'),formula('R9','=R7-T.INV.2T(0.05,R11-1)*R8/SQRT(R11)'),formula('R10','=R7+T.INV.2T(0.05,R11-1)*R8/SQRT(R11)'),vals('Q9:Q10',[['Lower 95% CI'],['Upper 95% CI']]),vals('Q13:R14',[['Fixed cost',3000],['Cost per fish',2]]),formula('N4','=$R$13+$R$14*$R$4'),fill('N4:N1003'),formula('U3','=R7'),'data table range "T3:U44" of active sheet column input range "R4" of active sheet',fmt('R7:R10','"$"#,##0.00'),fmt('U4:U44','"$"#,##0.00'),'set column width of range "Q:Q" of active sheet to 22','set column width of range "R:R" of active sheet to 18','set column width of range "U:U" of active sheet to 18']
 script('02_'+name.replace(' ','_'),lines)
for name,key,n in [('Airline (a)','air100',100),('Airline (b)','air5000',5100),('Airline (c)','air5000',5100)]:
 lines=[activate(name)]
 if n>100:
  lines += [fill('B4:K5103'),formula('B5','=B4+1'),fill('B5:B5103')]
 lines += [vals(f'C4:C{n+3}',[[x[0]] for x in d[key]['u']]),vals(f'G4:G{n+3}',[[1-x[1]] for x in d[key]['u']]),fmt(f'C4:C{n+3}','0.0000'),fmt(f'G4:G{n+3}','0.0000')]
 if name=='Airline (a)':
  lines += [vals('R8:R12',[['Summary'],['n'],['Mean'],['Sample SD'],['Lower 95% CI']]),vals('R13',[['Upper 95% CI']]),formula('S9','=COUNT(K4:K103)'),formula('S10','=AVERAGE(K4:K103)'),formula('S11','=STDEV.S(K4:K103)'),formula('S12','=S10-T.INV.2T(0.05,S9-1)*S11/SQRT(S9)'),formula('S13','=S10+T.INV.2T(0.05,S9-1)*S11/SQRT(S9)'),fmt('S10:S13','"$"#,##0.00')]
 if name=='Airline (b)':
  lines += [vals('O3:P3',[['Lower 95% CI','Upper 95% CI']]),formula('L4','=B4'),fill('L4:L5103'),formula('M4','=AVERAGE($K$4:K4)'),fill('M4:M5103'),formula('N5','=STDEV.S($K$4:K5)'),fill('N5:N5103'),formula('O5','=M5-T.INV.2T(0.05,L5-1)*N5/SQRT(L5)'),fill('O5:O5103'),formula('P5','=M5+T.INV.2T(0.05,L5-1)*N5/SQRT(L5)'),fill('P5:P5103'),fmt('M4:P5103','"$"#,##0.00')]
 if name=='Airline (c)':
  lines += [formula('S8','=AVERAGE(K4:K5103)'),vals('R10:S11',[['Samples',5100],['Bookings','Mean profit']]),vals('R12', [['Bookings']]),formula('S12','=S8'),vals('R13:R19',[[x] for x in range(19,26)]),'data table range "R12:S19" of active sheet column input range "S2" of active sheet',fmt('S8','"$"#,##0.00'),fmt('S13:S19','"$"#,##0.00'),'set source data chart of chart object 1 of active sheet source range "R12:S19" of active sheet plot by columns']
 lines += ['set column width of range "R:R" of active sheet to 21','set column width of range "S:S" of active sheet to 18']
 script('03_'+name.replace(' ','_').replace('(','').replace(')',''),lines)
script('04_food',[activate('Food bank'),vals('D29:F32',[d['food']['x']]+d['food']['e']),fmt('D57:D60','"$"#,##0.00'),fmt('G57','"$"#,##0.00')])
print('Generated native Excel scripts')

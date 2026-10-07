from pathlib import Path
import json,numpy as np,openpyxl
from zipfile import ZipFile
P=Path(__file__).parent;R=json.loads((P/'results.json').read_text());W=openpyxl.load_workbook(P.parent/'HW3_Solved.xlsx',data_only=True)
s=W['Problem 1'];t=W['Problem 2'];F=np.array(R['F']);C=np.array(R['C']);L=np.array(R['L']);U=np.array(R['U']);D=np.array(R['D'])
y=np.array([s.cell(r,2).value for r in range(22,26)])
assert np.isin(y,[0,1]).all() and U@y>=D.sum() and F@y==s['B27'].value==4500000
y=np.array([s.cell(r,2).value for r in range(38,42)]);q=np.array([s.cell(r,3).value for r in range(38,42)])
assert np.isin(y,[0,1]).all() and np.equal(q,np.round(q)).all() and np.all(q>=L*y) and np.all(q<=U*y) and q.sum()>=12000
assert F@y+C@q==s['B43'].value==R['p1d']['objective']
y=np.array([s.cell(r,2).value for r in range(57,61)]);x=np.array([[s.cell(r,c).value for c in range(3,8)] for r in range(57,61)]);q=x.sum(axis=1)
assert np.isin(y,[0,1]).all() and np.all(x>=0) and np.equal(x,np.round(x)).all()
assert np.all(x.sum(axis=0)==D) and np.all(q>=L*y) and np.all(q<=U*y)
assert F@y+C@q+(x*np.array(R['T'])).sum()==s['B66'].value==R['p1g']['objective']
x=np.array([[t.cell(r,c).value for c in range(2,8)] for r in range(24,38)])
assert np.isin(x,[0,1]).all() and np.all(x.sum(axis=0)==1) and np.all(x.sum(axis=1)<=2) and x[-1].sum()==2
for matches in [[0,1,4],[2,3,4],[0,2,5],[1,3,5]]:assert np.all(x[:,matches].sum(axis=1)<=1)
assert (x*np.array(R['V'])).sum()==t['B43'].value==-R['p2']['objective']
assert not [(sh.title,c.coordinate) for sh in W for row in sh for c in row if c.data_type=='e']
for f in ['HW3_Solved.xlsx','HW3_Solved.docx']:
 with ZipFile(P.parent/f) as z:
  assert not any('\u2014' in z.read(n).decode('utf-8') for n in z.namelist() if n.endswith('.xml'))
with ZipFile(P.parent/'HW3_Solved.docx') as z:assert len([n for n in z.namelist() if n.startswith('word/media/')])==12
print('PASS: all 4 optimal objectives, every model constraint, integrality, cached formulas, 12 embedded screenshots, and no em dashes.')

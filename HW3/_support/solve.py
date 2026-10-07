import json
from pathlib import Path
import numpy as np
from scipy.optimize import milp, Bounds, LinearConstraint
F=np.array([2100000,2800000,2400000,2700000]); C=np.array([380,165,155,170]); L=np.array([2000,3000,4000,2500]); U=np.array([5000,7000,8000,6000]); D=np.array([1000,3000,3000,1000,4000])
T=np.array([[18,35,50,30,20],[15,10,12,10,12],[40,50,30,35,25],[32,25,20,25,40]])
V=np.array([[185,170,183,168,178,175],[130,125,125,120,125,125],[110,120,115,125,115,120],[138,140,138,140,140,140],[175,170,182,177,177,175],[120,125,125,130,125,125],[110]*6,[144,142,142,140,142,142],[192,183,177,168,175,185],[130]*6,[120]*6,[156,153,153,150,153,153],[180,175,182,175,188,181],[150]*6])
teams=[[0,1,4],[2,3,4],[0,2,5],[1,3,5]]
def solve(c,upper,rows):
 A,lo,hi=zip(*rows)
 r=milp(c,integrality=np.ones(len(c)),bounds=Bounds(np.zeros(len(c)),upper),constraints=LinearConstraint(A,lo,hi),options={'mip_rel_gap':0})
 assert r.success,r.message
 return {'objective':float(r.fun),'x':np.rint(r.x).astype(int).tolist(),'message':r.message}
rows=[]
for i in range(4):
 a=np.zeros(8);a[i]=-L[i];a[i+4]=1;rows.append((a,0,np.inf))
 a=np.zeros(8);a[i]=-U[i];a[i+4]=1;rows.append((a,-np.inf,0))
rows.append((np.r_[np.zeros(4),np.ones(4)],12000,12000))
p1d=solve(np.r_[F,C],np.r_[np.ones(4),U],rows)
rows=[]
for i in range(4):
 a=np.zeros(24);a[i]=-L[i];a[4+5*i:9+5*i]=1;rows.append((a,0,np.inf))
 a=np.zeros(24);a[i]=-U[i];a[4+5*i:9+5*i]=1;rows.append((a,-np.inf,0))
for j in range(5):
 a=np.zeros(24);a[4+j::5]=1;rows.append((a,D[j],D[j]))
p1g=solve(np.r_[F,(C[:,None]+T).flatten()],np.r_[np.ones(4),np.full(20,np.inf)],rows)
rows=[]
for m in range(6):
 a=np.zeros((14,6));a[:,m]=1;rows.append((a.flatten(),1,1))
for day in range(14):
 a=np.zeros((14,6));a[day,:]=1;rows.append((a.flatten(),2 if day==13 else 0,2))
 for matches in teams:
  a=np.zeros((14,6));a[day,matches]=1;rows.append((a.flatten(),0,1))
p2=solve(-V.flatten(),np.ones(84),rows)
for day in range(12):
 for matches in teams:
  a=np.zeros((14,6));a[day:day+3,matches]=1;rows.append((a.flatten(),0,1))
p2rest=solve(-V.flatten(),np.ones(84),rows)
out={'F':F.tolist(),'C':C.tolist(),'L':L.tolist(),'U':U.tolist(),'D':D.tolist(),'T':T.tolist(),'V':V.tolist(),'p1d':p1d,'p1g':p1g,'p2':p2,'p2rest':p2rest}
Path(__file__).with_name('results.json').write_text(json.dumps(out,indent=2))
for key in ['p1d','p1g','p2','p2rest']:
 print(key,out[key])

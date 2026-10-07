import json, itertools
from pathlib import Path
import numpy as np
from scipy.optimize import linprog, milp, LinearConstraint, Bounds

OUT = Path(__file__).parent
c = np.array([4., 1., 3.])
A = np.array([[3,2,2],[.1,.2,.15],[-1,-1,-1]])
b = np.array([180,8,-60])
r = linprog(c,A_ub=A,b_ub=b,bounds=[(10,None)]*3,method='highs')
assert r.success
p1 = {'x':r.x.tolist(),'cost':r.fun,'lhs':(A@r.x).tolist(),'marginals':r.ineqlin.marginals.tolist(),'reduced_costs':r.lower.marginals.tolist()}
demand=[]
for d in np.arange(0,65.01,.5):
 q=linprog(c,A_ub=A,b_ub=[180,8,-d],bounds=[(10,None)]*3,method='highs')
 assert q.success
 demand.append([float(d),float(q.fun),*q.x.tolist()])
q=linprog(-np.ones(3),A_ub=A[:2],b_ub=b[:2],bounds=[(10,None)]*3)
p1['max_demand']=-q.fun
p1['demand']=demand

origins=['Pittsburgh','Cleveland','Columbus']; hubs=['Chicago','Atlanta']; dests=['Miami','Orlando','New York']
D=np.array([[100,60,40],[50,50,50],[0,40,60]])
cap1=np.array([[150,100],[100,100],[100,80]])
cost1=np.array([[50,100],[60,90],[70,80]])
cap2=np.array([[150,120,100],[120,150,120]])
cost2=np.array([[100,90,80],[80,70,100]])
capdir=np.array([[100,60,40],[100,60,50],[80,40,60]])
costdir=np.array([[120,80,70],[110,75,65],[100,70,60]])
p3={}
for chosen in [None,0,1,2]:
 # Every OD has two connecting-path variables and one direct-path variable.
 keys=list(itertools.product(range(3),range(3),range(3)))
 costs=np.array([cost1[i,k]+cost2[k,j] if k<2 else costdir[i,j] for i,j,k in keys])
 eq=np.array([[int(i==a and j==b) for i,j,k in keys] for a in range(3) for b in range(3)])
 ub=[]; rhs=[]
 for a in range(3):
  for h in range(2):
   ub.append([int(i==a and k==h) for i,j,k in keys]);rhs.append(cap1[a,h])
 for h in range(2):
  for z in range(3):
   ub.append([int(k==h and j==z) for i,j,k in keys]);rhs.append(cap2[h,z])
 bounds=[(0,None) if k<2 else (0,int(capdir[i,j]) if chosen==i else 0) for i,j,k in keys]
 sol=linprog(costs,A_ub=ub,b_ub=rhs,A_eq=eq,b_eq=D.flatten(),bounds=bounds,method='highs')
 assert sol.success and np.max(np.abs(sol.x-np.round(sol.x)))<1e-6
 x=np.round(sol.x).reshape(3,3,3).astype(int)
 assert np.array_equal(x.sum(axis=2),D)
 p3['Base' if chosen is None else origins[chosen]]={'cost':sol.fun,'paths':x.tolist(),'first_legs':x[:,:,:2].sum(axis=1).tolist(),'second_legs':x[:,:,:2].sum(axis=0).T.tolist(),'direct':x[:,:,2].tolist()}

names=['Alice','Ben','Carlos','Diana','Emma','Frank']
S=np.array([[0,5,10,100,95,85],[65,0,20,45,20,0],[10,70,0,60,40,25],[0,0,0,0,0,65],[0,0,0,0,0,50],[0,0,0,0,0,0]])
edges=list(zip(*np.nonzero(S)))
AA=np.array([[int(i==m) for i,j in edges] for m in range(6)])
EE=np.array([[int(j==m) for i,j in edges] for m in range(6)])
sol=linprog([-S[i,j] for i,j in edges],A_ub=AA,b_ub=[3]*6,A_eq=EE,b_eq=[1]*6,bounds=(0,1))
assert sol.success
selected=[(names[i],names[j],int(S[i,j])) for z,(i,j) in zip(sol.x,edges) if z>.5]
# Exhaustive independent verification of the small assignment problem.
options=[[i for i in range(6) if S[i,j]>0] for j in range(6)]
feasible=[(sum(S[i,j] for j,i in enumerate(a)),a) for a in itertools.product(*options) if max(a.count(i) for i in range(6))<=3]
best=max(v for v,a in feasible)
assert abs(best+sol.fun)<1e-7
p4={'score':float(best),'assignments':selected,'scores':S.tolist(),'optimal_count':int(sum(v==best for v,a in feasible))}
data={'p1':p1,'p3':p3,'p4':p4}
(OUT/'results.json').write_text(json.dumps(data,indent=2))
print(json.dumps({'p1':{k:v for k,v in p1.items() if k!='demand'},'p3':p3,'p4':p4},indent=2))

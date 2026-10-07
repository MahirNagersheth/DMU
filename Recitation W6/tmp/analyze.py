import json, math
import numpy as np
from scipy.optimize import linprog
from scipy.stats import norm, binom, t
from pathlib import Path
p=Path(__file__).parent
rng=np.random.default_rng(76006)
dp=np.array([.02,.03,.05,.08,.33,.29,.2]); dv=np.arange(7)*1000
def fish(n):
 u=rng.random((n,2)); price=norm.ppf(u[:,0],3.65,.2); demand=dv[np.searchsorted(np.cumsum(dp),u[:,1])]; profit=price*np.minimum(3500,demand)-10000
 return dict(u=u.tolist(),price=price.tolist(),demand=demand.tolist(),profit=profit.tolist())
def summary(a):
 a=np.array(a); n=len(a); m=a.mean(); sd=a.std(ddof=1); hw=t.ppf(.975,n-1)*sd/math.sqrt(n)
 return dict(n=n,mean=m,sd=sd,lower=m-hw,upper=m+hw)
f70=fish(70); f500=fish(500); fq=fish(1000)
qs=list(range(2000,6001,100)); qm=[float(np.mean(np.array(fq['price'])*np.minimum(q,fq['demand'])-10000)) for q in qs]
exactfish=float(3.65*np.dot(dp,np.minimum(3500,dv))-10000)
ad=np.arange(14,26); ap=np.array([.03,.05,.07,.09,.11,.15,.18,.14,.08,.05,.03,.02])
def airline(n):
 u=rng.random((n,2)); demand=ad[np.searchsorted(np.cumsum(ap),u[:,0])]; sold=np.minimum(22,demand); show=binom.ppf(u[:,1],sold,.9).astype(int); profit=150*sold-500*np.maximum(show-19,0)
 return dict(u=u.tolist(),demand=demand.tolist(),sold=sold.tolist(),show=show.tolist(),profit=profit.tolist())
a100=airline(100); a5000=airline(5100)
def exact_air(cap):
 mean=second=0.
 for d,pr in zip(ad,ap):
  sold=min(cap,d); k=np.arange(sold+1); val=150*sold-500*np.maximum(k-19,0); prob=binom.pmf(k,sold,.9)
  mean+=pr*np.dot(prob,val); second+=pr*np.dot(prob,val**2)
 return float(mean),float(math.sqrt(second-mean**2))
acaps=list(range(19,26)); ae=[exact_air(k)[0] for k in acaps]
asim=[]
for cap in acaps:
 u=np.array(a5000['u']); d=np.array(a5000['demand']); sold=np.minimum(cap,d); show=binom.ppf(u[:,1],sold,.9); asim.append(summary(150*sold-500*np.maximum(show-19,0)))
# Aggregate recourse LP. Variables: x[3], emergency[3 scenarios x 3 foods].
prob=np.array([.4,.35,.25]); purchase=np.array([12,10,15]); emergency=np.array([18,16,22])
don=np.array([[100,150,80],[200,100,150],[50,80,50]])
dem=np.array([[[120,100,80],[100,120,100],[80,100,70],[100,80,90]],[[140,120,100],[120,140,120],[100,120,90],[120,100,110]],[[100,90,70],[80,100,80],[70,80,60],[90,70,80]]])
tot=dem.sum(axis=1); need=tot-don
c=np.r_[purchase,(prob[:,None]*emergency).ravel()]
A=[]; b=[]
A.append(np.r_[purchase,np.zeros(9)]); b.append(12000)
A.append(np.r_[np.ones(3),np.zeros(9)]); b.append(700)
for s in range(3):
 for j in range(3):
  row=np.zeros(12); row[j]=-1; row[3+s*3+j]=-1; A.append(row); b.append(-need[s,j])
res=linprog(c,A_ub=A,b_ub=b,bounds=(0,None),method='highs')
assert res.success
out=dict(seed=76006,fish70=f70,fish500=f500,fishQ=fq,fish70_summary=summary(f70['profit']),fish500_summary=summary(f500['profit']),fish_exact=exactfish,Q=qs,Q_mean=qm,air100=a100,air5000=a5000,air100_summary=summary(a100['profit']),air5000_summary=summary(a5000['profit']),air_caps=acaps,air_exact=ae,air_sim=asim,air22_exact=exact_air(22),food=dict(x=res.x[:3].tolist(),e=res.x[3:].reshape(3,3).tolist(),objective=float(res.fun),initial=float(np.dot(purchase,res.x[:3])),donations=don.tolist(),demands=dem.tolist(),totals=tot.tolist(),needs=need.tolist(),slack=res.ineqlin.residual.tolist(),status=res.message))
(p/'results.json').write_text(json.dumps(out))
print(json.dumps({k:out[k] for k in ['fish70_summary','fish500_summary','fish_exact','air100_summary','air5000_summary','air22_exact','air_exact','food']},indent=2))

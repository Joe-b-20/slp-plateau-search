#!/usr/bin/env python3
"""LP relaxation value at a given cut level, with the mandatory 97@3 control."""
import sys, math, json, collections, time
sys.path.insert(0,'/home/joebachir20/xor_ui/slp-plateau-search/wrapup/day2/runs/mip3')
import numpy as np
from scipy.sparse import coo_matrix
from scipy.optimize import linprog
from build_lp import build, control_point
lev=int(sys.argv[1])
t0=time.monotonic()
rows, cost, meta = build(True, lev)
p = control_point(meta)
bad = collections.Counter(t for terms,rhs,t in rows if sum(c*p[j] for j,c in terms) < rhs)
obj = sum(c*v for c,v in zip(cost,p))
print(json.dumps({'level':lev,'rows':len(rows),'control_violations':dict(bad),
                  'control_obj':obj}), flush=True)
r,ci,va,b=[],[],[],[]
for i,(terms,rhs,tag) in enumerate(rows):
    for j,cf in terms: r.append(i); ci.append(j); va.append(cf)
    b.append(rhs)
A=coo_matrix((va,(r,ci)),shape=(len(rows),meta['nvar'])).tocsr()
res=linprog(np.array(cost,float), A_ub=(-A).tocsc(), b_ub=-np.array(b,float),
            bounds=[(0,1)]*meta['nvar'], method='highs')
out={'level':lev,'lp':res.fun,'status':res.status,
     'N_depth3_lower_bound': 32+math.ceil(res.fun-1e-7) if res.status==0 else None,
     'control_violations':dict(bad),'control_obj':obj,'wall':time.monotonic()-t0}
print(json.dumps(out), flush=True)
json.dump(out, open('/home/joebachir20/xor_ui/slp-plateau-search/wrapup/day2/runs/mip3/lp_level%d.json'%lev,'w'), indent=1)

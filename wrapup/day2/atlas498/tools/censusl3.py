import os,sys,json,pickle,time
from collections import Counter
ROOT="/home/joebachir20/xor_ui/slp-plateau-search"
sys.path.insert(0,ROOT);sys.path.insert(0,ROOT+"/atlas");sys.path.insert(0,ROOT+"/atlas/corner")
sys.path.insert(0,ROOT+"/experiments/e17_pure/laneY/code")
from verify_circuit import load_index_pairs, mixcolumns_target_masks
from socle import l3_of
from anatomy import replay
import ylib
T=mixcolumns_target_masks()
pop=pickle.load(open(ROOT+"/experiments/e15_campaign3/tools/pop88.pkl","rb"))
res=[];t0=time.monotonic();miss=0
for i,(p,_) in enumerate(pop):
    try:
        pr=[tuple(x) for x in load_index_pairs(json.load(open(p)))]
        l=l3_of(pr)
        dep=[0]*32
        for a,b in pr: dep.append(max(dep[a],dep[b])+1)
        rec={"i":i,"path":p,"l3":l,"depth":max(dep),"n":len(pr)}
        if l<=66:
            an=ylib.Analysis([list(x) for x in pr],T=T)
            rec["kappa"]=an.kappa;rec["Astar"]=len(an.Astar)
        res.append(rec)
    except Exception as e: miss+=1
    if i%2000==0: print(i,round(time.monotonic()-t0,1),file=sys.stderr,flush=True)
json.dump({"n":len(res),"miss":miss,"hist":dict(sorted(Counter(r["l3"] for r in res).items())),
 "low":[r for r in res if r["l3"]<=66]},open(ROOT+"/wrapup/day2/atlas498/census_l3.json","w"),indent=1)
print("done",len(res),"miss",miss,round(time.monotonic()-t0,1))
print(dict(sorted(Counter(r["l3"] for r in res).items())))

# Config as run -- 21h ladder

MODE = cascade (depth ladder, from scratch)
DEPTHS = [3,4,5,6,7,8,9,10,11] + uncapped final
ENGINE_D3 = anneal3 (from scratch);  deeper rungs = lns, seeded from the rung above
MAX_WAIT_S = 7200 (2h per rung);  DEPTH3_BASELINE = 97;  IMPROVE_BY = 1
SEEDS_PER_WORKER = [1,2,3]
RESEED = (feature did not exist in this code)
See ../coordinator.log for the exact launch/trigger timeline.

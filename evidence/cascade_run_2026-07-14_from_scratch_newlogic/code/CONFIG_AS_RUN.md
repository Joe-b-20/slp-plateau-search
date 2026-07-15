# Config as run -- cascade (from-scratch depth ladder, new logic)

MODE = "cascade";  RESEED = True;  CHUNK_S = 600;  SEEDS_PER_WORKER = [1,2,3]
DEPTHS = [3,4,5,6,7,8,9,10,11];  FINAL_UNCAPPED_DEPTH = True
ENGINE_D3 = anneal3 (from scratch);  ENGINE_DEEP = lns
MAX_WAIT_S = 7200;  IMPROVE_BY = 1;  DEPTH3_BASELINE = 97
Continuous reseeding ON (this is the run whose reseeding collapsed diversity).

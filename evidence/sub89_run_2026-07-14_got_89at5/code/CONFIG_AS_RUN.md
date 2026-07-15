# Config as run -- sub-89 (the seeded relaunch)

MODE = "fixed";  RESEED = True;  CHUNK_S = 600;  SEEDS_PER_WORKER = [1,2,3]
FIXED_WORKERS = [
  dict(label="uncapped_sub89", engine="lns", depth=None, start="seeds/seed_89_at_depth6.json"),
  dict(label="depth5_sub90",   engine="lns", depth=5,    start="seeds/seed_90_at_depth5.json"),
]
(seed_89_at_depth6 = the 21h run's d10 circuit; seed_90_at_depth5 = its d11)
Knobs: default LNS_KNOBS (see config.json). Reseeding ON.

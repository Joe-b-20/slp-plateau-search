# The two exact deciders

`exact_window.py` (budgets 1–2, k ≤ 3) and `exact_k4.py` (budget 3, k = 4),
verbatim as archived from campaign 87. Their module docstrings carry the
first-unlock case analysis that makes a `None` answer a proof rather than a
failed search — that proof is the completeness argument cited in
`../CERTIFICATES.md` and `../../../METHODS.md` §10.

Every `exact_window/`, `exact_k4/`, `pop_decider/` and `family3_exact/` verdict
log in the parent folder was produced by these two modules.

Stdlib-only. `exact_window.py` imports `mixcolumns_core` (identical to
`pipeline/mixcolumns_core.py`) and, inside `rebuild_circuit()` only, `engines`;
put those on the path to run them.

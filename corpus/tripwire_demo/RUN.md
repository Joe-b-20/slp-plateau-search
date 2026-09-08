# RUN — the B = 56 tripwire

`tripwire.py` is a standalone, standard-library instrument you point at
somebody else's XOR circuit file. In seconds it tells you whether a gate can be
deleted from it. Nothing about it is specific to this project's circuits.

It computes three things:

1. **Duplicate masks** — two gates computing the same value. Rewire and delete
   the later one.
2. **Dead gates** — a non-output gate nothing consumes. Delete it outright.
3. **B**, the number of gates that are neither outputs nor unread. On any
   valid, irreducible circuit `B = n - q`, where `q` is the number of outputs.
   For AES MixColumns `q = 32`, so a valid irreducible 88-gate circuit has
   **B = 56 exactly**.

`B ≠ n - q` on a valid circuit is not a curiosity: it **is** a one-gate
improvement, constructively. The arrow runs one way only — see the note under
positive control 1.

**It does not check that your circuit is correct.** Run a verifier first
([`../records_check/RUN.md`](../records_check/RUN.md)).

---

## RE-RUN (a) — a published 88: must stay SILENT, B = 56

The five published record 88s, plus the one published 88 from a **foreign
lineage** (an independently authored circuit this project did not produce).

```
$ nice -n 19 python3 tripwire.py --quiet circuits/mixcolumns_88gates_depth*.json circuits/foreign_88gates_depth7_eprint_2026-1481.json
target: AES MixColumns (forward), rebuilt from GF(2^8) mod 0x11B -- 32 outputs, 32 inputs
rule:   B = gates - outputs = n - 32 on any valid, irreducible circuit;
        any other value hands you an (n-1)-gate circuit by deletion.
note:   this tool does NOT check that the circuit is correct.

  mixcolumns_88gates_depth5.json                       n=88   B=56   expect=56   silent
  mixcolumns_88gates_depth5_fromscratch.json           n=88   B=56   expect=56   silent
  mixcolumns_88gates_depth6.json                       n=88   B=56   expect=56   silent
  mixcolumns_88gates_depth7.json                       n=88   B=56   expect=56   silent
  mixcolumns_88gates_depth8.json                       n=88   B=56   expect=56   silent
  foreign_88gates_depth7_eprint_2026-1481.json         n=88   B=56   expect=56   silent
========================================================================
6 file(s) examined, none has a deletable gate.
  exit status: 0  (0 = every file silent)
```

**PASS condition:** every file `B = 56`, silent, exit 0.
**Measured 2026-09-01: 0.3 s wall for all six.**

Silence means "no gate is deletable by the two mechanisms above". It does
**not** mean the circuit is minimal. That is a different and much harder
question, and this tool has nothing to say about it.

---

## RE-RUN (b) — the planted defects: must FIRE

An instrument that cannot fire is not evidence, so the positive controls are not
optional. Both are the published depth-6 record 88 with one gate added.

### Build them

```
$ nice -n 19 python3 tools/make_planted.py circuits/mixcolumns_88gates_depth6.json
outdir: /tmp/planted_xxxxxxxx
planted_dup.json  : 89 gates (duplicate of gate 20, given a consumer)
planted_dead.txt  : 89 gates (last one has no consumer)
```

With no output directory named, the two controls go to a fresh temporary
directory whose path is printed, and nothing inside the repository is written.
The copies committed under `circuits/` are what the runs below use; naming
`circuits` as a second argument regenerates them in place.

### Positive control 1 — a planted duplicate value

```
$ nice -n 19 python3 tripwire.py circuits/planted_dup.json
…
planted_dup.json
------------------------------------------------------------------------
  89 gates over 32 inputs; the target map has 32 outputs.
  32 of those 32 target values appear somewhere in the circuit.

  duplicate values : 1
  dead gates       : 0
  working values B : 57   (expected 57 = 89 gates - 32 outputs)

  RESULT: *** A GATE CAN BE DELETED. ***
          You are holding a 88-gate circuit for this map.

  1 duplicated value(s): two gates compute the same thing.
  Delete the later gate and point whatever read it at the earlier one.
     gate 20 and gate 21 both compute 0x02020002

========================================================================
1 of 1 file(s) have a deletable gate: planted_dup.json
  exit status: 1  (1 = fired, the pass condition here)
```

**Read the arrow the right way round.** In this control **B reads 57 — exactly
its expected value — and the tripwire fires anyway**, on the duplicate check.
The duplicated value is not one of the 32 targets, so both copies count as
working gates and B stays clean while a gate is still plainly deletable.

`B ≠ n - q ⟹ a deletable gate` is sound. **Its converse is false**, and this
control is the demonstration. B is a screen, not a decision procedure. Run all
three checks.

### Positive control 2 — a planted dead gate, in the plain-text format

```
$ nice -n 19 python3 tripwire.py circuits/planted_dead.txt
…
  duplicate values : 0
  dead gates       : 1
  working values B : 56   (expected 57 = 89 gates - 32 outputs)

  RESULT: *** A GATE CAN BE DELETED. ***
          You are holding a 88-gate circuit for this map.

  1 dead gate(s): computed, not a target, and nothing reads them.
  Delete them outright.
     gate(s): 88
  exit status: 1  (1 = fired)
```

Here B reads 56 against an expected 57 — the B rule fires on its own. This case
also exercises the second input reader: the file is the plain-text `a b` format,
not JSON.

**Measured 2026-09-01: 0.1 s wall each.**

---

## RE-RUN (c) — the built-in self-test

`--selftest` plants both defects into whatever circuit you hand it and checks
that the clean circuit is silent and both planted versions fire:

```
$ nice -n 19 python3 tripwire.py --selftest circuits/mixcolumns_88gates_depth5_fromscratch.json
========================================================================
SELF-TEST
------------------------------------------------------------------------
  1. the clean circuit as given            -> silent  (must be silent)
  2. same circuit + one duplicated gate    -> FIRED  (must fire)
  3. same circuit + one gate nobody reads  -> FIRED  (must fire)

  SELF-TEST: PASS
  exit status: 0  (0 = all three controls behaved)
```

**Measured 2026-09-01: 0.1 s wall.**

Full transcript of all of the above: `out/DEMO.txt`.

---

## Scope

The tripwire is a **theorem with a decision rule**, not a rigidity statistic: it
either produces a smaller circuit or it does not, and when it does, the smaller
circuit is constructed, not inferred. That is why it survives the repricing that
applies to this project's neighbourhood negatives
([`../calibration/CONTROL_AUDIT.md`](../calibration/CONTROL_AUDIT.md)) — it is
not being used as evidence *about* optimality.

The much stronger deletion test — delete a gate and allow the surviving 87
masks to be rebuilt in **any** order — is in
[`../deletion_certificate/CERT.md`](../deletion_certificate/CERT.md).

---

## Files

| path | what it is |
|---|---|
| `tripwire.py` | the instrument; standard library only, Python 3.6+ |
| `circuits/mixcolumns_88gates_depth{5,5_fromscratch,6,7,8}.json` | the five published record 88s |
| `circuits/foreign_88gates_depth7_eprint_2026-1481.json` | the published 88 from an independent author |
| `tools/make_planted.py` | builds the two positive controls |
| `out/DEMO.txt` | transcript of the 2026-09-01 re-run |

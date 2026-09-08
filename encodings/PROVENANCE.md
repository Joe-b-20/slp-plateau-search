# Provenance of the shipped files

Two things have to be true for the theorem in [`STATEMENT.md`](STATEMENT.md) to
mean anything: the CNFs must be the formulas that were actually solved, and the
instance must be the object the whole programme priced. Neither is asserted
here. Both are checkable, and this page says what was checked and what was
edited.

---

## 1. The instance is hash-pinned

`instance/instance_joint_W3U4.json` is the merged block, byte-for-byte. Nothing
in this pack constructs a supply, a target list or a line set; every script reads
that file verbatim.

| | |
|---|---|
| file sha256 | `d00504cbb8f19dc494d9edd93ee724d7075e262e82d76626e01d3f2f39de2d5b` |
| canonical sha256 (sorted keys, no whitespace) | `d00504cbb8f19dc494d9edd93ee724d7075e262e82d76626e01d3f2f39de2d5b` |
| instance key | `f04dcb3ecf180a30204434a0bd32453e7635e8b6` |
| shape | rank 16, lines {2, 3, 4, 7}, 33 free signals, 8 targets, no depth cap |

The canonical digest is pinned inside `code/instance_io.py`; every script that
reads this file refuses to run if it moves.

**Where the pin comes from.** Upstream, that object was produced by a pre-flight
that asserted it before a second of compute was spent. Its first run *failed*,
catching eight fabricated intermediate values that were leaking into the free
supply. The digest of that pre-flight file
(`d4916aef84137088c45e4c09627d4ac00d82420eec94fa9a033f3a822250cf68`), the key
computed by the upstream programme's own `key_of` function, and the assertions on
shape and supply are recorded verbatim in every
`cnf/*_meta.json` under `repo_cross_check`, and were re-run read-only at
generation time. The free supply is exactly the union of the two blocks'
supplies: 26 ∪ 25 = 33, with no value off the four lines.

## 2. The CNFs are the encoder's formulas

`code/check_cnf.py` parses each shipped file back into a clause list and compares
it with a fresh `slp_opt.build_cnf(...)` call **literal for literal and in
order**. All six ladder levels and the control return `VERDICT: IDENTICAL`; the
reports are in `results/identity_*.json` and the output is pasted in
[`RUN.md`](RUN.md) §1.

Each file's header also carries the **clause-order sha256** of the encoder's
output — a digest of the clause list as ordered, independent of file formatting.

## 3. What was edited for publication, and what was not

The CNFs were **not regenerated** for this pack. Their clause bytes were copied.
What changed is the `c` comment block at the top of each file: the generator had
written the internal module paths of the machine that produced it, and those were
rewritten to name this pack's own files instead. Comments are not part of a
DIMACS formula and no solver reads them.

That edit is proved harmless rather than claimed harmless: for every file below,
the bytes from the `p cnf` line onward — every clause, in order — hash the same
before and after.

| file | bytes | clause body identical | sha256 as generated | sha256 in this pack |
|---|---|---|---|---|
| `k9_joint_W3U4.cnf` | 2 038 738 | **yes** | `d59d155fdd5be5bb509a7acb3db81e61f3fdc32c08a361a1e1d3ee06679dee1b` | `3158d26e99da2de87f23520b4db4caae1200d990489d8a730582a67cd476a61d` |
| `k10_joint_W3U4.cnf` | 2 422 869 | **yes** | `bc57692514ed62ed9a27c3ad0489ae5b3f5d3c560f5e5dbd9d0cf5425f76188a` | `d10f412dd1aa7b1d6d9e2ff49c6e307e3123636297d018834e4fb67e373d446a` |
| `k11_joint_W3U4.cnf` | 2 840 968 | **yes** | `617ec336699ff519af548433674b6d8deb7b2c47bcf5d06ac3fec8eb77137b92` | `942436d281bef50bd75277c6728b51d02f44a9b7e327d6b84a740f8d71c51c02` |
| `k12_joint_W3U4.cnf` | 3 294 463 | **yes** | `cee458bd83b727cd2f7f14790622f0b8d0f73366df3896453f3de90b0eb3a6ed` | `59d836caf7b35f50fdc2add9d5f07259999d199d2b80d9ed99d5d4522b25c869` |
| `k13_joint_W3U4.cnf` | 3 784 918 | **yes** | `ca5a2a1716fbd011733be24672c4c70c87c54d7400992bf5c9f8f12e553f9c3d` | `a767d77ccb02a96662b01e01fbc624024d40d6563ef7f2ed06925971418770c1` |
| `k14_joint_W3U4.cnf` | 4 339 694 | **yes** | `1968ae974ce94945a3f0c2e954e3cbe075c17f7724402c8aad619ff9989f935f` | `4d12255ad5ec79e06722370000ec9f90a928d39953c4b3157967c527b01dbea7` |
| `k7_SUB_U4tgts.cnf` | 1 360 315 | **yes** | `573dc50146146c1c0b2b4e66a493cd26487b1ec29928281a1020e933b6740c63` | `327a924732694e48492c07e91739cdac864638d71387795f949fa11a9f9e3173` |

Clause-body digests — the quantity that is invariant under the comment edit:

```
k9_joint_W3U4.cnf   59e5632f6a70b10e84b8638779c3850f2562e2603158878f5045b4c8ff43778b
k10_joint_W3U4.cnf  ba8316b87bb50e434f14934028af9176c59cedf48eb8701fdd1c3911ab86af14
k11_joint_W3U4.cnf  b1578796eeb7c06e275b5b7ae204b4ea2216b936317493a9b0255ff7514a7de8
k12_joint_W3U4.cnf  dddd15200c446e2828938ac23fd61aa0d0afca25ae862e9224a6d0e8944dff47
k13_joint_W3U4.cnf  3de3ac6a0a94d0293bc5b341d4055e95472cd024341f343606a9c5275d3ded3d
k14_joint_W3U4.cnf  390b6733b8d78b6d96ad90dc808711a708adc96fdb63243b1a1f507ad32af28e
k7_SUB_U4tgts.cnf   afae813505f0d81fd9fa931a7091f72d424c2e3c2a4b96ac0fcae55048ab7ef0
```

The same edit was applied to the `*_meta.json` files: absolute filesystem paths
were reduced to file names. Every digest, key and boolean in them is unchanged.

`SHA256SUMS` lists the files as they ship here. Regenerate and check with:

```bash
sh code/make_checksums.sh
sha256sum -c SHA256SUMS
```

## 4. Copied code

| file | what it is |
|---|---|
| `code/slp_opt.py` | the encoder and its proofs, copied unmodified from the research repository |
| `code/verify_circuit.py` | the standalone MixColumns oracle, copied unmodified |

Both were verified byte-identical to their sources at copy time and their
digests are in `SHA256SUMS`, so any later drift is visible. The remaining
scripts (`solve_dimacs.py`, `check_cnf.py`, `emit_cnf.py`, `decode_model.py`,
`instance_facts.py`, `instance_io.py`) were written for this pack and depend on
nothing outside it.

## 5. What is *not* claimed

Byte-identity with any file on the machines that ran the decisive solves. No
such file exists: the solving harness builds its CNF in memory and hands the
clause list straight to a solver — it never writes DIMACS. The claim is
**semantic** identity: same instance object, same encoder function, same
arguments, same clause list in the same order. Each of those links is checked by
a script in this pack rather than asserted.

## 6. Citation

* Author: Joe Bachir
* Method and campaign: <https://github.com/Joe-b-20/slp-plateau-search>
* Circuits and note: <https://github.com/Joe-b-20/aes-mixcolumns-xor-circuits>,
  DOI [10.5281/zenodo.21299092](https://doi.org/10.5281/zenodo.21299092)
* Licence: MIT

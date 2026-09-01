#!/usr/bin/env python3
"""instance_io.py -- read an instance file verbatim and hash it.

Nothing in this pack constructs a supply, a target list or a line set.  Every
script reads the shipped JSON byte-for-byte and reports two digests:

  file_sha256       sha256 of the raw bytes on disk
  canonical_sha256  sha256 of the instance re-serialised with sorted keys and
                    no whitespace -- the *identity* of the mathematical object,
                    independent of formatting

The canonical digest of the merged-block instance is pinned below.  It is the
key that ties this pack's CNFs to the object the campaign solved; a script
that reads that file refuses to run if the digest moves.
"""
import hashlib, json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
PACK = os.path.dirname(HERE)

# canonical sha256 of the merged-block instance (the one in instance/)
MERGED_BLOCK_SHA256 = \
    "d00504cbb8f19dc494d9edd93ee724d7075e262e82d76626e01d3f2f39de2d5b"
# the campaign's instance key for the same object, carried verbatim
MERGED_BLOCK_KEY = "f04dcb3ecf180a30204434a0bd32453e7635e8b6"

DEFAULT_INSTANCE = os.path.join(PACK, "instance", "instance_joint_W3U4.json")


def load_slp_opt():
    """Import the encoder that ships with this pack (code/slp_opt.py)."""
    if HERE not in sys.path:
        sys.path.insert(0, HERE)
    import slp_opt as SO
    return SO


def canon(inst):
    return json.dumps(inst, sort_keys=True, separators=(",", ":")).encode()


def load_instance(path=None, pin=True):
    path = path or DEFAULT_INSTANCE
    with open(path, "rb") as f:
        raw = f.read()
    d = json.loads(raw)
    d = d.get("instance", d)
    inst = {kk: d[kk] for kk in d if not kk.startswith("_")}
    checks = {
        "file": os.path.basename(path),
        "file_sha256": hashlib.sha256(raw).hexdigest(),
        "canonical_sha256": hashlib.sha256(canon(inst)).hexdigest(),
        "dim": inst["dim"],
        "lines": inst.get("lines"),
        "n_inputs": len(inst["inputs"]),
        "n_targets": len(inst["targets"]),
        "depth": inst.get("depth"),
    }
    if pin:
        checks["canonical_sha256_matches_pin"] = (
            checks["canonical_sha256"] == MERGED_BLOCK_SHA256)
        checks["instance_key"] = MERGED_BLOCK_KEY
        if not checks["canonical_sha256_matches_pin"]:
            raise SystemExit("INSTANCE PIN FAILED: %s" % json.dumps(checks))
    return inst, checks


def clause_digest(clauses):
    """sha256 over the clause list AS ORDERED -- the encoder's output identity."""
    h = hashlib.sha256()
    for cl in clauses:
        h.update((" ".join(str(x) for x in cl) + " 0\n").encode())
    return h.hexdigest()


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()

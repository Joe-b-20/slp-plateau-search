#!/bin/bash
# One-shot status of the k=14 decisive solve. Safe to run any time.
R=/home/joebachir20/xor_ui/slp-plateau-search
L=$R/fleet11/laneCUBE
echo "=== $(date -Is)"

# 1. The headline: did anything find a circuit at 87 or below?
if [ -f "$R/experiments/STOP" ]; then
  echo "*** STOP FILE PRESENT — something claims <= 87 gates ***"
  ls -la $R/experiments/FOUND_*.json 2>/dev/null
  for f in $R/experiments/FOUND_*.json; do
    [ -f "$f" ] && echo "--- re-verifying $f:" && python3 $R/verify_circuit.py "$f" 2>&1 | tail -3
  done
else
  echo "no STOP file  (nothing claims <= 87)"
fi

# 2. Did the decisive level resolve?
if [ -f "$L/found/HIT_joint_W3U4_k14.json" ]; then
  echo "*** SAT AT k=14 — the class drops a gate. Witness:"
  head -c 400 "$L/found/HIT_joint_W3U4_k14.json"; echo
else
  v=$(grep -l '"status": "UNSAT"' "$L"/logs/mono_14*.log 2>/dev/null | head -1)
  if [ -n "$v" ]; then
    echo "*** k=14 DECIDED UNSAT by $(basename "$v") — merged W3|U4 = 15, no 87 in that class ***"
  else
    echo "no k=14 SAT hit yet"
  fi
fi

# 3. What the four solvers have said (empty = still running, silence is normal)
echo "--- solver logs:"
for f in "$L"/logs/mono_14*.log; do
  [ -f "$f" ] || continue
  n=$(wc -c < "$f")
  if [ "$n" -eq 0 ]; then echo "  $(basename $f): still running (no output yet)"
  else echo "  $(basename $f):"; tail -2 "$f" | sed 's/^/      /'; fi
done

# 4. Are they still alive, and for how long?
alive=0
for p in $(pgrep -f 'mono.py' 2>/dev/null); do
  case "$(readlink /proc/$p/cwd 2>/dev/null)" in *fleet11*) alive=$((alive+1));; esac
done
echo "--- $alive solver(s) alive; elapsed:"
for p in $(pgrep -f 'mono.py' 2>/dev/null); do
  case "$(readlink /proc/$p/cwd 2>/dev/null)" in
    *fleet11*) echo "      PID $p  $(ps -o etime=,pcpu= -p $p 2>/dev/null)";;
  esac
done
[ "$alive" -eq 0 ] && echo "      (none running — either finished, or stopped; check the logs above)"

echo "--- full write-up: $L/RESULT.md   (stop/resume commands in its section 9)"

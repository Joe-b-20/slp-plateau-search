#!/bin/bash
# status.sh -- one hunt status snapshot + dead-worker restart.
cd "$(dirname "$0")/runs_hunt" || exit 1
alive=$(ps aux | grep -c "[h]unt_worker.py")
line="$(date +%H:%M:%S) alive=$alive |"
for s in w*_status.json; do
  b=$(python3 -c "import json;d=json.load(open('$s'));print('%s@%s'%(d['best_gates'],d['best_depth']))" 2>/dev/null)
  line="$line ${s%_status.json}=$b"
done
echo "$line"
for f in ALERT_*_87gates.json ALERT_*_86gates.json ALERT_*_85gates.json; do
  [ -f "$f" ] && echo "BREAKTHROUGH CANDIDATE FILE: $f"
done
for w in w6_syl89 w7_hyb90 w8_div89a w9_div89b w10_sym94; do
  b=$(python3 -c "import json;print(json.load(open('${w}_status.json'))['best_gates'])" 2>/dev/null)
  if [ -n "$b" ] && [ "$b" -le 88 ] 2>/dev/null; then echo "INDEPENDENT <=88 on $w: $b gates (seed was >=89)"; fi
done
# restart dead workers if hunt window still open (deadline file holds epoch)
DEADLINE=$(cat ../hunt_deadline 2>/dev/null || echo 0)
NOW=$(date +%s)
if [ "$NOW" -lt "$((DEADLINE - 120))" ]; then
  for s in w*_status.json; do
    w=${s%_status.json}
    pid=$(python3 -c "import json;print(json.load(open('$s'))['pid'])" 2>/dev/null)
    upd=$(python3 -c "import json,time;print(int(time.time()-json.load(open('$s'))['updated']))" 2>/dev/null)
    if [ -n "$pid" ] && ! kill -0 "$pid" 2>/dev/null; then
      rem=$((DEADLINE - NOW))
      echo "RESTARTING dead worker $w for ${rem}s"
      seedf="${w}_best.json"; [ -f "$seedf" ] || seedf="../work/seeds/IMPORTED_88.json"
      (cd ../work && nohup python3 hunt_worker.py "$w" lns "../runs_hunt/$seedf" ../runs_hunt "$((RANDOM))" "$rem" '{}' >/dev/null 2>&1 &)
    fi
  done
fi

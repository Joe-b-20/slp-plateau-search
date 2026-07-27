#!/bin/bash
# monitor_pass.sh -- one wave-3 monitoring pass: status line, ALERT check,
# census (dedupe + family detection), dead-worker restart.
cd "$(dirname "$0")" || exit 1
line="$(date +%H:%M:%S) alive=$(ps aux | grep -c '[h]unt_worker.py') |"
for s in runs_hunt/*_status.json; do
  b=$(python3 -c "import json;d=json.load(open('$s'));print('%s@%s'%(d['best_gates'],d['best_depth']))" 2>/dev/null)
  w=$(basename "$s" _status.json)
  line="$line $w=$b"
done
echo "$line"
for f in runs_hunt/ALERT_*_87gates.json runs_hunt/ALERT_*_86gates.json runs_hunt/ALERT_*_85gates.json; do
  [ -f "$f" ] && echo "!!! BREAKTHROUGH CANDIDATE: $f"
done
python3 census.py
# restart dead workers with remaining time
DEADLINE=$(cat hunt_deadline 2>/dev/null || echo 0)
NOW=$(date +%s)
if [ "$NOW" -lt "$((DEADLINE - 180))" ]; then
  REPEL='{"lns":{"repel_file":"../repel_masks.json","repel_pen":2,"repel_up_p":0.25},"walk":{"repel_file":"../repel_masks.json","repel_up_p":0.25}}'
  for s in runs_hunt/*_status.json; do
    w=$(basename "$s" _status.json)
    pid=$(python3 -c "import json;print(json.load(open('$s'))['pid'])" 2>/dev/null)
    if [ -n "$pid" ] && ! kill -0 "$pid" 2>/dev/null; then
      rem=$((DEADLINE - NOW))
      seedf="../runs_hunt/${w}_best.json"
      [ -f "runs_hunt/${w}_best.json" ] || continue
      knobs='{}'
      case "$w" in p*) knobs="$REPEL";; f1*) knobs="$REPEL";; esac
      echo "RESTARTING dead worker $w for ${rem}s"
      (cd work && nohup python3 hunt_worker.py "$w" alt "$seedf" ../runs_hunt "$((RANDOM + 5000))" "$rem" "$knobs" >/dev/null 2>&1 &)
    fi
  done
fi
df -h / | tail -1 | awk '{print "disk avail: "$4}'

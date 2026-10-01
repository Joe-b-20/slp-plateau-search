#!/bin/sh
# Runs every check of lower_bounds/checks and prints the last lines of each. Python 3 standard library,
# except lp_regen.py (numpy + scipy). About 2 minutes on one core.
cd "$(dirname "$0")" || exit 1
for s in finite_facts.py check72.py check73.py check_dark_source.py certify74.py independent74.py certify75.py independent75.py stress.py lp_regen.py; do
  echo "=== $s"
  python3 "$s" 2>&1 | tail -n 6
done

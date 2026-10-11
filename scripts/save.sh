#!/usr/bin/env bash
# Commit the bot's new results back to the repo (runs inside GitHub Actions).
set -euo pipefail
git config user.name "quant-lab-bot"
git config user.email "41898282+github-actions[bot]@users.noreply.github.com"
git add -A data REPORT.md
[ -f BACKTEST.md ] && git add BACKTEST.md
if git diff --cached --quiet; then echo "nothing new to save"; exit 0; fi
git commit -q -m "$1"
for i in 1 2 3 4 5; do
  if git push -q; then echo "saved"; exit 0; fi
  echo "push rejected, rebasing (attempt $i)"
  git pull -q --rebase -X theirs || { git rebase --abort || true; git pull -q --no-rebase -X ours; }
  sleep $((i * 3))
done
echo "could not push results"; exit 1

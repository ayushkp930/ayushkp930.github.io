#!/usr/bin/env bash
set -euo pipefail

# Configure PORTFOLIO_DIR if your cloned Pages repository lives elsewhere.
PORTFOLIO_DIR="${PORTFOLIO_DIR:-$HOME/projects/ayushkp930.github.io}"
GENERATOR="$HOME/.thm-badge/src/generate.js"
BADGE_SYNC="$PORTFOLIO_DIR/scripts/sync-thm-badges.py"

if ! command -v node >/dev/null 2>&1; then
  echo "ERROR: Node.js is not installed or not in PATH." >&2; exit 1
fi
if [[ ! -f "$GENERATOR" ]]; then
  echo "ERROR: TryHackMe stats-badge generator not found at $GENERATOR" >&2
  echo "See SYNC_TRYHACKME_KALI.md for installation instructions." >&2; exit 1
fi
if [[ ! -f "$BADGE_SYNC" ]]; then
  echo "ERROR: Earned-badge sync script not found at $BADGE_SYNC" >&2; exit 1
fi
if [[ ! -d "$PORTFOLIO_DIR/.git" ]]; then
  echo "ERROR: Website repo not found at $PORTFOLIO_DIR" >&2
  echo "Clone https://github.com/ayushkp930/ayushkp930.github.io.git there or set PORTFOLIO_DIR." >&2
  exit 1
fi

# Prefer the dedicated venv used by the setup guide. Fallback to PATH's python3.
PYTHON="${SYNC_PYTHON:-$HOME/.thm-badge-venv/bin/python}"
if [[ ! -x "$PYTHON" ]]; then PYTHON="$(command -v python3)"; fi

cd "$PORTFOLIO_DIR"
export THM_USERNAME="Kshatantra"
export THEME="matrix"
export OUTPUT_PATH="assets/thm_badge.svg"

# The first generator creates the live stats SVG (rank/rooms/badge count etc.).
node "$GENERATOR"
# This second, community-documented endpoint returns earned badge records and artwork URLs.
# If it fails or gets checkpointed, set -e stops before commit/push; previous files remain intact.
"$PYTHON" "$BADGE_SYNC" --username "$THM_USERNAME" --output "assets/thm_badges.json"

git add assets/thm_badge.svg assets/thm_badges.json
if git diff --cached --quiet; then
  echo "No TryHackMe badge/stat changes to publish."
  exit 0
fi
git commit -m "chore: refresh TryHackMe stats and earned badges"
git push

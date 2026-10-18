# AYUSH.SEC — Cybersecurity Portfolio

Dark cyber-ops themed static portfolio for GitHub Pages. Built with HTML, CSS and browser JavaScript; no frontend framework or paid hosting required.

## Contents

- `index.html` — responsive portfolio with neon terminal aesthetic.
- `assets/thm_badge.svg` — placeholder for the community-generated TryHackMe stats SVG. Replace through the sync setup.
- `assets/thm_badges.json` — initial “not synced” data file. After a successful local sync, contains real earned badge names and public image URLs.
- `scripts/sync-thm-badges.py` — fetches the user's public earned-badge records on the user's own computer and writes the gallery JSON.
- `scripts/refresh-thm-badge.sh` — refreshes both the stats SVG and earned-badge JSON, then commits and pushes changes.
- `SYNC_TRYHACKME_KALI.md` — detailed Kali/Linux setup and daily scheduler instructions.

## Publish on GitHub Pages

1. Create/use a public repository named `ayushkp930.github.io`.
2. Upload the contents of this directory into the **repository root**; don't nest them inside another folder.
3. Keep `index.html` at the repository root and keep the `assets/` and `scripts/` folders beside it.
4. Open Settings → Pages and publish from branch `main` and folder `/(root)`.
5. Your site should be at `https://ayushkp930.github.io/`.

## TryHackMe badges

The page intentionally does not fabricate badge artwork. Until the local sync runs successfully, the THM gallery shows a clear “SYNC REQUIRED” state and links to the official TryHackMe profile. Follow `SYNC_TRYHACKME_KALI.md` to fetch public earned-badge records and publish the generated JSON. The endpoint is observed/unofficial and can change; it may return a checkpoint or rate limit. The stats SVG and earned-badge gallery are separate artifacts.

Do not put TryHackMe credentials/cookies, GitHub tokens, API keys, or other secrets into this public repository. The sync uses public profile data and your computer's normal Git authentication.

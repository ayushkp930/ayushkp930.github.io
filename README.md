# AYUSH.SEC — Cybersecurity Portfolio

Responsive cyber-ops portfolio for Ayush Kumar Patel. The site uses plain HTML, CSS and JavaScript, with a black / neon-green / cyan interface, terminal-inspired hero, custom matrix background, curated public repository cards, internship experience, certificates, and badge panels linking to the official training profiles.

## Run locally

1. Download and extract `ayush-cyber-portfolio.zip`.
2. Open `index.html` in a modern browser.
3. An internet connection is needed to load the linked official Hack The Box badge images. Everything else is static and local.

## Publish free with GitHub Pages

1. Create a **public** repository named `ayushkp930.github.io`.
2. Upload `index.html` and this `README.md` to the repository root.
3. Open **Settings → Pages**.
4. Select **Deploy from a branch**, choose branch `main` and folder `/ (root)`, then save.
5. When the deployment finishes, visit `https://ayushkp930.github.io`.

## What is linked

- GitHub profile: `https://github.com/ayushkp930`
- TryHackMe: `https://tryhackme.com/p/Kshatantra`
- Hack The Box: `https://profile.hackthebox.com/profile/019d526d-dbbd-71f6-91b5-494f42fe4cee`
- LinkedIn: `https://www.linkedin.com/in/ayush-kumar-patel-5a7985368/`
- Curated repositories: CloudSentinel, Advanced SOC & Threat Detection, GCP Breach Response & BCDR, PhishShield Pro, Web Application Vulnerability Scanner, and Google Cloud Mastery Labs.
- Credentials: TryHackMe SAL1, Google Cloud Cybersecurity Professional Certificate, Google Cybersecurity Professional Certificate, and IBM Cybersecurity Analyst Professional Certificate.

## Accuracy and privacy notes

- Public GitHub repository descriptions were checked when the site was updated. The project cards summarize each repository and link to the exact repository instead of linking every card to the GitHub profile.
- The site includes public Hack The Box badge images visible on the linked public HTB profile. The TryHackMe numbers (613+ rooms, 81 badges, 172-day streak, rank #1709 / Top 1%, league achievements) came from the supplied resume and are **not live data**. Recheck them on TryHackMe before publishing; remove or edit any figure that is no longer accurate.
- TryHackMe and Hack The Box automatic refresh is **not configured**. The site does not claim to have live API syncing. Unsupported metrics should not be scraped from private sessions or browser cookies.
- The site uses the email from the latest GitHub profile details pasted by the owner (`ayush0858e@gmail.com`). The supplied PDF resume lists a different email (`ayushkp930@gmail.com`) and a different LinkedIn slug (`ayush-kumar-cybersecurity`). Confirm the preferred primary email and LinkedIn URL before publishing the site or resume. This mismatch is intentionally documented here rather than silently assuming both are equivalent.
- The resume PDF is not bundled or linked. It contains contact details and currently has the conflicting email / LinkedIn values above; add a corrected copy only after confirming what should be public.
- Internship dates and bullet points are based on the supplied resume. The Elevate Labs repository is linked as proof-of-work; no public NIELIT project repository was supplied.
- The public `Web-Application-Vulnerability-Scanner` repository lists `users.sqlite3`, `scan_history.sqlite3`, and `__pycache__` files. Before promoting that repository, inspect the databases for real user, credential, scan-target, or other non-demo data; remove generated databases/caches from version control if they do not belong there and add suitable `.gitignore` entries. Do not assume they are safe without checking their contents.
- The vulnerability scanner should only be tested against systems you own or have explicit permission to assess.
- No passwords, session cookies, private API tokens, or API secrets are stored in this static site.

## Live-stat sync (future enhancement)

GitHub Pages serves static files, so it cannot safely hold private credentials. A later scheduled GitHub Actions workflow may publish a generated public JSON file for metrics that have a supported, stable source. The current site intentionally avoids claiming live THM/HTB synchronization where public endpoints cannot be verified.

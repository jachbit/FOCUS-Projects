# F.O.C.U.S.© Projects

**Jachbit 2026** · Every public F.O.C.U.S. project on GitHub in one place, with a link to its live page and its code.

**Open it:** https://jachbit.github.io/FOCUS-Projects/

## What it does
- Cards grouped by category (Trading Tools, Trading References, Everyday Tools, Community, Wellness), each with **▶ Open page** (the live GitHub Pages site) and **</> Code** (the repo), plus a Live page / Runs locally badge and the last-updated date.
- Search box and category filters.
- **Save PDF**: downloads the F.O.C.U.S. template PDF of all projects (clickable links), saved as `FOCUS_Projects_YYYYMMDD_HHMMSS.pdf`. GitHub rebuilds it (`data/FOCUS_Projects_latest.pdf`, Action *Projects PDF*) whenever `projects.json` changes and once a day for the updated dates. If that file is missing, the button falls back to printing the page.
- A new public repo shows up on its own under **New - not described yet** (the page reads the GitHub repo list each time it opens) until it gets an entry in `projects.json`.

## Adding a new project
1. Add an entry to `projects.json`: `repo` (exact GitHub name), `title`, `category`, `description`, `site` (live page URL, or `null` if it runs locally).
2. Commit and push; the page and its PDF update in a minute or two.
3. Optional: `make_pdf.bat` for a timestamped copy of the template PDF on the PC.

## Files
| File | What |
|---|---|
| `index.html` | the whole page |
| `projects.json` | names, categories, descriptions, live links |
| `build_projects_pdf.py` / `make_pdf.bat` | PDF from the F.O.C.U.S. PDF template (`FOCUS_Projects_GitHub_YYYYMMDD_HHMMSS.pdf`, clickable links); needs `pip install reportlab` |
| `.github/workflows/pdf.yml` | builds `data/FOCUS_Projects_latest.pdf` on GitHub (the Save PDF button's file) |
| `start.bat` | opens the live page |
| `backup_all.bat` | timestamped copies into `backups\` before editing |

For personal research only, not financial advice. © 2026 Jachbit. All rights reserved. · [linktr.ee/jachbit](https://linktr.ee/jachbit)

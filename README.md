# F.O.C.U.S.© Projects

**Jachbit 2026** · Every public F.O.C.U.S. project on GitHub in one place, with a link to its live page and its code.

**Open it:** https://jachbit.github.io/FOCUS-Projects/

## What it does
- Cards grouped by category (Trading Tools, Trading References, Everyday Tools, Community, Wellness), each with **▶ Open page** (the live GitHub Pages site) and **</> Code** (the repo), plus a Live page / Runs locally badge and the last-updated date.
- Search box and category filters.
- **Save PDF**: prints a white, ink-saving version with every link written out in full and clickable, named `FOCUS_Projects_YYYYMMDD_HHMMSS` (pick *Save as PDF* in the print box). The subtitle line says the date, the count and the filter or search used.
- A new public repo shows up on its own under **New - not described yet** (the page reads the GitHub repo list each time it opens) until it gets an entry in `projects.json`.

## Adding a new project
1. Add an entry to `projects.json`: `repo` (exact GitHub name), `title`, `category`, `description`, `site` (live page URL, or `null` if it runs locally).
2. Commit and push; the page updates in about a minute.
3. Optional: `make_pdf.bat` for a fresh template PDF.

## Files
| File | What |
|---|---|
| `index.html` | the whole page |
| `projects.json` | names, categories, descriptions, live links |
| `build_projects_pdf.py` / `make_pdf.bat` | PDF from the F.O.C.U.S. PDF template (`FOCUS_Projects_GitHub_YYYYMMDD_HHMMSS.pdf`, clickable links); needs `pip install reportlab` |
| `start.bat` | opens the live page |
| `backup_all.bat` | timestamped copies into `backups\` before editing |

For personal research only, not financial advice. © 2026 Jachbit. All rights reserved. · [linktr.ee/jachbit](https://linktr.ee/jachbit)

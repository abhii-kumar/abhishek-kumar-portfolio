# Abhishek Kumar — Data Analyst & Business Automation

Existing Django portfolio upgraded with a clean white / violet theme and a realistic, scrollable laptop showcase. No npm build, external font, icon CDN or API key is required.

## Run on Windows (PowerShell)
Extract the ZIP into a new folder. Open the folder containing manage.py in a terminal:

```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe manage.py migrate
.\.venv\Scripts\python.exe manage.py runserver
```

Open http://127.0.0.1:8000/ . Do not open templates/index.html directly; Django must render static paths, CSRF tokens and the contact form.

## macOS / Linux
```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python manage.py migrate
.venv/bin/python manage.py runserver
```

## New laptop showcase
- Scroll or swipe **inside the laptop screen** to explore the portfolio. The rest of the page scrolls normally outside it.
- Switch between Portfolio, Team Seeds, Expense Claims and Blinkit with the tabs. Arrow keys, Home and End also work when a tab is focused.
- Your real photo appears in a circular grayscale portrait with a soft multicolour halo; hover restores its colour.
- Desktop pointer movement adds a gentle laptop tilt. Scroll reveals and card hover effects respect reduced-motion preferences.
- Project previews use your actual screenshots and existing project descriptions; they do not embed the private applications.
- `preview/` contains screenshots of the finished desktop and mobile design.

## What is preserved
- Existing views, routes, models, forms, migrations, settings and admin.
- Contact submissions are saved in SQLite, not sent by email. Run `python manage.py createsuperuser`, then use `/admin/` to read them.
- Project detail dialogs and filters, three-page process notebook, light/dark theme.
- Existing `/api/pulses/` endpoint remains available; distracting cursor/pulse animations are removed from the frontend.
- Original resume PDF and source images are included. The page serves optimized WebP copies.
- No existing database was supplied. `migrate` creates one. When updating an existing installation, retain its db.sqlite3 file and configured environment.

## Edit content
- `templates/base.html`: document shell and local SVG icon symbols.
- `templates/index.html`: page content and accessible form markup.
- `static/css/variables.css`: theme tokens.
- `static/css/base.css`: layout primitives and typography.
- `static/css/components.css`: components.
- `static/css/laptop.css`: laptop hardware frame, scrollable preview, portrait halo and preview cards.
- `static/css/responsive.css`: breakpoints and reduced motion.
- `templates/portfolio/laptop_projects.html`: the three project previews.
- `static/js/app.js`: menu, theme, filters, dialogs and notebook.
- `portfolio/content.json`: dialog descriptions and real project URLs. Unknown project URLs remain absent, not placeholder links.

## Validation
```bash
python manage.py check
python manage.py test
```
Optional browser QA (development dependency only):
```bash
python -m pip install playwright
python -m playwright install chromium
python qa/browser_check.py
```
The browser check starts its own local server and tests all ten requested widths, with overflow clipping disabled during measurement, theme persistence, menu navigation, filters, dialogs, preview tabs, keyboard controls, independent wheel scrolling, mobile touch swipes and reduced motion. See CHANGELOG.md for this delivery's verification results.

For deployment, set DJANGO_DEBUG=0, DJANGO_SECRET_KEY and DJANGO_ALLOWED_HOSTS; serve collected static files with a production server. Local runserver is for development.

# Laptop showcase upgrade — 30 September 2026

## Requested reference treatment
- Built a realistic laptop from HTML/CSS with a metallic base, screen bezel, camera and soft shadow.
- Added an independently scrollable portfolio screen with the supplied photo in a circular grayscale treatment and a pink / purple / blue halo. Hover transitions back to colour. The original photo is unchanged.
- Added four preview tabs: Portfolio, Team Seeds, Expense Claims and Blinkit. Real screenshots, project details and contact links are used throughout.
- Added capability cards, a screen scroll indicator, an in-screen next-section button and a screen reset control.
- Added a subtle desktop-only pointer tilt, scroll reveals and card hover effects. Reduced-motion mode disables movement.
- Updated the full page to a white / charcoal / violet theme, with a matching dark mode.

## Files changed in this upgrade
- `templates/base.html`, `templates/index.html`, `static/js/app.js`.
- `static/css/variables.css`, `base.css`, `components.css`, `responsive.css`.
- New `templates/portfolio/laptop_projects.html` and `static/css/laptop.css`.
- Updated README, browser QA and saved test results; added preview screenshots.
- Existing Django views, forms, models, admin, settings, routes, migration, project data and resume are unchanged.

## Verification
- Django checks and all three existing backend tests passed.
- All ten widths passed: 1920, 1440, 1366, 1280, 1024, 768, 430, 390, 375, 360 px.
- No horizontal page overflow with clipping disabled, and no horizontal overflow in project screens.
- Preview tabs, arrow-key/Home navigation, independent mouse-wheel scroll, screen reset, native mobile swipe and reduced-motion behavior passed.
- Existing menu, theme persistence, filters and project dialogs passed. No browser exceptions or failed HTTP assets were recorded.
- Desktop, mobile, scrolled-screen and dark-mode screenshots visually reviewed.

## Run
Same commands as before. Extract into a new folder, install `requirements.txt`, run `python manage.py migrate`, then `python manage.py runserver`. See README for copy/paste Windows commands. Keep your existing `db.sqlite3` if moving saved contact messages into this version.

---

## Previous repair notes

# Portfolio frontend repair

## Findings from the supplied project
- The old 42 KB stylesheet layered multiple unrelated themes and repeated selectors. The final project-card layer forced dimensions, colors and display with many `!important` rules.
- Floating cards used rotated boxes, `right:-1%`, and labels at `right:-18px` with visible overflow. Decorations used fixed widths. These were concrete overflow risks.
- Project thumbnails were forced to 190/240 px heights and cover cropping; metadata fell to 7–11 px. The header had a fixed brand minimum width and no mobile menu control; navigation was simply hidden.
- There was only ONE portrait in the supplied template, already inside a positioned showcase. Its massive standalone appearance and unstyled header cannot be conclusively reproduced from source alone; missing or stale CSS on the original running site is a likely cause, not a proven diagnosis. No broken-page screenshot or server log was included in these attachments. Static paths in the ZIP were valid.
- Obsolete JS still targeted removed scenes/charts/cursor effects. Unicode icon characters depended on font support. Theme storage errors could interrupt the old script.

## Files changed
- Added `templates/base.html`; refactored `templates/index.html`.
- Replaced `static/css/style.css` with variables/base/components/responsive stylesheets.
- Rewrote `static/js/app.js`; added four optimized WebP assets.
- Updated README, added this changelog and optional `qa/browser_check.py`.
- Existing backend files, migration, project data, original images and resume remain unchanged.

## Fixes
- Bounded two-column hero, one contained transparent portrait, three browser-style screenshot cards.
- Consistent 1280 px maximum container; no 100vw or oversized fixed-width layout.
- Sticky spaced navbar, education anchor, accessible hamburger, active links.
- Local SVG icons; warm light/dark token system; no external asset dependency.
- Three-column project cards, consistent 16:9 contained screenshots, readable text, functioning filters/dialogs.
- Five skill categories, education score corrected to the supplied 91.2%, visible contact validation errors, resume/contact links.
- Mobile hero places the portrait and compact previews before two-column stats; cards become one column. Reduced-motion support and focus states retained.

## Image optimization
The four displayed assets total approximately 182 KB versus 3.21 MB for their originals (about 94% smaller). Portrait is an 850 px transparent WebP, with intrinsic dimensions and high fetch priority. Source portrait/cutout and screenshots remain included. Existing cutout transparency is preserved; no new likeness is synthesized.

## Run
Follow README.md: install requirements, run `python manage.py migrate`, then `python manage.py runserver` and open http://127.0.0.1:8000/ .

## Verification
- Django 5.2.17: `manage.py check` passed.
- All three existing backend tests passed, including contact persistence/validation and CSRF.
- Migrations applied successfully in a temporary local database.
- Development server homepage, all referenced CSS/JS/images, and the actual resume PDF returned HTTP 200.
- JavaScript syntax check passed.
- Chromium browser checks passed at 1920, 1440, 1366, 1280, 1024, 768, 430, 390, 375 and 360 px. scrollWidth == clientWidth at every width with clipping temporarily disabled; no main-content element escaped the viewport.
- Menu, education navigation, theme persistence, filters and modal opening/Escape close passed at all sizes. No JavaScript exceptions or HTTP asset failures.
- Full-page screenshots visually reviewed at desktop and mobile; final desktop hero reviewed at 1366×768. Test output is included in qa/browser-results.json. External social destination contents were not audited; supplied URLs are preserved.

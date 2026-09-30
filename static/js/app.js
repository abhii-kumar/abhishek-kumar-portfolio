'use strict';
const theme = document.querySelector('#theme-toggle');
function applyTheme(dark) {
  document.body.dataset.theme = dark ? 'dark' : 'light';
  theme.setAttribute('aria-pressed', String(dark));
  theme.setAttribute('aria-label', dark ? 'Switch to light theme' : 'Switch to dark theme');
}
try { applyTheme(localStorage.getItem('portfolio-theme') === 'dark'); } catch (_) { applyTheme(false); }
theme.addEventListener('click', () => {
  const dark = document.body.dataset.theme !== 'dark'; applyTheme(dark);
  try { localStorage.setItem('portfolio-theme', dark ? 'dark' : 'light'); } catch (_) { /* Storage is optional. */ }
});
const menu = document.querySelector('#menu-toggle'), nav = document.querySelector('#main-nav');
function closeMenu() { nav.classList.remove('open'); menu.setAttribute('aria-expanded', 'false'); menu.setAttribute('aria-label', 'Open navigation'); }
menu.addEventListener('click', () => {
  const open = nav.classList.toggle('open'); menu.setAttribute('aria-expanded', String(open)); menu.setAttribute('aria-label', open ? 'Close navigation' : 'Open navigation');
});
nav.querySelectorAll('a').forEach(a => a.addEventListener('click', closeMenu));
document.addEventListener('keydown', e => { if (e.key === 'Escape' && nav.classList.contains('open')) { closeMenu(); menu.focus(); } });
matchMedia('(min-width: 1280px)').addEventListener('change', closeMenu);
const sections = document.querySelectorAll('main section[id]');
const observer = new IntersectionObserver(entries => entries.forEach(entry => {
  if (entry.isIntersecting) nav.querySelectorAll('a').forEach(a => { const active = a.hash === '#' + entry.target.id; a.classList.toggle('active', active); if(active) a.setAttribute('aria-current', 'location'); else a.removeAttribute('aria-current'); });
}), {rootMargin: '-15% 0px -60% 0px'});
sections.forEach(s => observer.observe(s));
const pages = [ ['Understand the business question.', 'Start with the decision that needs to be made, then identify the data that can support it.'], ['Clean, validate and explore.', 'Prepare reliable data, investigate patterns and test assumptions before building the final view.'], ['Communicate the insight.', 'Turn analysis into clear KPIs, dashboards or automation that people can actually use.'] ];
let page = 0;
function turn(d) { page = (page + d + pages.length) % pages.length; document.querySelector('#page-number').textContent = `0${page + 1} / 03`; document.querySelector('#page-title').textContent = pages[page][0]; document.querySelector('#page-copy').textContent = pages[page][1]; }
document.querySelector('#prev').addEventListener('click', () => turn(-1));
document.querySelector('#next').addEventListener('click', () => turn(1));
const content = JSON.parse(document.querySelector('#project-content').textContent), dialog = document.querySelector('#project-dialog');
document.querySelectorAll('.case-link').forEach((b, i) => b.addEventListener('click', () => {
  const p = content[i]; dialog.querySelector('h2').textContent = p.title; document.querySelector('#project-description').textContent = p.description;
  const stack = document.querySelector('#project-stack'); stack.replaceChildren(); p.tags.forEach(t => { const span = document.createElement('span'); span.textContent = t; stack.append(span); });
  const links = document.querySelector('#project-links'); links.replaceChildren();
  [['View project', p.live_url], ['Source code', p.source_url]].forEach(([label,url]) => { if (!url || !/^https?:\/\//.test(url)) return; const a = document.createElement('a'); a.href = url; a.target = '_blank'; a.rel = 'noopener noreferrer'; a.textContent = label; links.append(a); });
  dialog.showModal();
}));
document.querySelector('#close-dialog').addEventListener('click', () => dialog.close());
document.querySelector('#discuss').addEventListener('click', () => dialog.close());
document.querySelectorAll('[data-filter]').forEach(b => { b.setAttribute('aria-pressed', String(b.classList.contains('selected'))); b.addEventListener('click', () => {
  document.querySelectorAll('[data-filter]').forEach(x => { x.classList.toggle('selected', x === b); x.setAttribute('aria-pressed', String(x === b)); });
  document.querySelectorAll('[data-category]').forEach(c => { c.hidden = b.dataset.filter !== 'all' && b.dataset.filter !== c.dataset.category; });
}); });

// Independently scrollable laptop preview; native scrolling remains untouched.
const previewScreen = document.querySelector('#laptop-screen');
const previewTabs = [...document.querySelectorAll('[data-preview]')];
const previewPanels = [...document.querySelectorAll('.preview-panel')];
const reducedMotion = matchMedia('(prefers-reduced-motion: reduce)');
const progressFill = document.querySelector('#screen-progress-fill');
function updateScreenProgress() {
  const range = previewScreen.scrollHeight - previewScreen.clientHeight;
  progressFill.style.width = `${range > 0 ? previewScreen.scrollTop / range * 100 : 0}%`;
}
function setPreview(key, focusScreen = false) {
  const panel = document.querySelector(`#preview-${key}`);
  if (!panel) return;
  previewTabs.forEach(tab => {
    const selected = tab.dataset.preview === key;
    tab.setAttribute('aria-selected', String(selected));
    tab.tabIndex = selected ? 0 : -1;
  });
  previewPanels.forEach(item => { item.hidden = item !== panel; });
  previewScreen.scrollTo({top: 0, behavior: 'instant'});
  previewScreen.setAttribute('aria-label', `Scrollable ${key === 'overview' ? 'portfolio' : previewTabs.find(tab => tab.dataset.preview === key).textContent} preview`);
  updateScreenProgress();
  if (focusScreen) previewScreen.focus({preventScroll: true});
}
previewTabs.forEach((tab, index) => {
  tab.addEventListener('click', () => setPreview(tab.dataset.preview));
  tab.addEventListener('keydown', event => {
    let target;
    if (event.key === 'ArrowRight') target = (index + 1) % previewTabs.length;
    if (event.key === 'ArrowLeft') target = (index - 1 + previewTabs.length) % previewTabs.length;
    if (event.key === 'Home') target = 0;
    if (event.key === 'End') target = previewTabs.length - 1;
    if (target !== undefined) {
      event.preventDefault(); previewTabs[target].focus(); setPreview(previewTabs[target].dataset.preview);
    }
  });
});
document.querySelectorAll('[data-open-preview]').forEach(button => button.addEventListener('click', () => setPreview(button.dataset.openPreview, true)));
document.querySelector('[data-screen-next]').addEventListener('click', () => {
  const target = document.querySelector('#screen-capabilities');
  const top = target.getBoundingClientRect().top - previewScreen.getBoundingClientRect().top + previewScreen.scrollTop;
  previewScreen.scrollTo({top, behavior: reducedMotion.matches ? 'instant' : 'smooth'});
});
document.querySelector('#screen-reset').addEventListener('click', () => previewScreen.scrollTo({top:0, behavior:reducedMotion.matches ? 'instant' : 'smooth'}));
previewScreen.addEventListener('scroll', updateScreenProgress, {passive:true});
new ResizeObserver(updateScreenProgress).observe(previewScreen);
previewScreen.querySelectorAll('img').forEach(img => img.addEventListener('load', updateScreenProgress));

// Subtle desktop perspective, never applied to touch or reduced-motion devices.
const laptop = document.querySelector('#laptop');
const finePointer = matchMedia('(hover: hover) and (pointer: fine) and (min-width: 901px)');
let tiltFrame;
function resetTilt() {
  cancelAnimationFrame(tiltFrame);
  laptop.style.setProperty('--tilt-x', '0deg'); laptop.style.setProperty('--tilt-y', '0deg');
}
laptop.addEventListener('pointermove', event => {
  if (reducedMotion.matches || !finePointer.matches || event.pointerType === 'touch') return;
  const bounds = laptop.getBoundingClientRect();
  cancelAnimationFrame(tiltFrame);
  tiltFrame = requestAnimationFrame(() => {
    laptop.style.setProperty('--tilt-x', `${((event.clientY - bounds.top) / bounds.height - .5) * -1.8}deg`);
    laptop.style.setProperty('--tilt-y', `${((event.clientX - bounds.left) / bounds.width - .5) * 2}deg`);
  });
});
laptop.addEventListener('pointerleave', resetTilt);
finePointer.addEventListener('change', resetTilt);
reducedMotion.addEventListener('change', resetTilt);

// Content stays readable without JavaScript or when reduced motion is requested.
if (!reducedMotion.matches && 'IntersectionObserver' in window) {
  const reveal = new IntersectionObserver(entries => entries.forEach(entry => {
    if (entry.isIntersecting) { entry.target.classList.remove('reveal-pending'); reveal.unobserve(entry.target); }
  }), {threshold:.05});
  document.querySelectorAll('.section-head,.notebook,.timeline article,.case-card,.skill-groups article,.education-list article').forEach(element => {
    element.classList.add('reveal-target');
    if (element.getBoundingClientRect().top > innerHeight) element.classList.add('reveal-pending');
    reveal.observe(element);
  });
}

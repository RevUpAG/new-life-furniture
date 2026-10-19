// Mobile menu
const btn = document.querySelector('.menu-btn'), nav = document.querySelector('.nav');
btn.addEventListener('click', () => {
  const open = btn.getAttribute('aria-expanded') !== 'true';
  btn.setAttribute('aria-expanded', open); btn.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
  nav.classList.toggle('open', open); document.body.style.overflow = open ? 'hidden' : '';
});
document.addEventListener('keydown', ev => { if (ev.key === 'Escape' && nav.classList.contains('open')) { btn.click(); btn.focus(); } });
document.getElementById('yr').textContent = new Date().getFullYear();

// Services dropdown (click/tap; hover handled in CSS on desktop)
const subBtn = document.querySelector('.sub-btn');
subBtn.addEventListener('click', ev => { ev.stopPropagation(); subBtn.setAttribute('aria-expanded', subBtn.getAttribute('aria-expanded') !== 'true'); });
document.addEventListener('click', ev => { if (!ev.target.closest('.has-sub') && !nav.classList.contains('open')) subBtn.setAttribute('aria-expanded', 'false'); });
document.addEventListener('keydown', ev => { if (ev.key === 'Escape' && subBtn.getAttribute('aria-expanded') === 'true') { subBtn.setAttribute('aria-expanded', 'false'); subBtn.focus(); } });

// Reviews carousel (mobile): arrow buttons + counter
const track = document.getElementById('quotes');
if (track) {
  const [prev, next] = document.querySelectorAll('.car-btn'), count = document.querySelector('.car-count'), items = [...track.children];
  const idx = () => Math.round(track.scrollLeft / (items[0].offsetWidth + 16));
  const update = () => { const i = Math.min(idx(), items.length - 1); count.textContent = `${i + 1} / ${items.length}`; prev.disabled = i === 0; next.disabled = i >= items.length - 1; };
  document.querySelectorAll('.car-btn').forEach(b => b.addEventListener('click', () => {
    const i = Math.max(0, Math.min(items.length - 1, idx() + +b.dataset.dir));
    track.scrollTo({left: items[i].offsetLeft - items[0].offsetLeft, behavior: matchMedia('(prefers-reduced-motion: reduce)').matches ? 'auto' : 'smooth'});
  }));
  track.addEventListener('scroll', () => requestAnimationFrame(update), {passive: true});
  update();
}

// Header shadow on scroll
const hdr = document.querySelector('.site-header');
addEventListener('scroll', () => hdr.classList.toggle('scrolled', scrollY > 8), {passive: true});

// Scroll reveal: progressive enhancement that can never leave content hidden.
// Checks positions on scroll/resize (works for jumps, anchors, restored scroll) so any way of reaching a section reveals it.
if (!matchMedia('(prefers-reduced-motion: reduce)').matches) {
  let els = [...document.querySelectorAll('.section h2, .section .lead, .bento .card, .cards .card, .mosaic figure, .gallery figure, .steps li, .quote, .split > *, .path, .faq, .final-grid > *')]
    .filter(el => el.getBoundingClientRect().top > innerHeight);   // only animate what starts below the fold
  els.forEach((el, i) => { el.classList.add('rv'); el.style.transitionDelay = (i % 4) * 70 + 'ms'; });
  let ticking = false;
  const check = () => {
    ticking = false;
    els = els.filter(el => { if (el.getBoundingClientRect().top < innerHeight * 0.92) { el.classList.add('in'); return false; } return true; });
    if (!els.length) removeEventListener('scroll', onScroll);
  };
  const onScroll = () => { if (!ticking) { ticking = true; requestAnimationFrame(check); } };
  addEventListener('scroll', onScroll, {passive: true}); addEventListener('resize', onScroll);
  addEventListener('load', check); check();
}

// Analytics: contact clicks -> dataLayer (GTM forwards to GA4 / Google Ads). No personal data is pushed.
window.dataLayer = window.dataLayer || [];
document.addEventListener('click', ev => {
  const a = ev.target.closest('a[href^="tel:"],a[href^="mailto:"],a[href^="https://wa.me/"]');
  if (a) dataLayer.push({event: a.href.startsWith('tel:') ? 'click_call' : a.href.startsWith('mailto:') ? 'click_email' : 'click_whatsapp', click_location: a.dataset.ev || 'other'});
});

// Keep Google Ads click IDs for 90 days so a lead submitted on a later visit is still attributed.
const qs = new URLSearchParams(location.search), KEYS = ['gclid', 'gbraid', 'wbraid'];
try {
  KEYS.forEach(k => { if (qs.get(k)) localStorage.setItem('nlf_' + k, JSON.stringify({v: qs.get(k), t: Date.now()})); });
} catch (_) {}
const clickId = k => { try { const o = JSON.parse(localStorage.getItem('nlf_' + k)); return o && Date.now() - o.t < 7776e6 ? o.v : ''; } catch (_) { return ''; } };

// Estimate form
document.querySelectorAll('.lead-form').forEach(form => {
  const status = form.querySelector('.form-status'), submit = form.querySelector('[type=submit]');
  const showErr = (el, msg) => {
    el.setAttribute('aria-invalid', 'true');
    let m = el.parentElement.querySelector('.err');
    if (!m) { m = document.createElement('span'); m.className = 'err'; m.id = el.id + '-err'; el.parentElement.append(m); el.setAttribute('aria-describedby', m.id); }
    m.textContent = msg;
  };
  const clearErr = el => { el.removeAttribute('aria-invalid'); el.parentElement.querySelector('.err')?.remove(); el.removeAttribute('aria-describedby'); };
  form.addEventListener('input', ev => { if (ev.target.getAttribute('aria-invalid')) clearErr(ev.target); });

  form.addEventListener('submit', async ev => {
    ev.preventDefault();
    if (form.dataset.sent) return;                 // one lead per page view: no duplicate conversions
    const f = form.elements; let first = null;
    [[f.name, v => v.trim().length > 1, 'Please enter your name.'],
     [f.phone, v => v.replace(/\D/g, '').length >= 10, 'Please enter a valid phone number.'],
     [f.email, v => /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(v), 'Please enter a valid email address.']]
      .forEach(([el, ok, msg]) => { clearErr(el); if (!ok(el.value)) { showErr(el, msg); first = first || el; } });
    if (first) { first.focus(); status.className = 'form-status bad'; status.textContent = 'Please check the highlighted fields.'; return; }
    if (f._gotcha.value) return;                   // honeypot: silently drop bots

    KEYS.forEach(k => f[k].value = clickId(k)); f.page.value = location.pathname;
    const endpoint = form.dataset.endpoint;
    if (!endpoint) {
      // No backend configured yet: open the visitor's email app. Not counted as a conversion.
      const d = new FormData(form), body = ['name', 'phone', 'email', 'service', 'project_type', 'message'].map(k => `${k}: ${d.get(k) || ''}`).join('\n');
      location.href = `mailto:Ian@newlifefurniture.com?subject=${encodeURIComponent('Estimate request: ' + d.get('service'))}&body=${encodeURIComponent(body)}`;
      status.className = 'form-status'; status.textContent = 'Your email app should open with your request. Send it to complete, or call (954) 895-8504.';
      return;
    }
    submit.disabled = true; submit.textContent = 'Sending…'; status.className = 'form-status'; status.textContent = '';
    try {
      const r = await fetch('https://formspree.io/f/' + endpoint, {method: 'POST', body: new FormData(form), headers: {Accept: 'application/json'}});
      if (!r.ok) throw new Error(r.status);
      form.dataset.sent = '1';
      dataLayer.push({event: 'generate_lead', form_service: f.service.value, project_type: f.project_type.value}); // fired only after a confirmed submission
      form.reset(); submit.textContent = 'Sent';
      status.className = 'form-status ok'; status.textContent = 'Thank you! Your request was received. We will contact you shortly.';
      status.focus?.();
    } catch (_) {
      submit.disabled = false; submit.textContent = 'Send request';
      status.className = 'form-status bad'; status.textContent = 'Something went wrong. Please call (954) 895-8504 or email Ian@newlifefurniture.com.';
    }
  });
});

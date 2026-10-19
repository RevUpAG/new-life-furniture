// Mobile menu
const btn = document.querySelector('.menu-btn'), nav = document.querySelector('.nav');
btn.addEventListener('click', () => {
  const open = btn.getAttribute('aria-expanded') !== 'true';
  btn.setAttribute('aria-expanded', open); btn.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
  nav.classList.toggle('open', open); document.body.style.overflow = open ? 'hidden' : '';
});
document.addEventListener('keydown', ev => { if (ev.key === 'Escape' && nav.classList.contains('open')) { btn.click(); btn.focus(); } });
document.getElementById('yr').textContent = new Date().getFullYear();

// Analytics: contact clicks -> dataLayer (GTM forwards to GA4 / Google Ads). No personal data is pushed.
window.dataLayer = window.dataLayer || [];
document.addEventListener('click', ev => {
  const a = ev.target.closest('a[href^="tel:"],a[href^="mailto:"]');
  if (a) dataLayer.push({event: a.href.startsWith('tel:') ? 'click_call' : 'click_email', click_location: a.dataset.ev || 'other'});
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

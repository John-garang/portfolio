// Load footer across all pages
// Inject mobile-fixes.css on every page
const _mf = document.createElement('link');
_mf.rel = 'stylesheet';
_mf.href = '/static/mobile-fixes.css';
document.head.appendChild(_mf);

// Load brand-notifications.js on every page
const _bn = document.createElement('script');
_bn.src = '/static/brand-notifications.js';
document.head.appendChild(_bn);

// Load EmailJS SDK
const _ejs = document.createElement('script');
_ejs.src = 'https://cdn.jsdelivr.net/npm/@emailjs/browser@4/dist/email.min.js';
_ejs.integrity = 'sha256-yHo0BbFBgMOHFJFMGqHFJFMGqHFJFMGqHFJFMGqHFI=';
_ejs.crossOrigin = 'anonymous';
_ejs.onload = () => emailjs.init('jMid5j4K3IEfIlIr0');
document.head.appendChild(_ejs);

fetch('footer')
    .then(response => response.text())
    .then(data => {
        const placeholder = document.getElementById('footer-placeholder');
        const parser = new DOMParser();
        const doc = parser.parseFromString(data, 'text/html');
        while (doc.body.firstChild) {
            placeholder.appendChild(doc.body.firstChild);
        }
        // Attach event listener after footer is loaded
        const form = document.getElementById('newsletterForm');
        if (form) {
            form.addEventListener('submit', subscribeNewsletter);
        }
    });

window.subscribeNewsletter = function(e) {
    e.preventDefault();
    const form = document.getElementById('newsletterForm');
    const btn = form.querySelector('button[type="submit"]');
    const originalText = btn.innerHTML;
    btn.disabled = true;
    btn.innerHTML = '<i class="fas fa-spinner fa-spin"></i>';

    emailjs.send('service_7gb9zw8', 'template_4qclxwp', {
        firstName: document.getElementById('newsletterFirstName').value,
        lastName:  document.getElementById('newsletterLastName').value,
        email:     document.getElementById('newsletterEmail').value
    }).then(() => {
        if (typeof showBrandNotification === 'function') {
            showBrandNotification('success', 'Subscribed!', 'Thanks for subscribing — you\'ll hear from me soon.');
        }
        form.reset();
    }).catch(() => {
        if (typeof showBrandNotification === 'function') {
            showBrandNotification('error', 'Oops!', 'Subscription failed. Please try again.');
        }
    }).finally(() => {
        btn.disabled = false;
        btn.innerHTML = originalText;
    });
};
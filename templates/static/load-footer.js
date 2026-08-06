// Load footer across all pages
fetch('/footer')
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
            form.addEventListener('submit', function(e) {
                e.preventDefault();
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
            });
        }
    });

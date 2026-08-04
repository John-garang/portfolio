// Load footer across all pages
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

// subscribeNewsletter is defined in footer.html via EmailJS
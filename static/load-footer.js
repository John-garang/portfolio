// Load footer across all pages
fetch('footer.html')
    .then(response => response.text())
    .then(data => {
        document.getElementById('footer-placeholder').innerHTML = data;
        // Attach event listener after footer is loaded
        const form = document.getElementById('newsletterForm');
        if (form) {
            form.addEventListener('submit', subscribeNewsletter);
        }
    });

// Make function globally accessible
window.subscribeNewsletter = async function(e) {
    e.preventDefault();
    e.stopPropagation();
    const firstName = document.getElementById('newsletterFirstName').value;
    const lastName = document.getElementById('newsletterLastName').value;
    const email = document.getElementById('newsletterEmail').value;
    const btn = e.target.querySelector('button');
    btn.disabled = true;
    btn.innerHTML = '<i class="fas fa-spinner fa-spin"></i>';
    
    try {
        const response = await fetch('https://script.google.com/macros/s/AKfycbzmaa8ZuVQtieBEGlHAZcZPyNyp3WUX7ZMWtdoAylzj9CGPI-rNV3NJChAno2DbTljluQ/exec', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ formType: 'newsletter', email })
        });
        
        const result = await response.json();
        
        if (result.success) {
            window.popupSystem.success('Thank you for subscribing to our newsletter! You\'ll receive updates on our latest content and insights.', 'Successfully Subscribed!');
            document.getElementById('newsletterForm').reset();
        } else {
            window.popupSystem.error(result.message || 'Subscription failed. Please try again.', 'Subscription Failed');
        }
    } catch (error) {
        window.popupSystem.error('Unable to connect to the server. Please check your internet connection and try again.', 'Connection Error');
    } finally {
        btn.disabled = false;
        btn.innerHTML = '<i class="fas fa-paper-plane"></i>';
    }
};

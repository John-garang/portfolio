// Load footer across all pages
fetch('footer')
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
window.subscribeNewsletter = function(e) {
    e.preventDefault();
    e.stopPropagation();
    const email = document.getElementById('newsletterEmail').value;
    const btn = e.target.querySelector('button');
    btn.disabled = true;
    btn.innerHTML = '<i class="fas fa-spinner fa-spin"></i>';
    
    // Create hidden form for newsletter
    const form = document.createElement('form');
    form.method = 'POST';
    form.action = 'https://script.google.com/macros/s/AKfycbyIkrho7Kdvo19Ely41v6U7CNvtjO-oU4IsUqulvVlJHiPa5DuB3hgmhxNkwTEm7Q1XWQ/exec';
    form.target = 'hidden_iframe';
    form.style.display = 'none';
    
    const formTypeInput = document.createElement('input');
    formTypeInput.type = 'hidden';
    formTypeInput.name = 'formType';
    formTypeInput.value = 'newsletter';
    form.appendChild(formTypeInput);
    
    const emailInput = document.createElement('input');
    emailInput.type = 'hidden';
    emailInput.name = 'email';
    emailInput.value = email;
    form.appendChild(emailInput);
    
    const iframe = document.createElement('iframe');
    iframe.name = 'hidden_iframe';
    iframe.style.display = 'none';
    
    iframe.onload = () => {
        alert('Thank you for subscribing to our newsletter!');
        document.getElementById('newsletterForm').reset();
        document.body.removeChild(form);
        document.body.removeChild(iframe);
        btn.disabled = false;
        btn.innerHTML = '<i class="fas fa-paper-plane"></i>';
    };
    
    document.body.appendChild(iframe);
    document.body.appendChild(form);
    form.submit();
};
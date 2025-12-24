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
window.subscribeNewsletter = function(e) {
    e.preventDefault();
    e.stopPropagation();
    const firstName = document.getElementById('newsletterFirstName').value;
    const lastName = document.getElementById('newsletterLastName').value;
    const email = document.getElementById('newsletterEmail').value;
    const btn = e.target.querySelector('button');
    const originalHTML = btn.innerHTML;
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
    
    const nameInput = document.createElement('input');
    nameInput.type = 'hidden';
    nameInput.name = 'name';
    nameInput.value = firstName + ' ' + lastName;
    form.appendChild(nameInput);
    
    const emailInput = document.createElement('input');
    emailInput.type = 'hidden';
    emailInput.name = 'email';
    emailInput.value = email;
    form.appendChild(emailInput);
    
    const iframe = document.createElement('iframe');
    iframe.name = 'hidden_iframe';
    iframe.style.display = 'none';
    
    iframe.onload = () => {
        // Create custom notification
        const notification = document.createElement('div');
        notification.style.cssText = `
            position: fixed; top: 20px; right: 20px; z-index: 10000;
            background: #4CAF50; color: white; padding: 15px 20px;
            border-radius: 8px; box-shadow: 0 4px 12px rgba(0,0,0,0.15);
            font-family: Arial, sans-serif; font-size: 14px;
            max-width: 350px; animation: slideIn 0.3s ease;
        `;
        notification.innerHTML = `
            <div style="display: flex; align-items: center; gap: 10px;">
                <i class="fas fa-check-circle" style="font-size: 18px;"></i>
                <span>Thanks ${firstName}! You're subscribed to our newsletter.</span>
                <button onclick="this.parentElement.parentElement.remove()" style="
                    background: none; border: none; color: white; font-size: 18px;
                    cursor: pointer; margin-left: auto; padding: 0;
                ">&times;</button>
            </div>
        `;
        
        // Add animation
        const style = document.createElement('style');
        style.textContent = '@keyframes slideIn { from { transform: translateX(100%); } to { transform: translateX(0); } }';
        document.head.appendChild(style);
        
        document.body.appendChild(notification);
        
        // Auto remove after 5 seconds
        setTimeout(() => {
            if (notification.parentElement) notification.remove();
        }, 5000);
        
        document.getElementById('newsletterForm').reset();
        document.body.removeChild(form);
        document.body.removeChild(iframe);
        btn.disabled = false;
        btn.innerHTML = originalHTML;
    };
    
    document.body.appendChild(iframe);
    document.body.appendChild(form);
    form.submit();
};

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
    
    // Prevent multiple executions
    if (e.target.submitting) return;
    e.target.submitting = true;
    
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
    form.target = 'hidden_iframe_' + Date.now();
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
    iframe.name = form.target;
    iframe.style.display = 'none';
    
    let notificationShown = false;
    iframe.onload = () => {
        if (notificationShown) return;
        notificationShown = true;
        
        // Create custom notification
        const notification = document.createElement('div');
        notification.style.cssText = `
            position: fixed; top: 50%; left: 50%; transform: translate(-50%, -50%); z-index: 10000;
            background: #4CAF50; color: white; padding: 20px 30px;
            border-radius: 8px; box-shadow: 0 4px 12px rgba(0,0,0,0.15);
            font-family: Arial, sans-serif; font-size: 16px; text-align: center;
            min-width: 300px; animation: fadeIn 0.3s ease;
        `;
        notification.innerHTML = `
            <div>
                <i class="fas fa-check-circle" style="font-size: 24px; margin-bottom: 10px; display: block;"></i>
                <div>Thanks ${firstName}!</div>
                <div style="margin-top: 5px; font-size: 14px; opacity: 0.9;">You're subscribed to our newsletter.</div>
                <button onclick="this.parentElement.parentElement.remove()" style="
                    background: rgba(255,255,255,0.2); border: none; color: white; 
                    padding: 8px 16px; border-radius: 4px; cursor: pointer; 
                    margin-top: 15px; font-size: 14px;
                ">Close</button>
            </div>
        `;
        
        // Add animation if not exists
        if (!document.querySelector('#fadeInAnimation')) {
            const style = document.createElement('style');
            style.id = 'fadeInAnimation';
            style.textContent = '@keyframes fadeIn { from { opacity: 0; transform: translate(-50%, -50%) scale(0.8); } to { opacity: 1; transform: translate(-50%, -50%) scale(1); } }';
            document.head.appendChild(style);
        }
        
        document.body.appendChild(notification);
        
        // Auto remove after 4 seconds
        setTimeout(() => {
            if (notification.parentElement) notification.remove();
        }, 4000);
        
        document.getElementById('newsletterForm').reset();
        document.body.removeChild(form);
        document.body.removeChild(iframe);
        btn.disabled = false;
        btn.innerHTML = originalHTML;
        e.target.submitting = false;
    };
    
    document.body.appendChild(iframe);
    document.body.appendChild(form);
    form.submit();
};

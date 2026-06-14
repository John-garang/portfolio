// Contact Form Handler - Saves to Admin Backend
function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.style.cssText = `
        position: fixed; top: 20px; right: 20px; z-index: 10000;
        background: ${type === 'success' ? '#4CAF50' : type === 'error' ? '#f44336' : '#2196F3'};
        color: white; padding: 16px 24px; border-radius: 4px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        font-family: Arial, sans-serif; font-size: 14px;
        max-width: 300px; animation: slideIn 0.3s ease;
    `;
    notification.textContent = message;
    
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.style.animation = 'slideOut 0.3s ease';
        setTimeout(() => notification.remove(), 300);
    }, 4000);
}

document.addEventListener('DOMContentLoaded', function() {
    const contactForm = document.querySelector('.professional-contact-form, .contact-form');
    
    if (contactForm) {
        contactForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            // Get form data
            const formData = {
                name: this.querySelector('input[placeholder*="name" i], input[name="name"]')?.value || '',
                email: this.querySelector('input[type="email"]')?.value || '',
                subject: this.querySelector('input[placeholder*="subject" i], select')?.value || 'General Inquiry',
                message: this.querySelector('textarea')?.value || ''
            };
            
            // Validate
            if (!formData.name || !formData.email || !formData.message) {
                showNotification('Please fill in all required fields', 'error');
                return;
            }
            
            // Save to backend
            if (typeof AdminBackend !== 'undefined') {
                AdminBackend.addMessage(formData);
                
                // Update analytics
                const analytics = AdminBackend.getAnalytics();
                AdminBackend.updateAnalytics('contactForms', analytics.contactForms + 1);
            }
            
            // Show success message
            showNotification('Thank you! Your message has been sent successfully.', 'success');
            this.reset();
        });
    }
});


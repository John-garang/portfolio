// Form Handler for Google Apps Script Integration
const APPS_SCRIPT_URL = 'https://script.google.com/macros/s/AKfycbwB77DBzA1M_FmV5nV9Yz3TtUJgVWnylnQ78jhqcTPQgD1c19hcY0O7-9XuA0iLun3JIA/exec';

// Contact Form Handler
function handleContactForm(formElement) {
    formElement.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        const submitBtn = this.querySelector('.submit-btn');
        const originalText = submitBtn.innerHTML;
        
        // Show loading state
        submitBtn.disabled = true;
        submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Sending...';
        
        // Collect form data
        const formData = {
            formType: 'contact',
            name: this.querySelector('#firstName').value + ' ' + this.querySelector('#lastName').value,
            email: this.querySelector('#email').value,
            phone: this.querySelector('#phone').value,
            company: this.querySelector('#company').value,
            service: this.querySelector('#service').value,
            budget: this.querySelector('#budget').value,
            timeline: this.querySelector('#timeline').value,
            message: this.querySelector('#message').value
        };
        
        try {
            const response = await fetch(APPS_SCRIPT_URL, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(formData)
            });
            
            const result = await response.json();
            
            if (result.success) {
                showNotification('Thank you! Your message has been sent successfully.', 'success');
                this.reset();
            } else {
                showNotification('Error: ' + result.message, 'error');
            }
        } catch (error) {
            showNotification('Error sending message. Please try again later.', 'error');
        }
        
        // Reset button
        submitBtn.disabled = false;
        submitBtn.innerHTML = originalText;
    });
}

// Newsletter Form Handler
function handleNewsletterForm(formElement) {
    formElement.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        const submitBtn = this.querySelector('button[type="submit"]');
        const originalText = submitBtn.innerHTML;
        
        // Show loading state
        submitBtn.disabled = true;
        submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Subscribing...';
        
        // Collect form data
        const formData = {
            formType: 'newsletter',
            email: this.querySelector('input[type="email"]').value
        };
        
        try {
            const response = await fetch(APPS_SCRIPT_URL, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(formData)
            });
            
            const result = await response.json();
            
            if (result.success) {
                showNotification('Successfully subscribed to newsletter!', 'success');
                this.reset();
            } else {
                showNotification('Error: ' + result.message, 'error');
            }
        } catch (error) {
            showNotification('Error subscribing. Please try again later.', 'error');
        }
        
        // Reset button
        submitBtn.disabled = false;
        submitBtn.innerHTML = originalText;
    });
}

// Notification System
function showNotification(message, type = 'info') {
    // Remove existing notifications
    const existing = document.querySelector('.form-notification');
    if (existing) existing.remove();
    
    // Create notification
    const notification = document.createElement('div');
    notification.className = `form-notification ${type}`;
    notification.innerHTML = `
        <i class="fas fa-${type === 'success' ? 'check-circle' : 'exclamation-circle'}"></i>
        <span>${message}</span>
        <button onclick="this.parentElement.remove()" class="close-btn">×</button>
    `;
    
    // Add styles
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: ${type === 'success' ? '#4CAF50' : '#f44336'};
        color: white;
        padding: 15px 20px;
        border-radius: 5px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        z-index: 10000;
        display: flex;
        align-items: center;
        gap: 10px;
        max-width: 400px;
    `;
    
    document.body.appendChild(notification);
    
    // Auto remove after 5 seconds
    setTimeout(() => {
        if (notification.parentElement) {
            notification.remove();
        }
    }, 5000);
}

// Initialize form handlers when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    // Contact form
    const contactForm = document.querySelector('.professional-contact-form');
    if (contactForm) {
        handleContactForm(contactForm);
    }
    
    // Newsletter forms
    const newsletterForms = document.querySelectorAll('.newsletter-form');
    newsletterForms.forEach(form => {
        handleNewsletterForm(form);
    });
    
    // Homepage contact form
    const homeContactForm = document.querySelector('.contact-form');
    if (homeContactForm) {
        homeContactForm.addEventListener('submit', async function(e) {
            e.preventDefault();
            
            const formData = {
                formType: 'contact',
                name: this.querySelector('input[placeholder="Your Name"]').value,
                email: this.querySelector('input[placeholder="Your Email"]').value,
                message: this.querySelector('input[placeholder="Subject"]').value + '\n\n' + this.querySelector('textarea').value
            };
            
            try {
                const response = await fetch(APPS_SCRIPT_URL, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(formData)
                });
                
                const result = await response.json();
                
                if (result.success) {
                    showNotification('Thank you! Your message has been sent successfully.', 'success');
                    this.reset();
                } else {
                    showNotification('Error: ' + result.message, 'error');
                }
            } catch (error) {
                showNotification('Error sending message. Please try again later.', 'error');
            }
        });
    }
});
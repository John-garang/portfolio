// Contact Form Handler - Saves to Admin Backend
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
                alert('Please fill in all required fields');
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
            alert('Thank you! Your message has been sent successfully.');
            this.reset();
        });
    }
});

// Simple popup system for admin dashboard
window.popupSystem = {
    success: function(message, title = 'Success') {
        this.show(message, title, 'success');
    },
    
    error: function(message, title = 'Error') {
        this.show(message, title, 'error');
    },
    
    warning: function(message, title = 'Warning') {
        this.show(message, title, 'warning');
    },
    
    info: function(message, title = 'Info') {
        this.show(message, title, 'info');
    },
    
    show: function(message, title, type) {
        // Create popup container if it doesn't exist
        let container = document.getElementById('popup-container');
        if (!container) {
            container = document.createElement('div');
            container.id = 'popup-container';
            document.body.appendChild(container);
        }
        
        // Create popup overlay
        const overlay = document.createElement('div');
        overlay.className = 'custom-popup-overlay';
        
        // Create popup content
        const popup = document.createElement('div');
        popup.className = 'custom-popup';
        
        const iconMap = {
            success: 'fas fa-check-circle',
            error: 'fas fa-exclamation-circle',
            warning: 'fas fa-exclamation-triangle',
            info: 'fas fa-info-circle'
        };
        
        popup.innerHTML = `
            <button class="popup-close" onclick="this.closest('.custom-popup-overlay').remove()">&times;</button>
            <div class="popup-header">
                <div class="popup-icon ${type}">
                    <i class="${iconMap[type]}"></i>
                </div>
                <h3 class="popup-title">${title}</h3>
            </div>
            <div class="popup-message">${message}</div>
            <div class="popup-actions">
                <button class="popup-btn primary" onclick="this.closest('.custom-popup-overlay').remove()">OK</button>
            </div>
        `;
        
        overlay.appendChild(popup);
        container.appendChild(overlay);
        
        // Show popup with animation
        setTimeout(() => overlay.classList.add('show'), 10);
        
        // Auto-close after 5 seconds for success messages
        if (type === 'success') {
            setTimeout(() => {
                if (overlay.parentNode) {
                    overlay.remove();
                }
            }, 5000);
        }
        
        // Close on overlay click
        overlay.addEventListener('click', (e) => {
            if (e.target === overlay) {
                overlay.remove();
            }
        });
    }
};

// Fallback alert system if popup system fails
window.alert = function(message) {
    if (window.popupSystem) {
        window.popupSystem.info(message);
    } else {
        // Use native alert as last resort
        window.originalAlert(message);
    }
};

// Store original alert
window.originalAlert = window.alert;

// Enhanced confirm function
window.confirm = function(message) {
    return new Promise((resolve) => {
        if (window.popupSystem) {
            const container = document.getElementById('popup-container') || document.body;
            const overlay = document.createElement('div');
            overlay.className = 'custom-popup-overlay show';
            
            const popup = document.createElement('div');
            popup.className = 'custom-popup';
            popup.innerHTML = `
                <div class="popup-header">
                    <div class="popup-icon warning">
                        <i class="fas fa-question-circle"></i>
                    </div>
                    <h3 class="popup-title">Confirm Action</h3>
                </div>
                <div class="popup-message">${message}</div>
                <div class="popup-actions">
                    <button class="popup-btn primary" onclick="confirmResult(true)">Yes</button>
                    <button class="popup-btn secondary" onclick="confirmResult(false)">Cancel</button>
                </div>
            `;
            
            overlay.appendChild(popup);
            container.appendChild(overlay);
            
            window.confirmResult = function(result) {
                overlay.remove();
                delete window.confirmResult;
                resolve(result);
            };
        } else {
            resolve(window.originalConfirm(message));
        }
    });
};

// Store original confirm
window.originalConfirm = window.confirm;

console.log('Popup system loaded successfully');
// Global Custom Popup System
class PopupSystem {
    constructor() {
        this.createPopupContainer();
        this.overrideAlert();
        this.overrideConfirm();
    }

    createPopupContainer() {
        if (document.getElementById('popup-container')) return;
        
        if (!document.body) return;
        const container = document.createElement('div');
        container.id = 'popup-container';
        document.body.appendChild(container);
    }

    show(options = {}) {
        const {
            type = 'info',
            title = '',
            message = '',
            showClose = true,
            buttons = [{ text: 'OK', action: 'close', primary: true }],
            onClose = null,
            autoClose = null
        } = options;

        const overlay = document.createElement('div');
        overlay.className = 'custom-popup-overlay';
        
        const popup = document.createElement('div');
        popup.className = 'custom-popup';

        const iconMap = {
            success: 'fas fa-check',
            error: 'fas fa-times',
            warning: 'fas fa-exclamation-triangle',
            info: 'fas fa-info-circle',
            loading: 'fas fa-spinner fa-spin'
        };

        popup.innerHTML = `
            ${showClose ? '<button class="popup-close" onclick="this.closest(\'.custom-popup-overlay\').remove()">&times;</button>' : ''}
            <div class="popup-header">
                <div class="popup-icon ${type}">
                    <i class="${iconMap[type]}"></i>
                </div>
                ${title ? `<h3 class="popup-title">${title}</h3>` : ''}
            </div>
            <div class="popup-content">
                <p class="popup-message">${message}</p>
                ${type === 'loading' ? '<div class="popup-loading"><div class="loading-spinner"></div><span>Please wait...</span></div>' : ''}
                <div class="popup-actions">
                    ${buttons.map(btn => `
                        <button class="popup-btn ${btn.primary ? 'primary' : 'secondary'}" 
                                onclick="window.popupSystem.handleAction('${btn.action}', this)">
                            ${btn.text}
                        </button>
                    `).join('')}
                </div>
            </div>
        `;

        overlay.appendChild(popup);
        document.getElementById('popup-container').appendChild(overlay);

        // Store callback for later use
        overlay._onClose = onClose;
        overlay._buttons = buttons;

        // Show with animation
        setTimeout(() => overlay.classList.add('show'), 10);

        // Auto close
        if (autoClose) {
            setTimeout(() => {
                if (overlay.parentNode) {
                    this.closePopup(overlay);
                }
            }, autoClose);
        }

        // Close on overlay click
        overlay.addEventListener('click', (e) => {
            if (e.target === overlay) {
                this.closePopup(overlay);
            }
        });

        return overlay;
    }

    handleAction(action, button) {
        const overlay = button.closest('.custom-popup-overlay');
        const buttonConfig = overlay._buttons.find(btn => btn.action === action);
        
        if (buttonConfig && buttonConfig.callback) {
            const result = buttonConfig.callback();
            if (result === false) return; // Prevent closing if callback returns false
        }

        if (action === 'close' || !buttonConfig || buttonConfig.close !== false) {
            this.closePopup(overlay);
        }
    }

    closePopup(overlay) {
        overlay.classList.remove('show');
        setTimeout(() => {
            if (overlay.parentNode) {
                if (overlay._onClose) overlay._onClose();
                overlay.remove();
            }
        }, 300);
    }

    // Success popup
    success(message, title = 'Success!', options = {}) {
        return this.show({
            type: 'success',
            title,
            message,
            autoClose: 3000,
            ...options
        });
    }

    // Error popup
    error(message, title = 'Error', options = {}) {
        return this.show({
            type: 'error',
            title,
            message,
            ...options
        });
    }

    // Warning popup
    warning(message, title = 'Warning', options = {}) {
        return this.show({
            type: 'warning',
            title,
            message,
            ...options
        });
    }

    // Info popup
    info(message, title = 'Information', options = {}) {
        return this.show({
            type: 'info',
            title,
            message,
            ...options
        });
    }

    // Loading popup
    loading(message = 'Loading...', title = '') {
        return this.show({
            type: 'loading',
            title,
            message,
            showClose: false,
            buttons: []
        });
    }

    // Confirm popup
    confirm(message, title = 'Confirm', options = {}) {
        return new Promise((resolve) => {
            this.show({
                type: 'warning',
                title,
                message,
                buttons: [
                    {
                        text: 'Cancel',
                        action: 'cancel',
                        callback: () => resolve(false)
                    },
                    {
                        text: 'OK',
                        action: 'confirm',
                        primary: true,
                        callback: () => resolve(true)
                    }
                ],
                ...options
            });
        });
    }

    // Override native alert
    overrideAlert() {
        window.originalAlert = window.alert;
        window.alert = (message) => {
            this.info(message, 'Alert');
        };
    }

    // Override native confirm
    overrideConfirm() {
        window.originalConfirm = window.confirm;
        window.confirm = (message) => {
            return this.confirm(message);
        };
    }

    // Restore native functions
    restoreNative() {
        if (window.originalAlert) {
            window.alert = window.originalAlert;
        }
        if (window.originalConfirm) {
            window.confirm = window.originalConfirm;
        }
    }
}

// Initialize the popup system after DOM loads
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
        window.popupSystem = new PopupSystem();
    });
} else {
    window.popupSystem = new PopupSystem();
}

// Export for module use
if (typeof module !== 'undefined' && module.exports) {
    module.exports = PopupSystem;
}

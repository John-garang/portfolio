// Brand Notifications System
function showBrandNotification(type, title, message) {
    // Remove any existing notifications
    const existing = document.querySelector('.brand-notification');
    if (existing) {
        existing.remove();
    }

    // Create notification element
    const notification = document.createElement('div');
    notification.className = `brand-notification brand-notification-${type}`;
    notification.innerHTML = `
        <div class="notification-content">
            <div class="notification-icon">
                <i class="fas fa-${type === 'success' ? 'check-circle' : type === 'error' ? 'exclamation-circle' : 'info-circle'}"></i>
            </div>
            <div class="notification-text">
                <h4>${title}</h4>
                <p>${message}</p>
            </div>
            <button class="notification-close" onclick="this.parentElement.remove()">
                <i class="fas fa-times"></i>
            </button>
        </div>
    `;

    // Add styles if not already added
    if (!document.getElementById('notification-styles')) {
        const styles = document.createElement('style');
        styles.id = 'notification-styles';
        styles.textContent = `
            .brand-notification {
                position: fixed;
                top: 20px;
                right: 20px;
                max-width: 400px;
                padding: 1rem;
                border-radius: 8px;
                box-shadow: 0 4px 20px rgba(0,0,0,0.15);
                z-index: 10000;
                animation: slideIn 0.3s ease;
                font-family: 'Inter', sans-serif;
            }
            @keyframes slideIn {
                from { transform: translateX(100%); opacity: 0; }
                to { transform: translateX(0); opacity: 1; }
            }
            .brand-notification-success {
                background: linear-gradient(135deg, #16b2dc, #1a7fa0);
                color: white;
            }
            .brand-notification-error {
                background: linear-gradient(135deg, #1a7fa0, #0f5570);
                color: white;
            }
            .brand-notification-info {
                background: linear-gradient(135deg, #16b2dc, #1a7fa0);
                color: white;
            }
            .notification-content {
                display: flex;
                align-items: flex-start;
                gap: 1rem;
            }
            .notification-icon {
                font-size: 1.5rem;
                flex-shrink: 0;
            }
            .notification-text {
                flex: 1;
            }
            .notification-text h4 {
                margin: 0 0 0.25rem;
                font-size: 1rem;
                font-weight: 600;
            }
            .notification-text p {
                margin: 0;
                font-size: 0.875rem;
                opacity: 0.95;
            }
            .notification-close {
                background: none;
                border: none;
                color: white;
                cursor: pointer;
                font-size: 1.25rem;
                padding: 0;
                line-height: 1;
                opacity: 0.8;
                transition: opacity 0.2s;
            }
            .notification-close:hover {
                opacity: 1;
            }
            @media (max-width: 640px) {
                .brand-notification {
                    max-width: calc(100% - 40px);
                    top: 10px;
                    right: 20px;
                }
            }
        `;
        document.head.appendChild(styles);
    }

    // Add to page
    document.body.appendChild(notification);

    // Auto-remove after 5 seconds
    setTimeout(() => {
        if (notification.parentElement) {
            notification.style.animation = 'slideIn 0.3s ease reverse';
            setTimeout(() => notification.remove(), 300);
        }
    }, 5000);
}
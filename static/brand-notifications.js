// Brand-consistent notification system
function showBrandNotification(type, title, message) {
    // Remove existing notifications
    const existing = document.querySelector('.brand-notification');
    if (existing) existing.remove();
    
    // Create notification
    const notification = document.createElement('div');
    notification.className = 'brand-notification';
    notification.style.cssText = `
        position: fixed; top: 50%; left: 50%; transform: translate(-50%, -50%); z-index: 10000;
        background: white; padding: 2.5rem; border-radius: 20px; 
        box-shadow: 0 25px 50px rgba(0,0,0,0.15); font-family: 'Lato', sans-serif;
        text-align: center; min-width: 350px; max-width: 90vw;
        animation: brandPopupFadeIn 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        border-top: 4px solid #16b2dc;
    `;
    
    const iconMap = {
        success: 'fas fa-check',
        error: 'fas fa-exclamation-triangle',
        info: 'fas fa-info-circle'
    };
    
    const colorMap = {
        success: 'linear-gradient(135deg, #16b2dc, #1a9ec7)',
        error: 'linear-gradient(135deg, #dc3545, #c82333)',
        info: 'linear-gradient(135deg, #17a2b8, #138496)'
    };
    
    notification.innerHTML = `
        <div style="margin-bottom: 1.5rem;">
            <div style="
                width: 60px; height: 60px; background: ${colorMap[type]};
                border-radius: 50%; display: flex; align-items: center; justify-content: center;
                margin: 0 auto 1rem; box-shadow: 0 8px 20px rgba(22, 178, 220, 0.3);
            ">
                <i class="${iconMap[type]}" style="font-size: 24px; color: white;"></i>
            </div>
            <h3 style="
                font-family: 'Playfair Display', serif; font-size: 1.5rem; 
                color: #333; margin-bottom: 0.5rem; font-weight: 600;
            ">${title}</h3>
            <p style="
                color: #666; font-size: 1rem; line-height: 1.6; margin: 0;
            ">${message}</p>
        </div>
        <button onclick="this.parentElement.remove()" style="
            background: linear-gradient(135deg, #16b2dc, #1a9ec7); color: white;
            border: none; padding: 0.75rem 2rem; border-radius: 8px;
            font-family: 'Lato', sans-serif; font-weight: 600; cursor: pointer;
            transition: all 0.3s ease; box-shadow: 0 4px 15px rgba(22, 178, 220, 0.3);
        " onmouseover="this.style.transform='translateY(-2px)'; this.style.boxShadow='0 8px 25px rgba(22, 178, 220, 0.4)'" 
           onmouseout="this.style.transform='translateY(0)'; this.style.boxShadow='0 4px 15px rgba(22, 178, 220, 0.3)'">Close</button>
    `;
    
    // Add animation keyframes if not exists
    if (!document.querySelector('#brandPopupAnimations')) {
        const style = document.createElement('style');
        style.id = 'brandPopupAnimations';
        style.textContent = `
            @keyframes brandPopupFadeIn {
                from { opacity: 0; transform: translate(-50%, -50%) scale(0.8); }
                to { opacity: 1; transform: translate(-50%, -50%) scale(1); }
            }
        `;
        document.head.appendChild(style);
    }
    
    document.body.appendChild(notification);
    
    // Auto remove after 5 seconds
    setTimeout(() => {
        if (notification.parentElement) notification.remove();
    }, 5000);
}
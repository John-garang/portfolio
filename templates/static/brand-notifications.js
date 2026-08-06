// Brand Notifications System — centred modal style
function showBrandNotification(type, title, message) {
    const existing = document.querySelector('.bn-overlay');
    if (existing) existing.remove();

    if (!document.getElementById('bn-styles')) {
        const s = document.createElement('style');
        s.id = 'bn-styles';
        s.textContent = `
            .bn-overlay {
                position: fixed;
                inset: 0;
                background: rgba(0,0,0,0.45);
                display: flex;
                align-items: center;
                justify-content: center;
                z-index: 99999;
                padding: 1rem;
                animation: bn-fade-in 0.2s ease;
            }
            @keyframes bn-fade-in {
                from { opacity: 0; }
                to   { opacity: 1; }
            }
            .bn-modal {
                background: #fff;
                border-radius: 0;
                box-shadow: 0 20px 60px rgba(0,0,0,0.2);
                padding: 2.5rem 2rem 2rem;
                max-width: 420px;
                width: 100%;
                text-align: center;
                position: relative;
                animation: bn-slide-up 0.25s ease;
                font-family: 'Inter', sans-serif;
            }
            @keyframes bn-slide-up {
                from { transform: translateY(24px); opacity: 0; }
                to   { transform: translateY(0);    opacity: 1; }
            }
            .bn-icon-wrap {
                width: 64px;
                height: 64px;
                border-radius: 50%;
                display: flex;
                align-items: center;
                justify-content: center;
                margin: 0 auto 1.25rem;
                font-size: 1.75rem;
            }
            .bn-icon-wrap.success { background: #e8f8f5; color: #16b2dc; }
            .bn-icon-wrap.error   { background: #fdecea; color: #c0392b; }
            .bn-icon-wrap.info    { background: #e8f4fd; color: #16b2dc; }
            .bn-title {
                font-size: 1.2rem;
                font-weight: 700;
                color: #1a1a1a;
                margin: 0 0 0.5rem;
            }
            .bn-message {
                font-size: 0.92rem;
                color: #666;
                line-height: 1.6;
                margin: 0 0 1.75rem;
            }
            .bn-close-btn {
                background: #16b2dc;
                color: #fff;
                border: none;
                padding: 0.65rem 2rem;
                font-family: 'Inter', sans-serif;
                font-size: 0.9rem;
                font-weight: 600;
                cursor: pointer;
                border-radius: 0;
                transition: background 0.2s;
                letter-spacing: 0.03em;
            }
            .bn-close-btn:hover { background: #1a9ec7; }
            .bn-close-btn.error { background: #c0392b; }
            .bn-close-btn.error:hover { background: #a93226; }
        `;
        document.head.appendChild(s);
    }

    const iconMap = {
        success: 'fa-check',
        error:   'fa-times',
        info:    'fa-info'
    };

    const overlay = document.createElement('div');
    overlay.className = 'bn-overlay';
    overlay.innerHTML = `
        <div class="bn-modal" role="dialog" aria-modal="true" aria-label="${title}">
            <div class="bn-icon-wrap ${type}">
                <i class="fas ${iconMap[type] || 'fa-info'}"></i>
            </div>
            <p class="bn-title">${title}</p>
            <p class="bn-message">${message}</p>
            <button class="bn-close-btn ${type === 'error' ? 'error' : ''}">Got it</button>
        </div>
    `;

    overlay.querySelector('.bn-close-btn').addEventListener('click', () => overlay.remove());
    overlay.addEventListener('click', e => { if (e.target === overlay) overlay.remove(); });

    document.body.appendChild(overlay);

    // Auto-dismiss after 6s
    setTimeout(() => { if (overlay.parentNode) overlay.remove(); }, 6000);
}

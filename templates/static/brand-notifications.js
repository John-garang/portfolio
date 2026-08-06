// Brand Notifications System — centred modal with brand identity
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
                background: rgba(0,0,0,0.55);
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
                background: linear-gradient(145deg, #16b2dc 0%, #0f7fa8 55%, #0a5c7a 100%);
                border-radius: 0;
                box-shadow: 0 24px 70px rgba(0,0,0,0.35);
                padding: 2.5rem 2rem 2rem;
                max-width: 400px;
                width: 100%;
                text-align: center;
                position: relative;
                animation: bn-slide-up 0.25s ease;
                font-family: 'Inter', sans-serif;
                color: #fff;
            }
            @keyframes bn-slide-up {
                from { transform: translateY(28px); opacity: 0; }
                to   { transform: translateY(0);    opacity: 1; }
            }
            .bn-logo {
                width: 52px;
                height: 52px;
                object-fit: contain;
                margin: 0 auto 1.25rem;
                display: block;
                filter: brightness(0) invert(1);
                opacity: 0.92;
            }
            .bn-icon-wrap {
                width: 56px;
                height: 56px;
                border-radius: 50%;
                display: flex;
                align-items: center;
                justify-content: center;
                margin: 0 auto 1.25rem;
                font-size: 1.5rem;
                background: rgba(255,255,255,0.18);
                color: #fff;
            }
            .bn-icon-wrap.error {
                background: rgba(255,255,255,0.15);
            }
            .bn-title {
                font-size: 1.2rem;
                font-weight: 700;
                color: #fff;
                margin: 0 0 0.5rem;
                letter-spacing: 0.01em;
            }
            .bn-message {
                font-size: 0.9rem;
                color: rgba(255,255,255,0.88);
                line-height: 1.65;
                margin: 0 0 1.75rem;
            }
            .bn-close-btn {
                background: rgba(255,255,255,0.18);
                color: #fff;
                border: 1.5px solid rgba(255,255,255,0.45);
                padding: 0.65rem 2.25rem;
                font-family: 'Inter', sans-serif;
                font-size: 0.88rem;
                font-weight: 600;
                cursor: pointer;
                border-radius: 0;
                transition: background 0.2s, border-color 0.2s;
                letter-spacing: 0.04em;
                text-transform: uppercase;
            }
            .bn-close-btn:hover {
                background: rgba(255,255,255,0.28);
                border-color: rgba(255,255,255,0.7);
            }
            .bn-divider {
                width: 40px;
                height: 2px;
                background: rgba(255,255,255,0.3);
                margin: 0 auto 1.25rem;
            }
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
            <img class="bn-logo" src="/static/Pictures/john-ngor-deng-garang-logo.png" alt="JNDG">
            <div class="bn-divider"></div>
            <div class="bn-icon-wrap ${type}">
                <i class="fas ${iconMap[type] || 'fa-info'}"></i>
            </div>
            <p class="bn-title">${title}</p>
            <p class="bn-message">${message}</p>
            <button class="bn-close-btn">Got it</button>
        </div>
    `;

    overlay.querySelector('.bn-close-btn').addEventListener('click', () => overlay.remove());
    overlay.addEventListener('click', e => { if (e.target === overlay) overlay.remove(); });

    document.body.appendChild(overlay);

    setTimeout(() => { if (overlay.parentNode) overlay.remove(); }, 6000);
}

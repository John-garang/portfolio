// Analytics Tracking System
class Analytics {
    constructor() {
        this.sessionId = this.generateSessionId();
        this.startTime = Date.now();
        this.trackPageView();
        this.setupEventListeners();
    }

    generateSessionId() {
        return 'session_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
    }

    async trackEvent(eventType, data = {}) {
        const eventData = {
            sessionId: this.sessionId,
            eventType,
            timestamp: new Date().toISOString(),
            page: window.location.pathname,
            referrer: document.referrer,
            userAgent: navigator.userAgent,
            screenResolution: `${screen.width}x${screen.height}`,
            ...data
        };

        try {
            await fetch('https://portfolio-backend-1-53hz.onrender.com/api/analytics/track', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(eventData)
            });
        } catch (error) {
            console.log('Analytics tracking failed:', error);
        }
    }

    trackPageView() {
        this.trackEvent('page_view', {
            title: document.title,
            url: window.location.href
        });
    }

    setupEventListeners() {
        // Track clicks on navigation links
        document.addEventListener('click', (e) => {
            if (e.target.matches('a[href]')) {
                this.trackEvent('link_click', {
                    linkText: e.target.textContent,
                    linkUrl: e.target.href,
                    linkType: e.target.href.startsWith('http') ? 'external' : 'internal'
                });
            }
        });

        // Track form submissions
        document.addEventListener('submit', (e) => {
            this.trackEvent('form_submit', {
                formId: e.target.id || 'unknown',
                formAction: e.target.action || 'none'
            });
        });

        // Track scroll depth
        let maxScroll = 0;
        window.addEventListener('scroll', () => {
            const scrollPercent = Math.round((window.scrollY / (document.body.scrollHeight - window.innerHeight)) * 100);
            if (scrollPercent > maxScroll) {
                maxScroll = scrollPercent;
                if (maxScroll % 25 === 0) { // Track at 25%, 50%, 75%, 100%
                    this.trackEvent('scroll_depth', { depth: maxScroll });
                }
            }
        });

        // Track time on page when leaving
        window.addEventListener('beforeunload', () => {
            const timeOnPage = Math.round((Date.now() - this.startTime) / 1000);
            this.trackEvent('page_exit', { timeOnPage });
        });
    }
}

// Initialize analytics
window.analytics = new Analytics();
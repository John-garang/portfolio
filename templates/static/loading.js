// Hide loading screen once page is fully loaded
window.addEventListener('load', () => {
    const loadingScreen = document.getElementById('loading-screen');
    if (loadingScreen) {
        loadingScreen.classList.add('fade-out');
        setTimeout(() => { loadingScreen.style.display = 'none'; }, 500);
    }
});

// Show loading screen on internal navigation
document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('a[href]').forEach(link => {
        const href = link.getAttribute('href');
        // Only trigger for internal links (not anchors, mailto, tel, external)
        if (!href || href.startsWith('#') || href.startsWith('mailto:') ||
            href.startsWith('tel:') || href.startsWith('http') || href.startsWith('//')) return;

        link.addEventListener('click', () => {
            const loadingScreen = document.getElementById('loading-screen');
            if (loadingScreen) {
                loadingScreen.style.display = 'flex';
                loadingScreen.classList.remove('fade-out');
            }
        });
    });
});

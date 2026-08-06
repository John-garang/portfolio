function hideLoadingScreen() {
    const el = document.getElementById('loading-screen') || document.getElementById('loadingScreen');
    if (!el) return;
    el.classList.add('fade-out');
    setTimeout(() => { el.style.display = 'none'; }, 400);
}

// Hide on load
window.addEventListener('load', hideLoadingScreen);

// Safety fallback — never stay stuck longer than 3 seconds
setTimeout(hideLoadingScreen, 3000);

document.addEventListener('click', (e) => {
    const link = e.target.closest('a[href]');
    if (!link) return;
    const href = link.getAttribute('href');
    if (!href || href.startsWith('#') || href.startsWith('mailto:') ||
        href.startsWith('tel:') || href.startsWith('http') || href.startsWith('//')) return;
    // Don't show loader if navigating to the current page
    const dest = new URL(href, location.href);
    if (dest.pathname === location.pathname) return;
    const el = document.getElementById('loading-screen') || document.getElementById('loadingScreen');
    if (el) {
        el.style.display = 'flex';
        el.classList.remove('fade-out');
    }
});

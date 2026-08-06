function hideLoadingScreen() {
    const el = document.getElementById('loading-screen') || document.getElementById('loadingScreen');
    if (!el) return;
    el.classList.add('fade-out');
    setTimeout(() => { el.style.display = 'none'; }, 400);
}

// Hide immediately if DOM is already ready
if (document.readyState === 'complete') {
    hideLoadingScreen();
} else {
    window.addEventListener('load', hideLoadingScreen);
}

// Hard fallback — never stuck longer than 2 seconds
setTimeout(hideLoadingScreen, 2000);

// Handle bfcache (back/forward navigation)
window.addEventListener('pageshow', hideLoadingScreen);

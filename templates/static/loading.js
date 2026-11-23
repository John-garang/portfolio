// Hide the splash as soon as the page's HTML is ready — not after every image has downloaded.
(function () {
    function hide() {
        var el = document.getElementById('loading-screen') || document.getElementById('loadingScreen');
        if (!el || el.dataset.hidden) return;
        el.dataset.hidden = '1';
        el.style.opacity = '0';
        el.style.pointerEvents = 'none';
        setTimeout(function () { el.style.display = 'none'; }, 300);
    }
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', hide);
    } else {
        hide();
    }
    setTimeout(hide, 1200);
    window.addEventListener('pageshow', hide);
})();

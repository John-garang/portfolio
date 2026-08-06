window.addEventListener('load', () => {
    const el = document.getElementById('loading-screen') || document.getElementById('loadingScreen');
    if (!el) return;
    el.classList.add('fade-out');
    setTimeout(() => { el.style.display = 'none'; }, 400);
});

document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('a[href]').forEach(link => {
        const href = link.getAttribute('href');
        if (!href || href.startsWith('#') || href.startsWith('mailto:') ||
            href.startsWith('tel:') || href.startsWith('http') || href.startsWith('//')) return;
        link.addEventListener('click', () => {
            const el = document.getElementById('loading-screen') || document.getElementById('loadingScreen');
            if (el) {
                el.style.display = 'flex';
                el.classList.remove('fade-out');
            }
        });
    });
});

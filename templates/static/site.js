/* johngarang.com — small interactions for theme v3
   1. Project breakdown: tabs + layers that pull apart when in view
   2. Japan-style type: a few letters loosen and fall
   3. Deck gallery: click and each design flies away (left / up / down)
*/
(function () {
    var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;

    /* 1. Breakdown ---------------------------------------------------- */
    function initBreakdown() {
        document.querySelectorAll('.breakdown').forEach(function (root) {
            var tabs = root.querySelectorAll('.bd-tab');
            var panels = root.querySelectorAll('.bd-panel');
            function show(id) {
                tabs.forEach(function (t) { t.setAttribute('aria-selected', String(t.dataset.panel === id)); });
                panels.forEach(function (p) {
                    var on = p.id === id;
                    p.classList.toggle('active', on);
                    p.classList.remove('exploded');
                    if (on) { requestAnimationFrame(function () { requestAnimationFrame(function () { p.classList.add('exploded'); }); }); }
                });
            }
            tabs.forEach(function (t) { t.addEventListener('click', function () { show(t.dataset.panel); }); });
            var first = root.querySelector('.bd-panel.active');
            if (!first) return;
            if (reduce || !('IntersectionObserver' in window)) { first.classList.add('exploded'); return; }
            var io = new IntersectionObserver(function (entries) {
                entries.forEach(function (e) {
                    var active = root.querySelector('.bd-panel.active');
                    if (e.isIntersecting && active) active.classList.add('exploded');
                });
            }, { threshold: 0.35 });
            io.observe(root);
        });
    }

    /* 2. Falling letters ---------------------------------------------- */
    function initFall() {
        document.querySelectorAll('.fall').forEach(function (el) {
            var text = el.textContent;
            el.setAttribute('aria-label', text);
            el.textContent = '';
            var chars = Array.prototype.slice.call(text);
            chars.forEach(function (c, i) {
                var s = document.createElement('span');
                s.className = 'ch';
                s.setAttribute('aria-hidden', 'true');
                s.textContent = c === ' ' ? ' ' : c;
                el.appendChild(s);
            });
            if (reduce || window.innerWidth < 769) return;
            var spans = el.querySelectorAll('.ch');
            // loosen the last few letters, like type slipping off the slide
            var n = Math.min(spans.length > 4 ? 3 : 1, spans.length);
            setTimeout(function () {
                for (var k = 0; k < n; k++) {
                    var sp = spans[spans.length - 1 - k];
                    var drop = 6 + k * 10 + Math.random() * 6;
                    var rot = (k % 2 ? -1 : 1) * (6 + k * 6);
                    sp.style.transform = 'translateY(' + drop + 'px) rotate(' + rot + 'deg)';
                    sp.style.opacity = String(1 - k * 0.2);
                }
            }, 700);
        });
    }

    /* 3. Deck gallery ------------------------------------------------- */
    var deck, stage, countEl, titleEl, cards = [], top = 0, dirs = ['left', 'up', 'down', 'right'];
    function buildDeck() {
        deck = document.createElement('div');
        deck.className = 'deck-overlay';
        deck.setAttribute('role', 'dialog');
        deck.setAttribute('aria-modal', 'true');
        deck.innerHTML = '<div class="deck-top"><div><h3 class="deck-title"></h3></div>' +
            '<div style="display:flex;align-items:center;gap:1rem"><span class="deck-count"></span><button class="deck-close" aria-label="Close">&times;</button></div></div>' +
            '<div class="deck-stage"></div>' +
            '<div class="deck-hint"><button type="button" class="deck-prev">&larr; Back</button><span>Click the design to throw it away</span><button type="button" class="deck-next">Next &rarr;</button></div>';
        document.body.appendChild(deck);
        stage = deck.querySelector('.deck-stage');
        countEl = deck.querySelector('.deck-count');
        titleEl = deck.querySelector('.deck-title');
        deck.querySelector('.deck-close').addEventListener('click', closeDeck);
        deck.querySelector('.deck-next').addEventListener('click', function () { fling(); });
        deck.querySelector('.deck-prev').addEventListener('click', back);
        deck.addEventListener('click', function (e) { if (e.target === deck) closeDeck(); });
        document.addEventListener('keydown', function (e) {
            if (!deck.classList.contains('open')) return;
            if (e.key === 'Escape') closeDeck();
            if (e.key === 'ArrowRight') fling('right');
            if (e.key === 'ArrowLeft') fling('left');
            if (e.key === 'ArrowUp') fling('up');
            if (e.key === 'ArrowDown') fling('down');
            if (e.key === 'Backspace') back();
        });
        // swipe
        var sx = 0, sy = 0;
        stage.addEventListener('touchstart', function (e) { sx = e.touches[0].clientX; sy = e.touches[0].clientY; }, { passive: true });
        stage.addEventListener('touchend', function (e) {
            var dx = e.changedTouches[0].clientX - sx, dy = e.changedTouches[0].clientY - sy;
            if (Math.max(Math.abs(dx), Math.abs(dy)) < 30) return;
            if (Math.abs(dx) > Math.abs(dy)) fling(dx < 0 ? 'left' : 'right'); else fling(dy < 0 ? 'up' : 'down');
        }, { passive: true });
    }
    function layout() {
        cards.forEach(function (c, i) {
            var d = i - top;
            if (d < 0) return; // thrown
            var depth = Math.min(d, 4);
            c.style.zIndex = String(100 - d);
            c.style.opacity = d > 4 ? '0' : '1';
            c.style.transform = 'translate(' + (depth * 10) + 'px,' + (depth * 8) + 'px) rotate(' + (depth ? (depth % 2 ? 2.5 : -2.5) * depth / 2 : 0) + 'deg) scale(' + (1 - depth * 0.035) + ')';
        });
        countEl.textContent = Math.min(top + 1, cards.length) + ' / ' + cards.length;
    }
    function fling(dir) {
        if (!cards.length) return;
        if (top >= cards.length - 1) { // last one: restack the deck
            top = 0;
            cards.forEach(function (c) { c.style.transition = 'none'; });
            layout();
            requestAnimationFrame(function () { cards.forEach(function (c) { c.style.transition = ''; }); });
            return;
        }
        dir = dir || dirs[top % 3];
        var c = cards[top];
        var x = 0, y = 0, r = 0;
        if (dir === 'left') { x = -window.innerWidth; r = -28; }
        if (dir === 'right') { x = window.innerWidth; r = 28; }
        if (dir === 'up') { y = -window.innerHeight; r = -10; }
        if (dir === 'down') { y = window.innerHeight; r = 12; }
        c.style.transform = 'translate(' + x + 'px,' + y + 'px) rotate(' + r + 'deg)';
        c.style.opacity = '0';
        top++;
        layout();
    }
    function back() {
        if (top === 0) return;
        top--;
        layout();
    }
    function openDeck(images, title, start) {
        if (!deck) buildDeck();
        stage.innerHTML = '';
        cards = images.map(function (im) {
            var c = document.createElement('div');
            c.className = 'deck-card';
            var img = document.createElement('img');
            img.src = im.src; img.alt = im.alt || '';
            c.appendChild(img);
            c.addEventListener('click', function () { fling(); });
            stage.appendChild(c);
            return c;
        });
        top = start || 0;
        titleEl.textContent = title || '';
        layout();
        deck.classList.add('open');
        document.body.style.overflow = 'hidden';
    }
    function closeDeck() {
        deck.classList.remove('open');
        document.body.style.overflow = '';
    }
    window.openDeck = openDeck;

    // Hook the existing galleries (Graphic Design + Programs) into the deck
    function imagesFrom(container, slideSel) {
        return Array.prototype.map.call(container.querySelectorAll(slideSel + ' img'), function (img) {
            return { src: img.getAttribute('src') || img.dataset.src, alt: img.alt };
        }).filter(function (i) { return i.src; });
    }
    function initGalleryHooks() {
        if (typeof window.openDesignLightbox === 'function') {
            window.openDesignLightbox = function (name, start) {
                var g = document.querySelector('.design-program-gallery[data-gallery="' + name + '"]');
                if (!g) return;
                var block = g.closest('.design-block');
                var label = block && block.querySelector('.overlay-label');
                openDeck(imagesFrom(g, '.design-gallery-slide'), label ? label.textContent : '', start || 0);
            };
        }
    }

    document.addEventListener('DOMContentLoaded', function () {
        initBreakdown();
        initFall();
        initGalleryHooks();
    });
})();

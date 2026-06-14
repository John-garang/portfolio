// =====================================================
// UNIFIED SITE SCRIPT - NO CONFLICTS
// =====================================================

(function() {
    'use strict';
    
    // Search data
    const searchData = [
        { title: 'Home', url: '/', desc: 'Digital communications portfolio showcasing skills and expertise' },
        { title: 'About Me', url: '/about', desc: 'Biography and background of John Ngor Deng Garang' },
        { title: 'Work Portfolio', url: '/work-portfolio', desc: 'Collection of professional work and projects' },
        { title: 'My Shelf', url: '/my-shelf', desc: 'Published writings and articles' },
        { title: 'Poems', url: '/poems', desc: 'Poetry collection' },
        { title: 'CV', url: '/cv', desc: 'Curriculum vitae and professional experience' },
        { title: 'Services', url: '/services', desc: 'Professional services offered' },
        { title: 'Contact', url: '/contact', desc: 'Get in touch and contact information' }
    ];
    
    // Wait for header to be loaded by load-header.js
    function waitForElement(selector, callback) {
        const observer = new MutationObserver(function(mutations, me) {
            const element = document.querySelector(selector);
            if (element) {
                me.disconnect();
                callback(element);
            }
        });
        
        observer.observe(document, {
            childList: true,
            subtree: true
        });
        
        // Also check immediately in case it's already there
        const element = document.querySelector(selector);
        if (element) {
            callback(element);
        }
    }
    
    // Initialize search when header is ready
    waitForElement('#searchBtn', function() {
        const searchBtn = document.getElementById('searchBtn');
        const searchOverlay = document.getElementById('searchOverlay');
        const searchInput = document.getElementById('searchInput');
        const searchClose = document.getElementById('searchClose');
        const searchResults = document.getElementById('searchResults');
        
        if (!searchBtn || !searchOverlay) return;
        
        // Open search
        searchBtn.addEventListener('click', () => {
            searchOverlay.style.display = 'block';
            setTimeout(() => searchInput.focus(), 100);
        });
        
        // Close search
        searchClose.addEventListener('click', closeSearch);
        searchOverlay.addEventListener('click', (e) => {
            if (e.target === searchOverlay) closeSearch();
        });
        
        function closeSearch() {
            searchOverlay.style.display = 'none';
            searchInput.value = '';
            searchResults.innerHTML = '';
        }
        
        // Search functionality
        searchInput.addEventListener('input', (e) => {
            const query = e.target.value.trim().toLowerCase();
            if (query.length === 0) {
                searchResults.innerHTML = '';
                return;
            }
            
            const results = searchData.filter(page => 
                page.title.toLowerCase().includes(query) ||
                page.desc.toLowerCase().includes(query)
            );
            
            if (results.length === 0) {
                searchResults.innerHTML = '<div class="no-search-results">No results found</div>';
            } else {
                searchResults.innerHTML = results.map(result => `
                    <a href="${result.url}" class="search-result-link">
                        <div class="search-result-title">${result.title}</div>
                        <div class="search-result-desc">${result.desc}</div>
                    </a>
                `).join('');
            }
        });
        
        // Escape key to close
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape' && searchOverlay.style.display === 'block') {
                closeSearch();
            }
        });
    });
    
    // Portfolio tabs (if on homepage)
    const tabBtns = document.querySelectorAll('.tab-btn');
    const tabContents = document.querySelectorAll('.tab-content');
    
    tabBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            tabBtns.forEach(b => b.classList.remove('active'));
            tabContents.forEach(content => content.classList.remove('active'));
            
            btn.classList.add('active');
            const targetTab = btn.getAttribute('data-tab');
            document.getElementById(targetTab)?.classList.add('active');
        });
    });
    
    // Smooth scrolling for anchor links
    document.addEventListener('click', (e) => {
        const anchor = e.target.closest('a[href^="#"]');
        if (anchor) {
            e.preventDefault();
            const target = document.querySelector(anchor.getAttribute('href'));
            if (target) {
                target.scrollIntoView({ behavior: 'smooth', block: 'start' });
            }
        }
    });
    
})();

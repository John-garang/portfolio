// Load header across all pages
fetch('header.html')
    .then(response => response.text())
    .then(data => {
        document.getElementById('header-placeholder').innerHTML = data;
        
        // Set active link based on current page
        const currentPage = window.location.pathname.split('/').pop() || 'index.html';
        document.querySelectorAll('.nav-link').forEach(link => {
            if (link.getAttribute('href') === currentPage) {
                link.classList.add('active');
            }
        });
        
        // Initialize navbar scroll behavior after header is loaded
        const navbar = document.querySelector('.navbar');
        if (navbar) {
            // Check if page has hero section
            const hasHero = document.querySelector('.hero, .about, .alu-hero, .blog-hero, .shelf-hero');
            
            if (!hasHero) {
                navbar.classList.add('scrolled');
            }
            
            window.addEventListener('scroll', () => {
                if (window.scrollY > 50) {
                    navbar.classList.add('scrolled');
                } else {
                    if (hasHero) {
                        navbar.classList.remove('scrolled');
                    }
                }
            });
        }
        
        // Initialize search functionality
        const searchBtn = document.getElementById('searchBtn');
        const searchOverlay = document.getElementById('searchOverlay');
        const searchInput = document.getElementById('searchInput');
        const searchClose = document.getElementById('searchClose');
        
        if (searchBtn && searchOverlay) {
            searchBtn.addEventListener('click', () => {
                searchOverlay.style.display = 'block';
                setTimeout(() => searchInput.focus(), 100);
            });
            
            searchClose.addEventListener('click', () => {
                searchOverlay.style.display = 'none';
                searchInput.value = '';
            });
            
            searchOverlay.addEventListener('click', (e) => {
                if (e.target === searchOverlay) {
                    searchOverlay.style.display = 'none';
                    searchInput.value = '';
                }
            });
            
            document.addEventListener('keydown', (e) => {
                if (e.key === 'Escape' && searchOverlay.style.display === 'block') {
                    searchOverlay.style.display = 'none';
                    searchInput.value = '';
                }
            });
            
            // Search functionality
            searchInput.addEventListener('input', (e) => {
                const query = e.target.value.toLowerCase();
                if (query.length > 2) {
                    // Search through page content
                    const results = [];
                    document.querySelectorAll('h1, h2, h3, p').forEach(el => {
                        if (el.textContent.toLowerCase().includes(query)) {
                            results.push(el);
                        }
                    });
                    
                    // Highlight first result
                    if (results.length > 0) {
                        results[0].scrollIntoView({ behavior: 'smooth', block: 'center' });
                    }
                }
            });
        }
        
        // Initialize mobile menu after header is loaded
        const hamburger = document.querySelector('.hamburger');
        const navMenu = document.querySelector('.nav-menu');
        const mobileOverlay = document.getElementById('mobileOverlay');
        
        if (hamburger && navMenu) {
            hamburger.addEventListener('click', () => {
                hamburger.classList.toggle('active');
                navMenu.classList.toggle('active');
                if (mobileOverlay) {
                    mobileOverlay.classList.toggle('active');
                }
                document.body.classList.toggle('menu-open');
            });
            
            if (mobileOverlay) {
                mobileOverlay.addEventListener('click', () => {
                    hamburger.classList.remove('active');
                    navMenu.classList.remove('active');
                    mobileOverlay.classList.remove('active');
                    document.body.classList.remove('menu-open');
                });
            }
            
            document.querySelectorAll('.nav-link').forEach(n => n.addEventListener('click', () => {
                hamburger.classList.remove('active');
                navMenu.classList.remove('active');
                if (mobileOverlay) {
                    mobileOverlay.classList.remove('active');
                }
                document.body.classList.remove('menu-open');
            }));
        }
    });

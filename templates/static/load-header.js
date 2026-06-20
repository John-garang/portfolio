// Universal Header System
document.addEventListener('DOMContentLoaded', function() {
    const headerPlaceholder = document.getElementById('header-placeholder');
    
    if (headerPlaceholder) {
        const header = `
            <nav class="navbar">
                <div class="nav-container">
                    <div class="nav-logo">
                        <img src="static/Pictures/Logo.png" alt="John Garang Logo">
                        <span class="logo-name">John Ngor Deng Garang</span>
                    </div>
                    <ul class="nav-menu">
                        <li><a href="/" class="nav-link">Home</a></li>
                        <li><a href="/about" class="nav-link">About</a></li>
                        <li class="dropdown">
                            <a href="/work-portfolio" class="nav-link">Work Portfolio <i class="fas fa-chevron-down"></i></a>
                            <div class="dropdown-content">
                                <a href="my-shelf.html">My Shelf</a>
                                <a href="artefacts.html">Artefacts</a>
                                <a href="cv.html">CV</a>
                                <a href="graphic-design.html">Graphic Design</a>
                            </div>
                        </li>
                        <li><a href="/experience-overview" class="nav-link">Experience</a></li>
                        <li><a href="/programs-overview" class="nav-link">Programs</a></li>
                        <li><a href="/services" class="nav-link">Services</a></li>
                        <li><a href="/contact" class="nav-link">Contact</a></li>
                        <li><a href="/poems" class="nav-link">Poems</a></li>
                    </ul>
                    <div class="nav-right">
                        <button class="search-btn" id="searchBtn">
                            <i class="fas fa-search"></i>
                        </button>
                        <div class="hamburger" id="hamburger">
                            <span></span>
                            <span></span>
                            <span></span>
                        </div>
                    </div>
                </div>
                <div class="mobile-overlay" id="mobileOverlay"></div>
            </nav>
            
            <!-- Search Overlay -->
            <div class="search-overlay" id="searchOverlay">
                <div class="search-modal">
                    <div class="search-header">
                        <i class="fas fa-search search-icon"></i>
                        <input type="text" id="searchInput" placeholder="Search pages...">
                        <button class="search-close" id="searchClose">&times;</button>
                    </div>
                    <div class="search-results" id="searchResults"></div>
                </div>
            </div>
        `;
        
        headerPlaceholder.innerHTML = header;
        
        // Get navbar and set background based on page
        const navbar = document.querySelector('.navbar');
        
        if (navbar) {
            // All pages start transparent
            navbar.style.background = 'transparent';
            navbar.classList.remove('scrolled');
        }
        
        // Set active page
        const currentPage = window.location.pathname === '/' ? 'index.html' : window.location.pathname.split('/').pop() + '.html';
        document.querySelectorAll('.nav-link').forEach(link => {
            const href = link.getAttribute('href');
            if ((href === '/' && currentPage === 'index.html') || 
                (href !== '/' && href.replace('/', '') + '.html' === currentPage)) {
                link.classList.add('active');
            }
        });
        
        // Scroll effects
        function updateNavbarState() {
            if (!navbar) return;
            // All pages have scroll behavior
            if (window.scrollY > 50) {
                navbar.style.background = 'rgba(255, 255, 255, 0.98)';
                navbar.classList.add('scrolled');
            } else {
                navbar.style.background = 'transparent';
                navbar.classList.remove('scrolled');
            }
        }
        
        // Set initial state after header loads
        setTimeout(() => {
            updateNavbarState();
            // Force transparent initially regardless of scroll position
            if (navbar && window.scrollY <= 80) {
                navbar.style.background = 'transparent';
                navbar.classList.remove('scrolled');
            }
        }, 0);
        
        // Update on scroll
        window.addEventListener('scroll', updateNavbarState);
        
        // Mobile menu
        const hamburger = document.getElementById('hamburger');
        const navMenu = document.querySelector('.nav-menu');
        const mobileOverlay = document.getElementById('mobileOverlay');
        
        if (hamburger && navMenu) {
            hamburger.addEventListener('click', function() {
                hamburger.classList.toggle('active');
                navMenu.classList.toggle('active');
                mobileOverlay.classList.toggle('active');
                document.body.classList.toggle('menu-open');
            });
            
            mobileOverlay.addEventListener('click', function() {
                hamburger.classList.remove('active');
                navMenu.classList.remove('active');
                mobileOverlay.classList.remove('active');
                document.body.classList.remove('menu-open');
            });
        }
    }
});
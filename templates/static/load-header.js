// Universal Header System
document.addEventListener('DOMContentLoaded', function() {
    const headerPlaceholder = document.getElementById('header-placeholder');
    
    if (headerPlaceholder) {
        const header = `
            <nav class="navbar">
                <div class="nav-container">
                    <div class="nav-logo">
                        <img src="/static/Pictures/john-ngor-deng-garang-logo.png" alt="John Garang Logo">
                        <span class="logo-name">John Ngor Deng Garang</span>
                    </div>
                    <ul class="nav-menu">
                        <li><a href="/" class="nav-link">Home</a></li>
                        <li><a href="/about" class="nav-link">About</a></li>
                        <li class="dropdown">
                            <a href="/work-portfolio" class="nav-link">Work Portfolio <i class="fas fa-chevron-down"></i></a>
                            <div class="dropdown-content">
                                <a href="/my-shelf">My Shelf</a>
                                <a href="/cv">CV</a>
                                <a href="/graphic-design">Graphic Design</a>
                                <a href="/web-design">Web Design</a>
                            </div>
                        </li>
                        <li><a href="/experience-overview" class="nav-link">Experience</a></li>
                        <li><a href="/programs-overview" class="nav-link">Programs</a></li>
                        <li><a href="/services" class="nav-link">Services</a></li>
                        <li><a href="/poems" class="nav-link">Poems</a></li>
                    </ul>
                    <div class="nav-right">
                        <div class="hamburger" id="hamburger">
                            <span></span>
                            <span></span>
                            <span></span>
                        </div>
                    </div>
                </div>
                <div class="mobile-overlay" id="mobileOverlay"></div>
            </nav>
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

            // Dropdown links: first tap opens, second tap navigates
            navMenu.querySelectorAll('.dropdown > .nav-link').forEach(function(link) {
                link.addEventListener('click', function(e) {
                    const dropdown = link.closest('.dropdown');
                    if (!dropdown.classList.contains('active')) {
                        e.preventDefault();
                        navMenu.querySelectorAll('.dropdown').forEach(function(d) {
                            if (d !== dropdown) d.classList.remove('active');
                        });
                        dropdown.classList.add('active');
                    }
                });
            });
        }
    }
});
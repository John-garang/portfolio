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
                        <li><a href="index.html" class="nav-link">Home</a></li>
                        <li><a href="about.html" class="nav-link">About</a></li>
                        <li class="dropdown">
                            <a href="work-portfolio.html" class="nav-link">Work Portfolio <i class="fas fa-chevron-down"></i></a>
                            <div class="dropdown-content">
                                <a href="my-shelf.html">My Shelf</a>
                                <a href="artefacts.html">Artefacts</a>
                                <a href="cv.html">CV</a>
                                <a href="graphic-design.html">Graphic Design</a>
                            </div>
                        </li>
                        <li class="dropdown">
                            <a href="experience-overview.html" class="nav-link">Experience <i class="fas fa-chevron-down"></i></a>
                            <div class="dropdown-content">
                                <a href="african-leadership-university.html">African Leadership University</a>
                                <a href="education-bridge.html">Education Bridge</a>
                                <a href="african-leadership-academy.html">African Leadership Academy</a>
                                <a href="ashinaga-foundation.html">Ashinaga Foundation</a>
                                <a href="uganics-repellents.html">Uganics Repellents Ltd</a>
                            </div>
                        </li>
                        <li class="dropdown">
                            <a href="programs-overview.html" class="nav-link">Programs <i class="fas fa-chevron-down"></i></a>
                            <div class="dropdown-content">
                                <a href="cnn-academy.html">CNN Academy Fellow</a>
                                <a href="take-action-lab.html">Take Action Lab</a>
                                <a href="unleash-innovation-lab.html">UNLEASH Innovation Lab</a>
                                <a href="accra-fusion.html">Accra Fusion</a>
                                <a href="yali-east-africa.html">YALI East Africa</a>
                            </div>
                        </li>
                        <li><a href="services.html" class="nav-link">Services</a></li>
                        <li><a href="contact.html" class="nav-link">Contact</a></li>
                        <li><a href="poems.html" class="nav-link">Poems</a></li>
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
        
        // Set active page
        const currentPage = window.location.pathname.split('/').pop() || 'index.html';
        document.querySelectorAll('.nav-link').forEach(link => {
            if (link.getAttribute('href') === currentPage) {
                link.classList.add('active');
            }
        });
        
        // Scroll effects
        const navbar = document.querySelector('.navbar');
        window.addEventListener('scroll', function() {
            if (window.scrollY > 50) {
                navbar.classList.add('scrolled');
            } else {
                navbar.classList.remove('scrolled');
            }
        });
        
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
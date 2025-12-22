import os
import re
from pathlib import Path

def add_universal_header():
    templates_dir = Path("templates")
    
    # Header HTML with all functionality
    header_html = '''    <!-- Header Placeholder -->
    <div id="header-placeholder">
        <!-- Universal Navigation -->
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
    </div>
    <script>
        // Navbar scroll effect
        window.addEventListener('scroll', function() {
            const navbar = document.querySelector('.navbar');
            if (window.scrollY > 50) {
                navbar.classList.add('scrolled');
            } else {
                navbar.classList.remove('scrolled');
            }
        });
        
        // Mobile menu functionality
        document.addEventListener('DOMContentLoaded', function() {
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
        });
    </script>'''
    
    # JavaScript for setting active page
    active_script = '''
    <script>
        // Set active page
        document.addEventListener('DOMContentLoaded', function() {
            const currentPage = window.location.pathname.split('/').pop() || 'index.html';
            document.querySelectorAll('.nav-link').forEach(link => {
                if (link.getAttribute('href') === currentPage) {
                    link.classList.add('active');
                }
            });
        });
    </script>'''
    
    for html_file in templates_dir.glob("*.html"):
        if html_file.name == 'header.html' or html_file.name == 'footer.html':
            continue
            
        with open(html_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Skip if already has header
        if 'nav class="navbar"' in content and html_file.name != 'index.html':
            continue
            
        # Find body tag and add header after it
        if '<body>' in content:
            content = content.replace('<body>', f'<body>\n{header_html}')
        elif '<body' in content:
            # Handle body tag with attributes
            body_match = re.search(r'<body[^>]*>', content)
            if body_match:
                content = content.replace(body_match.group(), f'{body_match.group()}\n{header_html}')
        
        # Add active script before closing body tag
        if '</body>' in content:
            content = content.replace('</body>', f'{active_script}\n</body>')
        
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"Added header to: {html_file.name}")

if __name__ == "__main__":
    add_universal_header()
    print("Universal header added to all pages!")
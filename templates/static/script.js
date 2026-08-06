// Search Functionality
const searchBtn = document.getElementById('searchBtn');
const searchOverlay = document.getElementById('searchOverlay');
const searchInput = document.getElementById('searchInput');
const searchClose = document.getElementById('searchClose');
const searchResults = document.getElementById('searchResults');

const searchData = [
    { title: 'Home', url: 'index', desc: 'Digital communications portfolio showcasing skills and expertise' },
    { title: 'About Me', url: 'about', desc: 'Biography and background of John Ngor Deng Garang' },
    { title: 'Work Portfolio', url: 'work-portfolio', desc: 'Collection of professional work and projects' },
    { title: 'My Shelf', url: 'my-shelf', desc: 'Published writings and articles' },
    { title: 'Artefacts', url: 'artefacts', desc: 'Creative projects and artefacts' },
    { title: 'CV', url: 'cv', desc: 'Curriculum vitae and professional experience' },
    { title: 'Graphic Design', url: 'graphic-design', desc: 'Graphic design portfolio and visual work' },
    { title: 'Experience Overview', url: 'experience-overview', desc: 'Overview of professional experience and career' },
    { title: 'African Leadership University', url: 'african-leadership-university', desc: 'Experience at African Leadership University' },
    { title: 'Education Bridge', url: 'education-bridge', desc: 'Work with Education Bridge organization' },
    { title: 'African Leadership Academy', url: 'african-leadership-academy', desc: 'Experience at African Leadership Academy' },
    { title: 'CNN Academy Fellow', url: 'cnn-academy', desc: 'CNN Academy Fellowship experience' },
    { title: 'Services', url: 'services', desc: 'Professional services offered' },
    { title: 'Contact', url: 'contact', desc: 'Get in touch and contact information' }
];

if (searchBtn && searchOverlay) {
    searchBtn.addEventListener('click', () => {
        searchOverlay.style.display = 'block';
        setTimeout(() => searchInput.focus(), 100);
    });
    
    searchClose.addEventListener('click', () => {
        searchOverlay.style.display = 'none';
        searchInput.value = '';
        searchResults.innerHTML = '';
    });
    
    searchOverlay.addEventListener('click', (e) => {
        if (e.target === searchOverlay) {
            searchOverlay.style.display = 'none';
            searchInput.value = '';
            searchResults.innerHTML = '';
        }
    });
    
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
    
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape' && searchOverlay.style.display === 'block') {
            searchOverlay.style.display = 'none';
            searchInput.value = '';
            searchResults.innerHTML = '';
        }
    });
}

// Mobile Navigation is now handled in load-header.js

// Smooth scrolling for navigation links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});

// Portfolio tabs functionality
const tabBtns = document.querySelectorAll('.tab-btn');
const tabContents = document.querySelectorAll('.tab-content');

if (tabBtns.length > 0 && tabContents.length > 0) {
    tabBtns.forEach(btn => {
        // Support both click and touch events for mobile
        const handleTabClick = (e) => {
            e.preventDefault();
            e.stopPropagation();
            
            // Remove active class from all buttons and contents
            tabBtns.forEach(b => b.classList.remove('active'));
            tabContents.forEach(content => content.classList.remove('active'));
            
            // Add active class to clicked button
            btn.classList.add('active');
            
            // Show corresponding content
            const targetTab = btn.getAttribute('data-tab');
            const targetContent = document.getElementById(targetTab);
            if (targetContent) {
                targetContent.classList.add('active');
            }
        };
        
        btn.addEventListener('click', handleTabClick);
        btn.addEventListener('touchend', handleTabClick, { passive: false });
    });
}

// Experience dropdown functionality
function toggleDropdown(element) {
    const content = element.nextElementSibling;
    const icon = element.querySelector('i');
    
    // Close all other dropdowns
    document.querySelectorAll('.exp-content').forEach(item => {
        if (item !== content) {
            item.classList.remove('active');
            item.previousElementSibling.classList.remove('active');
        }
    });
    
    // Toggle current dropdown
    content.classList.toggle('active');
    element.classList.toggle('active');
}

// Navbar scroll behavior is now handled in load-header.js



// Intersection Observer for animations
const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -50px 0px'
};

const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.classList.add('animate');
        }
    });
}, observerOptions);

document.querySelectorAll('.scroll-animate').forEach(el => observer.observe(el));


// Typing effect for hero title (optional enhancement)
function typeWriter(element, text, speed = 100) {
    let i = 0;
    element.textContent = '';
    
    function type() {
        if (i < text.length) {
            element.textContent += text.charAt(i);
            i++;
            setTimeout(type, speed);
        }
    }
    type();
}

// Initialize typing effect on page load
document.addEventListener('DOMContentLoaded', () => {
    const heroTitle = document.querySelector('.hero h1');
    if (heroTitle) {
        const originalText = heroTitle.textContent;
        typeWriter(heroTitle, originalText, 80);
    }
});

window.addEventListener('load', () => {
    document.body.classList.add('loaded');
});

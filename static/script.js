// Search Functionality
const searchBtn = document.getElementById('searchBtn');
const searchOverlay = document.getElementById('searchOverlay');
const searchInput = document.getElementById('searchInput');
const searchClose = document.getElementById('searchClose');
const searchResults = document.getElementById('searchResults');

const searchData = [
    { title: 'Home', url: 'index.html', desc: 'Digital communications portfolio showcasing skills and expertise' },
    { title: 'About Me', url: 'about.html', desc: 'Biography and background of John Ngor Deng Garang' },
    { title: 'Work Portfolio', url: 'work-portfolio.html', desc: 'Collection of professional work and projects' },
    { title: 'My Shelf', url: 'my-shelf.html', desc: 'Published writings and articles' },
    { title: 'Artefacts', url: 'artefacts.html', desc: 'Creative projects and artefacts' },
    { title: 'CV', url: 'cv.html', desc: 'Curriculum vitae and professional experience' },
    { title: 'Graphic Design', url: 'graphic-design.html', desc: 'Graphic design portfolio and visual work' },
    { title: 'Experience Overview', url: 'experience-overview.html', desc: 'Overview of professional experience and career' },
    { title: 'African Leadership University', url: 'african-leadership-university.html', desc: 'Experience at African Leadership University' },
    { title: 'Education Bridge', url: 'education-bridge.html', desc: 'Work with Education Bridge organization' },
    { title: 'African Leadership Academy', url: 'african-leadership-academy.html', desc: 'Experience at African Leadership Academy' },
    { title: 'CNN Academy Fellow', url: 'cnn-academy.html', desc: 'CNN Academy Fellowship experience' },
    { title: 'Services', url: 'services.html', desc: 'Professional services offered' },
    { title: 'Contact', url: 'contact.html', desc: 'Get in touch and contact information' }
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

tabBtns.forEach(btn => {
    btn.addEventListener('click', () => {
        // Remove active class from all buttons and contents
        tabBtns.forEach(b => b.classList.remove('active'));
        tabContents.forEach(content => content.classList.remove('active'));
        
        // Add active class to clicked button
        btn.classList.add('active');
        
        // Show corresponding content
        const targetTab = btn.getAttribute('data-tab');
        document.getElementById(targetTab).classList.add('active');
    });
});

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

// Contact form handling
const contactForm = document.querySelector('.contact-form');
if (contactForm) {
    contactForm.addEventListener('submit', function(e) {
    e.preventDefault();
    
    // Get form data
    const formData = new FormData(this);
    const name = this.querySelector('input[type="text"]').value;
    const email = this.querySelector('input[type="email"]').value;
    const subject = this.querySelector('input[type="text"]:nth-of-type(2)').value;
    const message = this.querySelector('textarea').value;
    
    // Simple validation
    if (!name || !email || !subject || !message) {
        alert('Please fill in all fields');
        return;
    }
    
    // Simulate form submission
    const submitBtn = this.querySelector('button');
    const originalText = submitBtn.textContent;
    submitBtn.textContent = 'Sending...';
    submitBtn.disabled = true;
    
    setTimeout(() => {
        alert('Thank you for your message! I\'ll get back to you soon.');
        this.reset();
        submitBtn.textContent = originalText;
        submitBtn.disabled = false;
    }, 2000);
});
}

// Intersection Observer for animations
const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -50px 0px'
};

const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.style.opacity = '1';
            entry.target.style.transform = 'translateY(0)';
        }
    });
}, observerOptions);





// Typing effect for hero title (optional enhancement)
function typeWriter(element, text, speed = 100) {
    let i = 0;
    element.innerHTML = '';
    
    function type() {
        if (i < text.length) {
            element.innerHTML += text.charAt(i);
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

// Parallax effect for hero section
window.addEventListener('scroll', () => {
    const scrolled = window.pageYOffset;
    const hero = document.querySelector('.hero');
    if (hero) {
        hero.style.transform = `translateY(${scrolled * 0.5}px)`;
    }
});

// Add loading animation
window.addEventListener('load', () => {
    document.body.classList.add('loaded');
});

// Preloader (optional)
document.addEventListener('DOMContentLoaded', () => {
    const preloader = document.createElement('div');
    preloader.className = 'preloader';
    preloader.innerHTML = '<div class="loader"></div>';
    document.body.appendChild(preloader);
    
    window.addEventListener('load', () => {
        preloader.style.opacity = '0';
        setTimeout(() => {
            preloader.remove();
        }, 500);
    });
});

// Add CSS for preloader
const preloaderCSS = `
.preloader {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: #fff;
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 9999;
    transition: opacity 0.5s ease;
}

.loader {
    width: 50px;
    height: 50px;
    border: 5px solid #f3f3f3;
    border-top: 5px solid #6c5ce7;
    border-radius: 50%;
    animation: spin 1s linear infinite;
}

@keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
}
`;

const style = document.createElement('style');
style.textContent = preloaderCSS;
document.head.appendChild(style);
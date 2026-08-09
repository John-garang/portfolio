// Search data - pages and their content
const searchData = [
    { title: 'Home', url: 'index', desc: 'Digital communications portfolio showcasing skills and expertise', keywords: 'john garang digital communications portfolio skills graphic design web development' },
    { title: 'About Me', url: 'about', desc: 'Biography and background of John Ngor Deng Garang', keywords: 'about biography south sudanese leader communicator designer storytelling' },
    { title: 'Work Portfolio', url: 'work-portfolio', desc: 'Collection of professional work and projects', keywords: 'work portfolio projects experience' },
    { title: 'My Shelf', url: 'my-shelf', desc: 'Published writings and articles', keywords: 'shelf writings articles publications medium' },
    { title: 'CV', url: 'cv', desc: 'Curriculum vitae and professional experience', keywords: 'cv resume curriculum vitae experience education' },
    { title: 'Graphic Design', url: 'graphic-design', desc: 'Graphic design portfolio and visual work', keywords: 'graphic design visual branding creative' },
    { title: 'Experience Overview', url: 'experience-overview', desc: 'Overview of professional experience and career', keywords: 'experience work history career' },
    { title: 'Programs Overview', url: 'programs-overview', desc: 'Overview of programs and fellowships', keywords: 'programs training fellowship' },
    { title: 'Take Action Lab', url: 'take-action-lab', desc: 'Take Action Lab leadership program', keywords: 'take action lab leadership' },
    { title: 'UNLEASH Innovation Lab', url: 'unleash-innovation', desc: 'UNLEASH Innovation Lab for SDGs', keywords: 'unleash innovation lab sdg sustainability' },
    { title: 'Services', url: 'services', desc: 'Professional services offered', keywords: 'services consulting design development' },
    { title: 'Contact', url: 'contact', desc: 'Get in touch and contact information', keywords: 'contact email phone reach out' }
];

// Get search query from URL
const urlParams = new URLSearchParams(window.location.search);
const query = urlParams.get('q');

if (query) {
    document.getElementById('searchQuery').textContent = query;
    performSearch(query);
} else {
    document.getElementById('searchQuery').textContent = 'All Pages';
    displayAllResults();
}

function performSearch(searchTerm) {
    const results = searchData.filter(page => 
        page.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
        page.keywords.toLowerCase().includes(searchTerm.toLowerCase())
    );

    const container = document.getElementById('searchResultsContainer');
    
    if (results.length === 0) {
        container.innerHTML = '<p class="no-results">No results found. Try different keywords.</p>';
        return;
    }

    container.innerHTML = results.map(result => `
        <div class="search-result-item">
            <h3><a href="${result.url}">${result.title}</a></h3>
            <p class="result-desc">${result.desc}</p>
            <p class="result-url">${result.url}</p>
        </div>
    `).join('');
}

function displayAllResults() {
    const container = document.getElementById('searchResultsContainer');
    container.innerHTML = searchData.map(result => `
        <div class="search-result-item">
            <h3><a href="${result.url}">${result.title}</a></h3>
            <p class="result-desc">${result.desc}</p>
            <p class="result-url">${result.url}</p>
        </div>
    `).join('');
}


// Search data - pages and their content
const searchData = [
    { title: 'Home', url: 'index.html', desc: 'Digital communications portfolio showcasing skills and expertise', keywords: 'john garang digital communications portfolio skills graphic design web development' },
    { title: 'About Me', url: 'about.html', desc: 'Biography and background of John Ngor Deng Garang', keywords: 'about biography south sudanese leader communicator designer storytelling' },
    { title: 'Work Portfolio', url: 'work-portfolio.html', desc: 'Collection of professional work and projects', keywords: 'work portfolio projects experience' },
    { title: 'My Shelf', url: 'my-shelf.html', desc: 'Published writings and articles', keywords: 'shelf writings articles publications medium' },
    { title: 'Artefacts', url: 'artefacts.html', desc: 'Creative projects and artefacts', keywords: 'artefacts projects creative work portfolio' },
    { title: 'CV', url: 'cv.html', desc: 'Curriculum vitae and professional experience', keywords: 'cv resume curriculum vitae experience education' },
    { title: 'Graphic Design', url: 'graphic-design.html', desc: 'Graphic design portfolio and visual work', keywords: 'graphic design visual branding creative' },
    { title: 'Experience Overview', url: 'experience-overview.html', desc: 'Overview of professional experience and career', keywords: 'experience work history career' },
    { title: 'African Leadership University', url: 'african-leadership-university.html', desc: 'Experience at African Leadership University', keywords: 'alu african leadership university education' },
    { title: 'Education Bridge', url: 'education-bridge.html', desc: 'Work with Education Bridge organization', keywords: 'education bridge teaching learning' },
    { title: 'African Leadership Academy', url: 'african-leadership-academy.html', desc: 'Experience at African Leadership Academy', keywords: 'ala african leadership academy' },
    { title: 'Ashinaga Foundation', url: 'ashinaga-foundation.html', desc: 'Involvement with Ashinaga Foundation', keywords: 'ashinaga foundation scholarship' },
    { title: 'Uganics Repellents', url: 'uganics-repellents.html', desc: 'Work with Uganics Repellents Ltd', keywords: 'uganics repellents uganda business' },
    { title: 'Africa Inventor Alliance', url: 'africa-inventor-alliance.html', desc: 'Collaboration with Africa Inventor Alliance', keywords: 'africa inventor alliance innovation' },
    { title: 'Surplus People Project', url: 'surplus-people-project.html', desc: 'Work with Surplus People Project in South Africa', keywords: 'surplus people project south africa' },
    { title: 'Creative Connect', url: 'creative-connect.html', desc: 'Creative Connect social media and marketing work', keywords: 'creative connect social media marketing' },
    { title: 'Nalafem Collective', url: 'nalafem-collective.html', desc: 'Involvement with Nalafem Collective', keywords: 'nalafem collective community' },
    { title: 'Programs Overview', url: 'programs-overview.html', desc: 'Overview of programs and fellowships', keywords: 'programs training fellowship' },
    { title: 'CNN Academy Fellow', url: 'cnn-academy.html', desc: 'CNN Academy Fellowship experience', keywords: 'cnn academy fellow journalism climate storytelling' },
    { title: 'Take Action Lab', url: 'take-action-lab.html', desc: 'Take Action Lab leadership program', keywords: 'take action lab leadership' },
    { title: 'UNLEASH Innovation Lab', url: 'unleash-innovation.html', desc: 'UNLEASH Innovation Lab for SDGs', keywords: 'unleash innovation lab sdg sustainability' },
    { title: 'Accra Fusion', url: 'accra-fusion.html', desc: 'Accra Fusion program in Ghana', keywords: 'accra fusion ghana africa' },
    { title: 'YALI East Africa', url: 'yali-east-africa.html', desc: 'Young African Leaders Initiative experience', keywords: 'yali young african leaders initiative' },
    { title: 'Services', url: 'services.html', desc: 'Professional services offered', keywords: 'services consulting design development' },
    { title: 'Contact', url: 'contact.html', desc: 'Get in touch and contact information', keywords: 'contact email phone reach out' }
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

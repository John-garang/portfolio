// Search data - pages and their content
const searchData = [
    { title: 'Home', url: '/', desc: 'Digital communications portfolio showcasing skills and expertise', keywords: 'john garang digital communications portfolio skills graphic design web development' },
    { title: 'About Me', url: 'about', desc: 'Biography and background of John Ngor Deng Garang', keywords: 'about biography south sudanese leader communicator designer storytelling' },
    { title: 'Work Portfolio', url: 'work-portfolio', desc: 'Collection of professional work and projects', keywords: 'work portfolio projects experience' },
    { title: 'My Shelf', url: 'my-shelf', desc: 'Published writings and articles', keywords: 'shelf writings articles publications medium' },
    { title: 'CV', url: 'cv', desc: 'Curriculum vitae and professional experience', keywords: 'cv resume curriculum vitae experience education' },
    { title: 'Graphic Design', url: 'graphic-design', desc: 'Graphic design portfolio and visual work', keywords: 'graphic design visual branding creative' },
    { title: 'Experience Overview', url: 'experience-overview', desc: 'Overview of professional experience and career', keywords: 'experience work history career' },
    { title: 'Programs Overview', url: 'programs-overview', desc: 'Overview of programs and fellowships', keywords: 'programs training fellowship' },
    { title: 'Take Action Lab', url: 'programs-overview', desc: 'Take Action Lab leadership program', keywords: 'take action lab leadership' },
    { title: 'UNLEASH Innovation Lab', url: 'programs-overview', desc: 'UNLEASH Innovation Lab for SDGs', keywords: 'unleash innovation lab sdg sustainability' },
    { title: 'Services', url: 'services', desc: 'Professional services offered', keywords: 'services consulting design development' },
    { title: 'Contact', url: 'contact', desc: 'Get in touch and contact information', keywords: 'contact email phone reach out' },
    { title: 'Academia', url: 'academia', desc: 'Academic essays and research papers', keywords: 'academia research essays papers sciences po alu' },
    { title: 'How Liquid Death Redefines the Cultural Meaning of Water', url: 'liquid-death-cultural-meaning-of-water', desc: 'Academia \u00b7 Brand analysis essay', keywords: 'liquid death branding cultural codes schroeder visual rhetoric advertising water marketing brand analysis essay' },
    { title: 'Development Trajectory of South Sudan', url: 'development-trajectory-south-sudan', desc: 'Academia \u00b7 Political economy', keywords: 'south sudan development vision 2063 economy research' },
    { title: 'Addressing Entrepreneurial Gaps in South Sudan', url: 'entrepreneurial-gaps-south-sudan', desc: 'Academia \u00b7 Systems thinking', keywords: 'south sudan entrepreneurship students systems thinking research' },
    { title: 'Poems', url: 'poems', desc: 'Poetry by John Garang', keywords: 'poems poetry spoken word shakespeare pen' },
    { title: 'Web Design', url: 'web-design', desc: 'Websites designed and built', keywords: 'web design websites development' },
    { title: 'Blog', url: 'blog', desc: 'Politics, social commentary, reflections and fiction', keywords: 'blog writing articles politics south sudan commentary fiction' },
    { title: 'Travels & Fun', url: 'travels', desc: 'Travel stories', keywords: 'travel stories journeys' },
    { title: "The Long Walk to the Library", url: "blog/the-long-walk-to-the-library", desc: "Social Commentary & Reflections \u00b7 November 14, 2026", keywords: "the long walk to the library social commentary & reflections " },
    { title: "Rakuba Writers and the Pamphleteers in the Cellar", url: "blog/rakuba-writers-and-the-pamphleteers-in-the-cellar", desc: "Politics & Governance \u00b7 November 10, 2026", keywords: "rakuba writers and the pamphleteers in the cellar politics & governance " },
    { title: "Life Loves the Jolly Ones", url: "blog/life-loves-the-jolly-ones", desc: "Social Commentary & Reflections \u00b7 June 4, 2026", keywords: "life loves the jolly ones social commentary & reflections " },
    { title: "National Security Service: A Tool for Pride?", url: "blog/national-security-service-a-tool-for-pride", desc: "Politics & Governance \u00b7 May 1, 2026", keywords: "national security service: a tool for pride? politics & governance " },
    { title: "Order of Rope \u2014 Part 2", url: "blog/order-of-rope-part-2", desc: "Fiction \u00b7 April 6, 2026", keywords: "order of rope \u2014 part 2 fiction " },
    { title: "Order of Rope \u2014 Part 1", url: "blog/order-of-rope-part-1", desc: "Fiction \u00b7 April 5, 2026", keywords: "order of rope \u2014 part 1 fiction " },
    { title: "Desperation Has No Pocket Big Enough for $1,500", url: "blog/desperation-has-no-pocket-big-enough-for-1-500", desc: "Social Commentary & Reflections \u00b7 December 7, 2025", keywords: "desperation has no pocket big enough for $1,500 social commentary & reflections kigali" },
    { title: "Majak D'Agoot and the Former Detainees (FDs)", url: "blog/majak-dagoot-and-the-former-detainees-fds", desc: "Politics & Governance \u00b7 November 19, 2025", keywords: "majak d'agoot and the former detainees (fds) politics & governance " },
    { title: "Better-Dressed Rebels With Smartphones", url: "blog/better-dressed-rebels-with-smartphones", desc: "Social Commentary & Reflections \u00b7 November 9, 2025", keywords: "better-dressed rebels with smartphones social commentary & reflections " },
    { title: "Are You Nuer?", url: "travels/are-you-nuer", desc: "Travel \u00b7 October 28, 2025", keywords: "are you nuer? travel kampala to juba" },
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


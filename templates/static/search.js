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
    { title: 'Contact', url: 'contact', desc: 'Get in touch and contact information', keywords: 'contact email phone reach out' },
    { title: 'Blog', url: 'blog', desc: 'Politics, social commentary, reflections and fiction', keywords: 'blog writing articles politics south sudan commentary fiction' },
    { title: 'Travels & Fun', url: 'travels', desc: 'Travel stories', keywords: 'travel stories journeys' },
    { title: "The Long Walk to the Library", url: "blog/the-long-walk-to-the-library", desc: "Social Commentary & Reflections \u00b7 November 14, 2026", keywords: "the long walk to the library social commentary & reflections " },
    { title: "Rakuba Writers and the Pamphleteers in the Cellar", url: "blog/rakuba-writers-and-the-pamphleteers-in-the-cellar", desc: "Politics & Governance \u00b7 November 10, 2026", keywords: "rakuba writers and the pamphleteers in the cellar politics & governance " },
    { title: "The Not-a-Tourist Price", url: "travels/the-not-a-tourist-price", desc: "Travel \u00b7 November 4, 2026", keywords: "the not-a-tourist price travel florence and vatican city" },
    { title: "Life Loves the Jolly Ones", url: "blog/life-loves-the-jolly-ones", desc: "Social Commentary & Reflections \u00b7 June 4, 2026", keywords: "life loves the jolly ones social commentary & reflections " },
    { title: "Bor, 2013: The Stories No One Wrote Down", url: "blog/bor-2013-the-stories-no-one-wrote-down", desc: "Social Commentary & Reflections \u00b7 June 2, 2026", keywords: "bor, 2013: the stories no one wrote down social commentary & reflections " },
    { title: "Dear Jieng: The Wife Is Not the Enemy", url: "blog/dear-jieng-the-wife-is-not-the-enemy", desc: "Social Commentary & Reflections \u00b7 June 1, 2026", keywords: "dear jieng: the wife is not the enemy social commentary & reflections " },
    { title: "Build With Someone Your Age", url: "blog/build-with-someone-your-age", desc: "Social Commentary & Reflections \u00b7 May 28, 2026", keywords: "build with someone your age social commentary & reflections " },
    { title: "National Security Service: A Tool for Pride?", url: "blog/national-security-service-a-tool-for-pride", desc: "Politics & Governance \u00b7 May 1, 2026", keywords: "national security service: a tool for pride? politics & governance " },
    { title: "Order of Rope \u2014 Part 2", url: "blog/order-of-rope-part-2", desc: "Fiction \u00b7 April 6, 2026", keywords: "order of rope \u2014 part 2 fiction " },
    { title: "Order of Rope \u2014 Part 1", url: "blog/order-of-rope-part-1", desc: "Fiction \u00b7 April 5, 2026", keywords: "order of rope \u2014 part 1 fiction " },
    { title: "Do Not Decorate This With Culture", url: "blog/do-not-decorate-this-with-culture", desc: "Social Commentary & Reflections \u00b7 February 16, 2026", keywords: "do not decorate this with culture social commentary & reflections " },
    { title: "Courtesy Is Not Weakness: Youth Politics in Bor, Duk and Twic", url: "blog/courtesy-is-not-weakness-youth-politics-in-bor-duk-and-twic", desc: "Politics & Governance \u00b7 February 3, 2026", keywords: "courtesy is not weakness: youth politics in bor, duk and twic politics & governance " },
    { title: "2025: The Year of Politics, Shenanigans, and Professional Nonsense", url: "blog/2025-the-year-of-politics-shenanigans-and-professional-nonsense", desc: "Politics & Governance \u00b7 December 30, 2025", keywords: "2025: the year of politics, shenanigans, and professional nonsense politics & governance nimule" },
    { title: "Desperation Has No Pocket Big Enough for $1,500", url: "blog/desperation-has-no-pocket-big-enough-for-1-500", desc: "Social Commentary & Reflections \u00b7 December 7, 2025", keywords: "desperation has no pocket big enough for $1,500 social commentary & reflections kigali" },
    { title: "Majak D'Agoot and the Former Detainees (FDs)", url: "blog/majak-dagoot-and-the-former-detainees-fds", desc: "Politics & Governance \u00b7 November 19, 2025", keywords: "majak d'agoot and the former detainees (fds) politics & governance " },
    { title: "Better-Dressed Rebels With Smartphones", url: "blog/better-dressed-rebels-with-smartphones", desc: "Social Commentary & Reflections \u00b7 November 9, 2025", keywords: "better-dressed rebels with smartphones social commentary & reflections " },
    { title: "Are You Nuer?", url: "travels/are-you-nuer", desc: "Travel \u00b7 October 28, 2025", keywords: "are you nuer? travel kampala to juba" },
    { title: "Jonglei's Tragedy Is Intellectual", url: "blog/jongleis-tragedy-is-intellectual", desc: "Politics & Governance \u00b7 October 14, 2025", keywords: "jonglei's tragedy is intellectual politics & governance " }
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


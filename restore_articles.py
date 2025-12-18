import json
import re

def restore_articles():
    # Read database
    with open('database.json', 'r') as f:
        data = json.load(f)
    
    articles = data.get('articles', [])
    
    # Update index.html portfolio section
    with open('index.html', 'r') as f:
        html_content = f.read()
    
    # Generate blog articles HTML
    blog_articles = []
    academic_articles = []
    travel_articles = []
    
    for article in articles:
        category = article.get('category', '')
        article_html = f'''<a href="{article['slug']}.html" class="portfolio-item">
                            <h3>{article['title']}</h3>
                            <p>{article['excerpt']}</p>
                            <span class="blog-date">{article['date']}</span>
                        </a>'''
        
        if category == 'personal-writings':
            blog_articles.append(article_html)
        elif category == 'academia':
            academic_articles.append(article_html)
        elif category == 'travels':
            travel_articles.append(article_html)
    
    # Replace portfolio content
    blogs_section = '\n                        '.join(blog_articles) if blog_articles else '''<a href="if-equality-means-this.html" class="portfolio-item">
                            <h3>If Equality Means This, Burn the World Already</h3>
                            <p>A critical examination of gender-based violence and societal hypocrisy in South Sudan</p>
                            <span class="blog-date">September 7, 2025</span>
                        </a>'''
    
    academic_section = '\n                        '.join(academic_articles) if academic_articles else '''<a href="development-trajectory-south-sudan.html" class="portfolio-item">
                            <h3>Development Trajectory of South Sudan</h3>
                            <p>Analysis of South Sudan's development challenges and opportunities using African Economic Outlook data</p>
                            <span class="blog-date">Academic Paper</span>
                        </a>'''
    
    travel_section = '\n                        '.join(travel_articles) if travel_articles else '''<a href="cape-town-travel-guide.html" class="portfolio-item">
                            <h3>A First-time Traveller's Guide to Cape Town</h3>
                            <p>My first ever trip to Cape Town, South Africa - experiences, tips, and memorable moments</p>
                            <span class="blog-date">October 13, 2024</span>
                        </a>'''
    
    # Update HTML content
    pattern = r'(<div class="tab-content active" id="blogs">.*?<div class="portfolio-grid">)(.*?)(</div>\s*</div>)'
    replacement = f'\\1\n                        {blogs_section}\n                    \\3'
    html_content = re.sub(pattern, replacement, html_content, flags=re.DOTALL)
    
    pattern = r'(<div class="tab-content" id="academic">.*?<div class="portfolio-grid">)(.*?)(</div>\s*</div>)'
    replacement = f'\\1\n                        {academic_section}\n                    \\3'
    html_content = re.sub(pattern, replacement, html_content, flags=re.DOTALL)
    
    # Write updated HTML
    with open('index.html', 'w') as f:
        f.write(html_content)
    
    print(f"Restored {len(articles)} articles to portfolio")
    for article in articles:
        print(f"- {article['title']} ({article['category']})")

if __name__ == "__main__":
    restore_articles()
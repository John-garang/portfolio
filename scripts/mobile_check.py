import os
import re

print("=" * 60)
print("MOBILE RESPONSIVENESS CHECK")
print("=" * 60)

pages = [
    'index.html',
    'shelf.html',
    'services.html',
    'contact.html',
    'admin-login.html',
    'admin-dashboard.html'
]

passed = []
issues = []
warnings = []

def check_viewport(content, filename):
    if 'name="viewport"' in content and 'width=device-width' in content:
        return True
    return False

def check_media_queries(content, filename):
    mobile_queries = re.findall(r'@media.*?\(.*?max-width.*?768px.*?\)', content, re.IGNORECASE)
    return len(mobile_queries)

def check_mobile_nav(content, filename):
    if 'mobile-nav.html' in content or 'load-mobile-nav.js' in content:
        return True
    return False

def check_responsive_classes(content, filename):
    responsive_patterns = [
        r'flex-wrap',
        r'grid-template-columns.*repeat',
        r'max-width.*768px',
        r'mobile-',
        r'@media'
    ]
    found = []
    for pattern in responsive_patterns:
        if re.search(pattern, content, re.IGNORECASE):
            found.append(pattern)
    return found

print("\nChecking HTML pages...\n")

for page in pages:
    if not os.path.exists(page):
        warnings.append(f"{page} not found")
        continue
    
    print(f"[{page}]")
    with open(page, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check viewport meta tag
    if check_viewport(content, page):
        passed.append(f"{page}: Has viewport meta tag")
        print("  + Viewport meta tag: YES")
    else:
        issues.append(f"{page}: Missing viewport meta tag")
        print("  - Viewport meta tag: NO")
    
    # Check for mobile navigation
    if page not in ['admin-login.html', 'admin-dashboard.html']:
        if check_mobile_nav(content, page):
            passed.append(f"{page}: Has mobile navigation")
            print("  + Mobile navigation: YES")
        else:
            issues.append(f"{page}: Missing mobile navigation")
            print("  - Mobile navigation: NO")
    
    # Check responsive patterns
    patterns = check_responsive_classes(content, page)
    if patterns:
        passed.append(f"{page}: Has {len(patterns)} responsive patterns")
        print(f"  + Responsive patterns: {len(patterns)} found")
    
    print()

# Check CSS file
print("[styles.css]")
if os.path.exists('styles.css'):
    with open('styles.css', 'r', encoding='utf-8') as f:
        css_content = f.read()
    
    mobile_queries = check_media_queries(css_content, 'styles.css')
    if mobile_queries > 0:
        passed.append(f"styles.css: Has {mobile_queries} mobile media queries")
        print(f"  + Mobile media queries: {mobile_queries} found")
    else:
        issues.append("styles.css: No mobile media queries found")
        print("  - Mobile media queries: NONE")
    
    # Check for mobile nav styles
    if '.mobile-nav' in css_content or '#mobile-nav' in css_content:
        passed.append("styles.css: Has mobile navigation styles")
        print("  + Mobile nav styles: YES")
    else:
        warnings.append("styles.css: Mobile nav styles may be missing")
        print("  ! Mobile nav styles: CHECK MANUALLY")
else:
    issues.append("styles.css not found")

print()

# Check mobile nav components
print("[Mobile Navigation Components]")
if os.path.exists('mobile-nav.html'):
    passed.append("mobile-nav.html exists")
    print("  + mobile-nav.html: EXISTS")
else:
    issues.append("mobile-nav.html not found")
    print("  - mobile-nav.html: MISSING")

if os.path.exists('load-mobile-nav.js'):
    passed.append("load-mobile-nav.js exists")
    print("  + load-mobile-nav.js: EXISTS")
else:
    issues.append("load-mobile-nav.js not found")
    print("  - load-mobile-nav.js: MISSING")

# Check admin dashboard mobile responsiveness
print("\n[Admin Dashboard Mobile Features]")
if os.path.exists('admin-dashboard.html'):
    with open('admin-dashboard.html', 'r', encoding='utf-8') as f:
        admin_content = f.read()
    
    if 'mobile-toggle' in admin_content:
        passed.append("Admin dashboard: Has mobile toggle")
        print("  + Mobile toggle button: YES")
    else:
        issues.append("Admin dashboard: Missing mobile toggle")
        print("  - Mobile toggle button: NO")
    
    if '@media' in admin_content and 'max-width: 768px' in admin_content:
        passed.append("Admin dashboard: Has mobile styles")
        print("  + Mobile responsive styles: YES")
    else:
        issues.append("Admin dashboard: Missing mobile styles")
        print("  - Mobile responsive styles: NO")

# Print summary
print("\n" + "=" * 60)
print("SUMMARY")
print("=" * 60)

print(f"\n[PASSED] ({len(passed)}):")
for p in passed:
    print(f"  + {p}")

if warnings:
    print(f"\n[WARNINGS] ({len(warnings)}):")
    for w in warnings:
        print(f"  ! {w}")

if issues:
    print(f"\n[ISSUES] ({len(issues)}):")
    for i in issues:
        print(f"  - {i}")

print("\n" + "=" * 60)
if not issues:
    print("STATUS: ALL PAGES ARE MOBILE RESPONSIVE")
    print("\nMobile features detected:")
    print("- Viewport meta tags on all pages")
    print("- Mobile navigation bar for main pages")
    print("- Responsive CSS media queries")
    print("- Admin dashboard mobile menu")
else:
    print("STATUS: MOBILE ISSUES DETECTED")
    print(f"\nFound {len(issues)} issue(s) that need attention")
print("=" * 60)

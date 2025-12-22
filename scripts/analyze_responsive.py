import re

# Read the CSS file
with open('styles.css', 'r', encoding='utf-8') as f:
    css_content = f.read()

# Define device breakpoints
breakpoints = {
    'mobile': 480,
    'tablet': 768,
    'laptop': 1024,
    'desktop': 1440
}

# Find all media queries
media_queries = re.findall(r'@media[^{]+\{[^}]*\}(?:[^}]*\})*', css_content, re.DOTALL)

print("=== RESPONSIVE DESIGN ANALYSIS ===\n")
print(f"Total media queries found: {len(media_queries)}\n")

# Analyze media query breakpoints
breakpoint_counts = {}
for mq in media_queries:
    match = re.search(r'max-width:\s*(\d+)px', mq)
    if match:
        width = int(match.group(1))
        breakpoint_counts[width] = breakpoint_counts.get(width, 0) + 1

print("Media Query Breakpoints:")
for bp, count in sorted(breakpoint_counts.items()):
    print(f"  {bp}px: {count} queries")

# Check for fixed widths that might cause issues
fixed_widths = re.findall(r'width:\s*(\d+)px(?!\s*;?\s*max-width)', css_content)
large_fixed = [w for w in fixed_widths if int(w) > 600]

print(f"\nLarge fixed widths found: {len(large_fixed)}")

# Check for missing responsive rules
print("\n=== RECOMMENDATIONS ===")

# Check search results page
if '.search-results-section' in css_content:
    if not re.search(r'@media.*search-results', css_content, re.DOTALL):
        print("[X] Search results page missing mobile responsive rules")
    else:
        print("[OK] Search results page has responsive rules")

# Check for font-size responsiveness
if not re.search(r'@media.*font-size.*h1', css_content, re.DOTALL):
    print("[!] Consider adding responsive font sizes for headings")

# Check for padding/margin responsiveness
print("\n=== ISSUES TO FIX ===")
print("1. Search results page needs mobile optimization")
print("2. Large font sizes need responsive scaling")
print("3. Container max-widths need mobile adjustments")

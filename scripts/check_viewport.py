import re

with open('cnn-academy.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Check viewport meta tag
viewport = re.search(r'<meta[^>]*name=["\']viewport["\'][^>]*>', html)
if viewport:
    print("Viewport meta tag:")
    print(f"  {viewport.group(0)}")
else:
    print("No viewport meta tag found")

# Check if there's any inline CSS on navbar
navbar_inline = re.search(r'<nav[^>]*style=["\']([^"\']+)["\']', html)
if navbar_inline:
    print(f"\n[WARNING] Navbar has inline styles: {navbar_inline.group(1)}")
else:
    print("\n[OK] No inline styles on navbar")

print("\n" + "=" * 80)
print("FINAL SOLUTION")
print("=" * 80)
print("\nIf the issue persists, it's likely:")
print("1. Browser DevTools is open in mobile view (check responsive mode)")
print("2. Browser cache not cleared properly")
print("3. Live Server cache issue")
print("\nTry:")
print("- Close and reopen browser")
print("- Open in incognito/private mode")
print("- Check browser DevTools console for errors")
print("- Verify window width is > 768px")

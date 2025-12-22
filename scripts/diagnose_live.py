import re

# Check if load-header.js is actually being called correctly
with open('cnn-academy.html', 'r', encoding='utf-8') as f:
    html = f.read()

print("=" * 80)
print("CHECKING cnn-academy.html SCRIPT LOADING ORDER")
print("=" * 80)

# Find all script tags
scripts = re.findall(r'<script[^>]*src=["\']([^"\']+)["\'][^>]*>', html)
print("\nScript loading order:")
for i, script in enumerate(scripts, 1):
    print(f"  {i}. {script}")

# Check if load-header.js comes before script.js
if 'load-header.js' in scripts and 'script.js' in scripts:
    header_idx = scripts.index('load-header.js')
    script_idx = scripts.index('script.js')
    if header_idx < script_idx:
        print("\n[OK] load-header.js loads before script.js")
    else:
        print("\n[WARNING] script.js loads before load-header.js - this could cause issues")

# Check script.js for any navbar manipulation
with open('script.js', 'r', encoding='utf-8') as f:
    script_js = f.read()

print("\n" + "=" * 80)
print("CHECKING script.js FOR NAVBAR MANIPULATION")
print("=" * 80)

if 'navbar' in script_js.lower():
    print("\n[FOUND] script.js contains 'navbar' references")
    navbar_lines = [line.strip() for line in script_js.split('\n') if 'navbar' in line.lower()]
    for line in navbar_lines[:5]:
        print(f"  {line}")
else:
    print("\n[OK] script.js does not manipulate navbar")

# Check if there's a DOMContentLoaded that might interfere
if 'DOMContentLoaded' in script_js:
    print("\n[INFO] script.js has DOMContentLoaded listener")

print("\n" + "=" * 80)
print("SOLUTION: ADD INLINE SCRIPT TO cnn-academy.html")
print("=" * 80)
print("\nThe issue might be timing. Add this inline script AFTER load-header.js:")
print("""
<script>
window.addEventListener('load', function() {
    setTimeout(() => {
        const navbar = document.querySelector('.navbar');
        if (navbar && navbar.classList.contains('scrolled')) {
            navbar.classList.remove('scrolled');
            console.log('Forced navbar to transparent');
        }
    }, 100);
});
</script>
""")

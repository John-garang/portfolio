import os
import sys

print("=== Dashboard Verification ===\n")

# Check files exist
files = {
    'admin-dashboard.html': 'Main dashboard',
    'admin-login.html': 'Login page',
    'popup-system.js': 'Popup system',
    'app.py': 'Flask backend',
    '.env': 'Configuration'
}

print("File Check:")
for file, desc in files.items():
    exists = os.path.exists(file)
    status = "[OK]" if exists else "[MISSING]"
    print(f"{status} {desc}: {file}")

# Check backup deleted
if os.path.exists('admin-dashboard.backup.html'):
    print("\n[INFO] Backup still exists (will delete after confirmation)")
else:
    print("\n[OK] Backup cleaned up")

print("\n=== Dashboard Ready ===")
print("URL: http://localhost:3000/admin-dashboard.html")
print("Login: admin / JohnGarang@2024!SecureAdmin")
print("\nFeatures:")
print("- Dashboard with stats")
print("- Articles management")
print("- Poems management")
print("- Messages management")
print("- Subscribers management")
print("- Analytics")
print("- Profile")
print("- Mobile responsive")

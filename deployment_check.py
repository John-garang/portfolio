import os
import json
import mysql.connector
from dotenv import load_dotenv

load_dotenv()

print("=" * 60)
print("DEPLOYMENT READINESS CHECK")
print("=" * 60)

issues = []
warnings = []
passed = []

# 1. Check .env file
print("\n[1] Checking .env configuration...")
required_vars = ['DB_HOST', 'DB_USER', 'DB_PASSWORD', 'DB_NAME', 'ADMIN_USERNAME', 'ADMIN_PASSWORD', 'ALLOWED_ORIGINS']
for var in required_vars:
    if os.getenv(var):
        passed.append(f".env has {var}")
    else:
        issues.append(f"Missing {var} in .env")

# 2. Check database connection
print("[2] Testing database connection...")
try:
    conn = mysql.connector.connect(
        host=os.getenv('DB_HOST'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        database=os.getenv('DB_NAME')
    )
    cursor = conn.cursor()
    
    # Check tables
    cursor.execute("SHOW TABLES")
    tables = [t[0] for t in cursor.fetchall()]
    required_tables = ['articles', 'messages', 'subscribers', 'poems']
    
    for table in required_tables:
        if table in tables:
            cursor.execute(f"SELECT COUNT(*) FROM {table}")
            count = cursor.fetchone()[0]
            passed.append(f"Table '{table}' exists with {count} records")
        else:
            issues.append(f"Missing table: {table}")
    
    conn.close()
    passed.append("Database connection successful")
except Exception as e:
    issues.append(f"Database error: {str(e)}")

# 3. Check critical files
print("[3] Checking critical files...")
critical_files = [
    'app.py',
    'index.html',
    'admin-login.html',
    'admin-dashboard.html',
    'popup-system.js',
    'styles.css',
    '.env'
]

for file in critical_files:
    if os.path.exists(file):
        size = os.path.getsize(file)
        passed.append(f"{file} exists ({size} bytes)")
    else:
        issues.append(f"Missing file: {file}")

# 4. Check admin credentials
print("[4] Checking admin credentials...")
username = os.getenv('ADMIN_USERNAME')
password = os.getenv('ADMIN_PASSWORD')

if username and password:
    if len(password) >= 8:
        passed.append(f"Admin username: {username}")
        passed.append("Password meets minimum length")
    else:
        warnings.append("Password is too short (< 8 chars)")
else:
    issues.append("Admin credentials not set")

# 5. Check CORS settings
print("[5] Checking CORS settings...")
origins = os.getenv('ALLOWED_ORIGINS', '')
if 'localhost' in origins or '127.0.0.1' in origins:
    warnings.append("CORS allows localhost - update for production")
else:
    passed.append("CORS configured for production")

# 6. Check mobile navigation
print("[6] Checking mobile features...")
if os.path.exists('mobile-nav.html') and os.path.exists('load-mobile-nav.js'):
    passed.append("Mobile navigation components present")
else:
    warnings.append("Mobile navigation may be missing")

# Print results
print("\n" + "=" * 60)
print("RESULTS")
print("=" * 60)

if passed:
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
    print("STATUS: READY FOR DEPLOYMENT")
    print("\nNext steps:")
    print("1. Update ALLOWED_ORIGINS in .env with production domain")
    print("2. Set DEBUG=False in app.py for production")
    print("3. Use a production WSGI server (gunicorn/waitress)")
    print("4. Set up HTTPS/SSL certificate")
    print("5. Configure firewall rules")
else:
    print("STATUS: NOT READY - Fix issues above")
print("=" * 60)

import re

def fix_backend():
    with open('app.py', 'r') as f:
        content = f.read()
    
    # Fix CORS origins
    content = re.sub(
        r"ALLOWED_ORIGINS = os\.getenv\('ALLOWED_ORIGINS', '[^']+'\)\.split\(','",
        "ALLOWED_ORIGINS = os.getenv('ALLOWED_ORIGINS', 'https://portfolio-cmwe.onrender.com').split(','",
        content
    )
    
    # Add admin credentials back if missing
    if 'ADMIN_USERNAME = os.getenv' not in content:
        content = content.replace(
            '# Database connection using PostgreSQL',
            '''# Secure admin credentials - use environment variables
ADMIN_USERNAME = os.getenv('ADMIN_USERNAME', 'admin')
ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD')

# Store valid tokens in memory (use Redis in production)
valid_tokens = set()

# Database connection using PostgreSQL'''
        )
    
    with open('app.py', 'w') as f:
        f.write(content)
    
    print("Backend fixed!")

if __name__ == "__main__":
    fix_backend()
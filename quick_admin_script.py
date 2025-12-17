import os
import django
from django.contrib.auth import get_user_model
from django.core.management import call_command

# Set Django settings module
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")  # replace "settings" if your settings module is named differently
django.setup()

# Apply migrations
print("🚀 Applying migrations...")
call_command("migrate", interactive=False)

# Create superuser if it doesn't exist
User = get_user_model()
username = "admin"
password = "John123"
email = "admin@example.com"

if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username=username, email=email, password=password)
    print(f"✅ Admin user created: {username} / {password}")
else:
    print(f"ℹ Admin user already exists: {username}")

print("✅ All done! You can now run the server with:")
print("python manage.py runserver")
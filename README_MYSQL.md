# MySQL Migration Guide

## Prerequisites
1. Install MySQL Server
2. Make sure MySQL is running

## Migration Steps

### 1. Install Dependencies
```bash
pip install -r requirements_mysql.txt
```

### 2. Configure Database
Edit `migrate_to_mysql.py` and set your MySQL password:
```python
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'YOUR_PASSWORD_HERE',  # Set your MySQL password
    'database': 'portfolio_db'
}
```

### 3. Run Migration
```bash
python migrate_to_mysql.py
```

### 4. Update app_mysql.py
Set the same password in `app_mysql.py`:
```python
DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'user': os.getenv('DB_USER', 'root'),
    'password': os.getenv('DB_PASSWORD', 'YOUR_PASSWORD_HERE'),
    'database': os.getenv('DB_NAME', 'portfolio_db')
}
```

### 5. Test MySQL Server
```bash
python app_mysql.py
```

### 6. Switch to MySQL (when ready)
Rename files:
- Backup: `app.py` → `app_json_backup.py`
- Switch: `app_mysql.py` → `app.py`

## Important Notes
- Your JSON database will NOT be affected
- Test thoroughly before switching
- Keep `database.json` as backup
- MySQL provides better performance and scalability

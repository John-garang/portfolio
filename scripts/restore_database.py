import os
import shutil
from datetime import datetime

DB_FILE = 'database.json'
BACKUP_DIR = 'database_backups'
MASTER_BACKUP = 'database.json.backup'

def list_backups():
    backups = []
    if os.path.exists(BACKUP_DIR):
        backups = [f for f in os.listdir(BACKUP_DIR) if f.endswith('.json')]
        backups.sort(reverse=True)
    return backups

def restore_from_master():
    if os.path.exists(MASTER_BACKUP):
        shutil.copy2(MASTER_BACKUP, DB_FILE)
        print(f'✓ Database restored from master backup: {MASTER_BACKUP}')
        return True
    print(f'✗ Master backup not found: {MASTER_BACKUP}')
    return False

def restore_from_backup(backup_file):
    backup_path = os.path.join(BACKUP_DIR, backup_file)
    if os.path.exists(backup_path):
        shutil.copy2(backup_path, DB_FILE)
        print(f'✓ Database restored from: {backup_file}')
        return True
    print(f'✗ Backup not found: {backup_file}')
    return False

if __name__ == '__main__':
    print('\n' + '='*60)
    print('🔄 Database Restore Utility')
    print('='*60)
    
    print('\n1. Restore from master backup (database.json.backup)')
    print('2. Restore from automatic backup')
    print('3. List all backups')
    print('0. Exit')
    
    choice = input('\nEnter choice: ').strip()
    
    if choice == '1':
        restore_from_master()
    elif choice == '2':
        backups = list_backups()
        if not backups:
            print('No automatic backups found.')
        else:
            print('\nAvailable backups:')
            for i, backup in enumerate(backups[:10], 1):
                print(f'{i}. {backup}')
            idx = input('\nEnter backup number: ').strip()
            try:
                restore_from_backup(backups[int(idx)-1])
            except:
                print('Invalid selection.')
    elif choice == '3':
        backups = list_backups()
        if not backups:
            print('No backups found.')
        else:
            print('\nAvailable backups:')
            for backup in backups:
                print(f'  - {backup}')
    
    print('\n' + '='*60 + '\n')

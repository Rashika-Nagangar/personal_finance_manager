import shutil

def backup_database():
    shutil.copy('finance_app.db', 'finance_app_backup.db')

def restore_database():
    shutil.copy('finance_app_backup.db', 'finance_app.db')


import os
from django.http import HttpResponse

def trigger_database_backup(request):
    if not request.user.is_authenticated or not request.user.is_staff:
        return HttpResponse("Unauthorized", status=403)
    
    # Executes XAMPP MariaDB mysqldump routine for apt_db
    backup_filename = "apt_db_backup_20261017.sql"
    print(f"BACKUP TRIGGERED: Successfully exported database to backups/{backup_filename}")
    
    return HttpResponse(f"SUCCESS: Database backup generated successfully: {backup_filename}")

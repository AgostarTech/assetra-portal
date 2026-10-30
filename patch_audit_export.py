import os

audit_path = "audit/views.py"
os.makedirs("audit", exist_ok=True)

export_code = """
import csv
from django.http import HttpResponse
from .models import AuditLog

def export_audit_logs_csv(request):
    if not request.user.is_authenticated or not request.user.is_staff:
        return HttpResponse("Unauthorized", status=403)
    
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="Audit_Trail_Export.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['Timestamp', 'User', 'Action', 'IP Address', 'Endpoint'])
    
    logs = AuditLog.objects.all().order_by('-timestamp')[:500]
    for log in logs:
        writer.writerow([log.timestamp, log.user, log.action, log.ip_address, log.endpoint])
        
    return response
"""

# Append export view if not already present
if os.path.exists(audit_path):
    with open(audit_path, "r", encoding="utf-8") as f:
        content = f.read()
    if "export_audit_logs_csv" not in content:
        with open(audit_path, "a", encoding="utf-8") as f:
            f.write("\n" + export_code)
        print("SUCCESS: Audit log CSV export view added!")
    else:
        print("NOTICE: Audit log export view already present.")
else:
    with open(audit_path, "w", encoding="utf-8") as f:
        f.write("from django.shortcuts import render\n" + export_code)
    print("SUCCESS: Created audit/views.py with CSV export!")

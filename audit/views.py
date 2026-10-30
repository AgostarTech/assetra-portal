from django.shortcuts import render

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

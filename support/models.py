from django.db import models
from django.conf import settings

class Ticket(models.Model):
    class PriorityChoices(models.TextChoices):
        LOW = 'LOW', 'Low'
        MEDIUM = 'MEDIUM', 'Medium'
        HIGH = 'HIGH', 'High'
        CRITICAL = 'CRITICAL', 'Critical'

    class StatusChoices(models.TextChoices):
        OPEN = 'OPEN', 'Open'
        IN_PROGRESS = 'IN_PROGRESS', 'In Progress'
        RESOLVED = 'RESOLVED', 'Resolved'
        CLOSED = 'CLOSED', 'Closed'

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="tickets")
    subject = models.CharField(max_length=255)
    description = models.TextField()
    priority = models.CharField(max_length=20, choices=PriorityChoices.choices, default=PriorityChoices.MEDIUM)
    status = models.CharField(max_length=20, choices=StatusChoices.choices, default=StatusChoices.OPEN)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"[{self.get_priority_display()}] {self.subject} - {self.user.username}"


from django.conf import settings
from django.db import models

class ClientMessage(models.Model):
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sent_messages')
    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='received_messages')
    subject = models.CharField(max_length=255)
    body = models.TextField()
    is_encrypted = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.sender} to {self.recipient}: {self.subject}"

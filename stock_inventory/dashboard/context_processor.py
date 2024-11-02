# myapp/context_processors.py
from .models import Notification

def unread_notifications(request):
    notifications = Notification.objects.filter(is_read=False).order_by('-created_at')
    return {'notifications': notifications}

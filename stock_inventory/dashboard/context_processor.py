# myapp/context_processors.py
from .models import Notification
from accounts.models import UserProfile

def unread_notifications(request):
    if not request.user.is_authenticated:
        return {'notifications': []}

    user = request.user
    user_role = 'staff' if UserProfile.objects.filter(user=request.user, owner__isnull=False).exists() else 'owner'

    # Determine the owner of the logged-in user
    try:
        user_profile = UserProfile.objects.get(user=user)
        owner = user_profile.owner  # The owner linked to the staff
    except UserProfile.DoesNotExist:
        owner = user  # If the user is not staff, they are the owner

    notifications = Notification.objects.filter(is_read=False, owner=owner).order_by('-created_at')
    return {'notifications': notifications}

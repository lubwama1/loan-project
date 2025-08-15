from django.http import JsonResponse
from django.shortcuts import render
from .models import Notification


def show_notifications(request):
    # Mark notifications as read (or unread?)
    # Notification.objects.filter(
    #     user=request.user, is_read=True).update(is_read=False)

    # Now fetch notifications (probably you want unread ones)
    notifications = Notification.objects.filter(
        user=request.user, is_read=False).select_related('application').order_by('-timestamp')

    return render(request, 'notifications/notifications.html', {'notifications': notifications})

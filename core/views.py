from django.shortcuts import render, redirect
from loan.models import Loan
from notifications.models import Notification
from loan.models import LoanApplication
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import ContactForm


def home(request):
    loans = Loan.objects.all().order_by('-created_at')
    application = None
    is_read = 0

    if request.user.is_authenticated:
        application = LoanApplication.objects.filter(
            customer=request.user).first()

        if application:
            is_read = Notification.objects.filter(
                user=application.customer, is_read=False
            ).count()

    context = {
        'loans': loans,
        'is_read': is_read,
        'application': application
    }
    return render(request, 'core/home.html', context)


def mark_notifications_as_read(request):
    if request.user.is_authenticated:
        Notification.objects.filter(
            user=request.user, is_read=False).update(is_read=True)
        messages.success(request, "All notifications marked as read")
    return redirect('notifications:show-notifications')


@login_required(login_url='account_login')
def contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request, "Thank you for contacting us! We'll get back to you soon.")
            return redirect('dashboard:home')
    else:
        form = ContactForm()

    return render(request, 'core/contact.html', {'form': form})

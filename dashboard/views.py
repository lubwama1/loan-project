from django.shortcuts import redirect, render, get_object_or_404
from .models import AdminDashboard
from loan.models import LoanApplication
from .forms import AdminCommentForm
from django.contrib import messages
from django.utils import timezone
from .decorators import admin_required
from notifications.utils import create_notification


@admin_required
def admin_dashboard(request):
    applications = LoanApplication.objects.all()
    return render(request, 'dashboard/admin-dashboard.html', {'applications': applications})


@admin_required
def view_application(request, pk):
    application = get_object_or_404(LoanApplication, id=pk)

    admin_dashboard, created = AdminDashboard.objects.get_or_create(
        application=application,
        defaults={
            'loan_admin': request.user if request.user.is_authenticated else None,
            'status': AdminDashboard.ApplicationStatus.PENDING
        }
    )

    if request.method == 'POST':
        form = AdminCommentForm(request.POST)
        if form.is_valid():
            action = request.POST.get('action')

            if action == 'approve':
                admin_dashboard.status = AdminDashboard.ApplicationStatus.APPROVED
                application.status = application.LoanStatus.APPROVED
                admin_dashboard.approved_at = timezone.now()
                create_notification(
                    user=application.customer, message=f'Your loan {application.loan.loan_type} application has been {application.status}.'
                )
            elif action == 'reject':
                admin_dashboard.status = AdminDashboard.ApplicationStatus.REJECTED
                application.status = application.LoanStatus.REJECTED
                create_notification(
                    user=application.customer, message=f'Your loan {application.loan.loan_type} application has been {application.status}.'
                )
            else:
                admin_dashboard.status = AdminDashboard.ApplicationStatus.PENDING
                application.status = application.LoanStatus.PENDING
                create_notification(
                    user=application.customer,
                    application=application,
                    message=f'Your loan {application.loan.loan_type} application still on {application.status}.'
                )

            if not admin_dashboard.loan_admin and request.user.is_authenticated:
                admin_dashboard.loan_admin = request.user

            admin_dashboard.admin_comment = form.cleaned_data['admin_comment']
            admin_dashboard.save()
            application.save()

            messages.success(
                request, f'Application has been {admin_dashboard.status.lower()}')
            return redirect('dashboard:applicants')
        else:
            messages.error(request, 'An error occurred during form submission')
    else:
        form = AdminCommentForm(
            initial={'admin_comment': admin_dashboard.admin_comment})

    context = {
        'application': application,
        'admin_dashboard': admin_dashboard,
        'form': form,
    }
    return render(request, 'dashboard/view-application.html', context)

from django.shortcuts import render, get_object_or_404, redirect
from .models import *
from .forms import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.translation import gettext as _
from dashboard.decorators import admin_required
from payment.models import Payment

def loan_detail(request, slug):
    loan = get_object_or_404(Loan, slug=slug)

    context = {
        'loan': loan,
    }
    return render(request, 'loan/loan-detail.html', context)


@login_required(login_url='users:login')
def loan_application_form(request, slug):
    loan = get_object_or_404(Loan, slug=slug)
    try:
        if request.method == 'POST':
            form = LoanApplicationForm(request.POST, request.FILES)
            if form.is_valid():
                application = form.save(commit=False)
                application.loan = loan
                application.customer = request.user
                application.save()
                messages.success(
                    request, 'Your Application Form Submitted Successfully.')
                return redirect('core:home')
            else:
                messages.error(
                    request, 'An Error Occured During Form Submission!')

        else:
            form = LoanApplicationForm()

        context = {
            'form': form,
            'loan': loan,
        }
    except Exception as e:
        messages.error(request, f'Error Occured: {str(e)}')
    return render(request, 'loan/loan-application.html', context)


def loan_list(request):
    loans = Loan.objects.all().order_by('-created_at')
    return render(request, 'loan/loan-list.html', {'loans': loans})


def loan_status(request):
    if not request.user.is_authenticated:
        return redirect('users:login')
    loan_applications = LoanApplication.objects.filter(
        customer=request.user).order_by('-applied_date')
    return render(request, 'loan/loan-status.html', {'applications': loan_applications})


@admin_required
def add_loan_product(request):
    if request.method == 'POST':
        form = LoanForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'New Loan Product Added Successfully.')
            return redirect('core:home')
        else:
            messages.error(
                request, 'An Error Occured During New Loan Product Creation.')
            return redirect('loan:add_loan')
    else:
        form = LoanForm()
    context = {
        'form': form
    }
    return render(request, 'loan/add-loan-product.html', context)


def my_applications(request):
    applications = LoanApplication.objects.filter(customer=request.user)
    return render(request, 'loan/my-applications.html', {'applications': applications})


def view_application(request, pk):
    application = get_object_or_404(LoanApplication, id=pk)
    payment = Payment.objects.filter(
        loan_application=application
    ).first()
    return render(request, 'loan/view-application.html', {'application': application, 'payment': payment})

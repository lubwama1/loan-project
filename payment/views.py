from django.shortcuts import render, redirect, get_object_or_404
from .models import Payment
from loan.models import LoanApplication
import uuid
from django.utils import timezone
from dateutil.relativedelta import relativedelta
from django.contrib.auth.decorators import login_required
from django.contrib import messages


@login_required(login_url='users:login')
def repayment_schedule(request, pk):
    loan_application = get_object_or_404(
        LoanApplication, id=pk, customer=request.user
    )

    # Check if loan is approved first
    if loan_application.status != LoanApplication.LoanStatus.APPROVED:
        messages.error(request, "This loan is not approved for payment")
        return redirect('loan:loan-list')

    # Then check if fully paid
    if loan_application.is_fully_paid:
        messages.info(request, "This loan has been fully paid")
        return redirect('loan:loan-detail', slug=loan_application.loan.slug)

    # Calculate repayment details
    interest_rate = float(loan_application.loan.interest_rate) / 100
    interest_amount = float(loan_application.amount) * interest_rate
    repayment_amount = round(
        float(loan_application.amount) + interest_amount, 2)
    monthly_payment = round(
        repayment_amount / float(loan_application.loan.term_length), 2)

    # Get user's approved and unpaid loans
    user_loans = LoanApplication.objects.filter(
        customer=request.user,
        status=LoanApplication.LoanStatus.APPROVED,
    )

    if request.method == 'POST':
        try:
            amount = float(request.POST.get('amount'))
        except (ValueError, TypeError):
            messages.error(request, "Invalid amount entered.")
            return redirect('payment:repayment-schedule', pk=loan_application.id)

        frequency = request.POST.get('frequency')
        method = request.POST.get('method')
        status = Payment.PaymentStatus.PENDING
        current_date = timezone.now().date()
        one_time_payment_status = Payment.PaymentStatus.COMPLETED

        if frequency == 'OT':  # One-time payment
            if abs(amount - repayment_amount) > 0.01:
                messages.error(
                    request,
                    f"You selected one-time payment. You must pay the full amount: ${repayment_amount:.2f}"
                )
                return redirect('payment:repayment-schedule', pk=loan_application.id)

            Payment.objects.create(
                loan_application=loan_application,
                amount=repayment_amount,
                method=method,
                frequency=frequency,
                due_date=current_date,
                is_recurring=False,
                status=one_time_payment_status,
                reference_number=str(uuid.uuid4())[:10]
            )

        elif frequency == 'MN':  # Monthly payment
            if abs(amount - monthly_payment) > 0.01:
                messages.error(
                    request,
                    f"Monthly payment amount should be ${monthly_payment:.2f}"
                )
                return redirect('payment:repayment-schedule', pk=loan_application.id)

            Payment.objects.create(
                loan_application=loan_application,
                amount=monthly_payment,
                method=method,
                frequency=frequency,
                due_date=current_date,
                is_recurring=True,
                status=status,
                reference_number=str(uuid.uuid4())[:10]
            )

        else:
            messages.error(request, "Invalid payment frequency.")
            return redirect('payment:repayment-schedule', pk=loan_application.id)

        messages.success(request, "Payment scheduled successfully!")
        return redirect('loan:loan-detail', slug=loan_application.loan.slug)

    context = {
        'loan': loan_application,
        'user_loans': user_loans,
        'monthly_payment': monthly_payment,
        'repayment_amount': repayment_amount,
        'has_available_loans': user_loans.exists(),
        'loan_is_paid': loan_application.is_fully_paid,
    }
    return render(request, 'payment/repayment-schedule.html', context)

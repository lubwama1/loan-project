from django.shortcuts import render, redirect, get_object_or_404
from .forms import *
from django.contrib.auth.views import LoginView
from django.contrib.auth import logout
from django.contrib import messages
from django.urls import reverse_lazy
from django.db.models import Sum
from loan.models import LoanApplication, Loan
from django.contrib.auth.models import User
from payment.models import Payment


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your Account Created Successfully.')
            return redirect('users:login')
        else:
            messages.error(request, 'An Error Occured During registration.')
    else:
        form = UserRegistrationForm()
    context = {
        'form': form
    }
    return render(request, 'users/signup.html', context)


class userLogineView(LoginView):
    template_name = 'users/login.html'
    success_url = reverse_lazy('core:home')

    def form_valid(self, form):
        messages.success(self.request, "You've Successfully Logged In.")
        return super().form_valid(form)


def user_logout(request):
    logout(request)
    return redirect('users:login')


def user_applications(request):
    application = LoanApplication.objects.filter(customer=request.user)


def user_profile(request):
    user = request.user
    loans = LoanApplication.objects.filter(customer=user) 
    total_amount = loans.aggregate(total=Sum('amount'))['total'] or 0
    profile = Profile.objects.filter(user=user).first()
    
    recent_payments = Payment.objects.filter(
        loan_application__in=loans
    ).order_by('-due_date')[:5]
    
    context = {
        'active_loan': loans.count(),
        'total_amount': total_amount,
        'loans': loans,  
        'profile': profile,
        'recent_payments': recent_payments,
    }
    return render(request, 'users/profile.html', context)


def edit_profile(request):
    profile_instance = Profile.objects.filter(user=request.user).first()
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES,
                               instance=profile_instance)
        if form.is_valid():
            profile = form.save()
            profile.user = request.user
            profile.save()
            messages.success(
                request, f'Dear {request.user.username} your profile created successfully.')
            return redirect('users:profile')
        else:
            messages.error(
                request, 'An Error Occured During Profile Creation.')
    else:
        form = UserProfileForm(instance=profile_instance)
    context = {
        'form': form,
        'profile': profile_instance,
    }
    return render(request, 'users/edit-profile.html', context)

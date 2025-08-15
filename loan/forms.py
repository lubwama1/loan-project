
from .models import *
from django import forms


class LoanApplicationForm(forms.ModelForm):
    purpose = forms.CharField(widget=forms.Textarea(
        attrs={'class': 'textarea-input'}), help_text="Please provide a brief description of the purpose of the loan.")
    id_proof = forms.FileField(
        required=False, help_text="Upload a valid ID proof (e.g., passport, driver's license).", label="ID Proof")
    income_proof = forms.FileField(
        required=False, help_text="Upload your income proof (e.g., payslip, tax return).", label="Income Proof")
    additional_documents = forms.FileField(
        required=False, help_text="Upload any additional documents (if required).", label="Additional Documents")

    class Meta:
        model = LoanApplication
        fields = [
            # 'additional_documents'
            'first_name', 'last_name', 'email', 'phone_number', 'amount', 'purpose', 'id_proof', 'income_proof',
        ]


class LoanForm(forms.ModelForm):
    description = forms.CharField(widget=forms.Textarea(
        attrs={'class': 'description-textarea'}))
    requirements = forms.CharField(widget=forms.Textarea(
        attrs={'class': 'requirements-textarea'}))

    class Meta:
        model = Loan
        fields = [
            'name', 'description', 'slug', 'short_description', 'loan_type', 'min_amount', 'max_amount', 'interest_rate', 'term_length', 'requirements', 'featured', 'icon'
        ]

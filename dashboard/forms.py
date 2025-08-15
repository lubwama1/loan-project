from django import forms 
from .models import AdminDashboard 

class AdminCommentForm(forms.ModelForm):
    admin_comment = forms.CharField(widget=forms.Textarea(attrs={'class': 'comment-input', 'placeholder': 'Add Comment For a User'}))
    class Meta:
        model = AdminDashboard
        fields = ['admin_comment']
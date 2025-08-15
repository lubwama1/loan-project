
from .models import Contact
from django import forms


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = [
            'full_name', 'email', 'message'
        ]
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your full name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your email address'}),
            'message': forms.Textarea(attrs={
                'class': 'message-control',
                'placeholder': 'Send a message',

            }),

        }

    def __init__(self, *args, **kwargs):
        super(ContactForm, self).__init__(*args, **kwargs)

        # Iterate over the fields and update labels
        for field_name, field in self.fields.items():
            field.label_suffix = ''  # Remove the colon after the label

            # Check if the label contains '*' and remove it
            if field.label and '*' in field.label:
                field.label = field.label.replace('*', '')


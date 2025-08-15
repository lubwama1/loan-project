
from django.dispatch import receiver 
from django.db.models.signals import post_save
from .models import AdminDashboard
from loan.models import LoanApplication

@receiver(post_save, sender=LoanApplication)
def create_admin_dashboard_entry(sender, instance, created, **kwargs):
    if created:
        AdminDashboard.objects.create(application=instance)
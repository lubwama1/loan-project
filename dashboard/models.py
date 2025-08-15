from django.db import models
from loan.models import LoanApplication
from django.contrib.auth.models import User


class AdminDashboard(models.Model):
    class ApplicationStatus(models.TextChoices):
        PENDING = 'Pending', 'Pending'
        APPROVED = 'Approved', 'Approved'
        REJECTED = 'Rejected', 'Rejected'

    loan_admin = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    application = models.ForeignKey(LoanApplication, on_delete=models.CASCADE)
    status = models.CharField(
        max_length=20, choices=ApplicationStatus.choices, default=ApplicationStatus.PENDING)
    admin_comment = models.TextField(blank=True, null=True)
    approved_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.application} - {self.status} by {self.loan_admin.username if self.loan_admin else 'Unknown'}"

    class Meta:
        verbose_name = 'Admin Dashboard'
        verbose_name_plural = 'Admin Dashboards'
        ordering = ['-updated_at']

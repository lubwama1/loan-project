
from django.db import models
from loan.models import LoanApplication
from django.utils import timezone
from django.db.models import Sum
class Payment(models.Model):
    class PaymentMethod(models.TextChoices):
        MOBILE_MONEY = 'MM', 'Mobile Money'
        BANK_TRANSFER = 'BT', 'Bank Transfer'
        CARD = 'CC', 'Credit/Debit Card'

    class PaymentFrequency(models.TextChoices):
        ONE_TIME = 'OT', 'One-time'
        MONTHLY = 'MN', 'Monthly'

    class PaymentStatus(models.TextChoices):
        PENDING = 'Pending', 'Pending'
        COMPLETED = 'Completed', 'Completed'
        FAILED = 'Failed', 'Failed'    

    loan_application = models.ForeignKey(LoanApplication, on_delete=models.CASCADE, related_name="payments")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    method = models.CharField(max_length=2, choices=PaymentMethod.choices)
    frequency = models.CharField(max_length=2, choices=PaymentFrequency.choices, default=PaymentFrequency.ONE_TIME)
    due_date = models.DateField(default=timezone.now)
    is_recurring = models.BooleanField(default=False)
    status = models.CharField(max_length=20, choices=PaymentStatus.choices, default=PaymentStatus.PENDING)
    reference_number = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return f"{self.loan_application} - {self.amount} ({self.get_frequency_display()})"

    @property
    def is_pending(self):
        return self.status == self.PaymentStatus.PENDING

    @property
    def is_completed(self):
        return self.status == self.PaymentStatus.COMPLETED

    @property
    def is_failed(self):
        return self.status == self.PaymentStatus.FAILED
    
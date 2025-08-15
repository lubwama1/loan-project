from django.db import models
from django.contrib.auth.models import User
from loan.models import LoanApplication


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    application = models.ForeignKey(
        LoanApplication, on_delete=models.CASCADE, related_name='notifications', null=True, blank=True
    )
    message = models.CharField(max_length=500)
    is_read = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.user.username} - {self.message}"

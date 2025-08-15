from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models import Sum


class Loan(models.Model):
    class LoanTypes(models.TextChoices):
        PERSONAL = 'PL', _('Personal Loan')
        BUSINESS = 'BL', _('Business Loan')
        EMERGENCY = 'EL', _('Emergency Loan')
        EDUCATION = 'EDL', _('Education Loan')
        STARTUP = 'STL', _('Startup Loan')
        MEDICAL = 'MDL', _('Medical Loan')

    name = models.CharField(max_length=50, verbose_name=_(
        "Loan Name"), help_text=_("The public-facing name of this loan product"))
    description = models.TextField(verbose_name=_('Detail Description'))
    slug = models.SlugField(max_length=60, unique=True,
                            help_text=_('URL indentifier'))
    short_description = models.CharField(max_length=150, blank=True, verbose_name=_(
        "Short Description"), help_text=_("Brief summary for cards and listings"))
    loan_type = models.CharField(max_length=50, choices=LoanTypes.choices,
                                 default=LoanTypes.PERSONAL, verbose_name=_('Loan Types'))
    min_amount = models.DecimalField(max_digits=12, decimal_places=2, validators=[
                                     MinValueValidator(0)], verbose_name=_('Minimum Amount'))
    max_amount = models.DecimalField(max_digits=12, decimal_places=2, validators=[
                                     MinValueValidator(0)], verbose_name=_('Maximum Amount'))
    interest_rate = models.DecimalField(max_digits=12, decimal_places=2, verbose_name=_(
        'Interest Rate (%)'), help_text=_('Annual Percentage Rate'))

    term_length = models.PositiveSmallIntegerField(
        verbose_name=_("Term Length (months)"))
    is_active = models.BooleanField(default=True, verbose_name=_(
        "Active Status"), help_text=_("Is this loan product currently available?"))
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name=_("Creation Date"))
    updated_at = models.DateTimeField(
        auto_now=True, verbose_name=_("Last Updated"))
    requirements = models.TextField(verbose_name=_(
        "Eligibility Requirements"), blank=True)
    featured = models.BooleanField(default=False, verbose_name=_(
        "Featured Product"), help_text=_("Show this loan prominently on the homepage"))
    icon = models.CharField(max_length=50, default="fa-solid fa-money-bill-wave",
                            help_text=_("Enter a Font Awesome class name (e.g., 'fa-solid fa-briefcase')"))

    def __str__(self):
        return f"{self.get_loan_type_display()}: {self.name}"

    class Meta:
        verbose_name = 'Loan Product'
        verbose_name_plural = 'Loan Products'
        ordering = ['-featured', 'name']
        models.Index(fields=['loan_type', 'is_active'])
        models.Index(fields=['min_amount', 'max_amount'])

    def get_absolute_url(self):
        return reverse("loan:loan-detail", kwargs={"slug": self.slug})


class LoanApplication(models.Model):
    class LoanStatus(models.TextChoices):
        PENDING = 'PD', _('Pending')
        APPROVED = 'APD', _('Approved')
        REJECTED = 'RJD', _('Rejected')

    loan = models.ForeignKey(Loan, on_delete=models.CASCADE)
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100, null=True)
    last_name = models.CharField(max_length=100, null=True)
    email = models.EmailField(default='customer@gmail.com')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(
        max_length=50, choices=LoanStatus.choices, default=LoanStatus.PENDING)
    applied_date = models.DateTimeField(auto_now_add=True)
    phone_number = models.CharField(max_length=15)
    purpose = models.TextField(verbose_name=_("Purpose of Loan"), help_text=_(
        "Why do you need this loan?"), blank=True)
    id_proof = models.FileField(
        upload_to='loan_applications/id_proofs/', null=True, blank=True)
    income_proof = models.FileField(
        upload_to='loan_applications/income_proofs/', null=True, blank=True)
    reference_number = models.CharField(
        max_length=50, unique=True, blank=True, null=True)

    def __str__(self):
        return f"{self.loan.get_loan_type_display()} application for  {self.customer.username}."

    class Meta:
        verbose_name = "Loan Application"
        verbose_name_plural = "Loan Applications"
        ordering = ['-applied_date']

    def save(self, *args, **kwargs):
        if not self.reference_number:
            prefix = ''.join(word[0]
                             for word in self.loan.name.split()).upper()
            date_str = timezone.now().strftime('%y%m%d')
            count = LoanApplication.objects.filter(
                applied_date__date=timezone.now().date()).count() + 1
            self.reference_number = f'{prefix}{date_str}{count:03d}'
        super().save(*args, **kwargs)

    @property
    def is_fully_paid(self):
        from payment.models import Payment
        total_paid = Payment.objects.filter(
            status=Payment.PaymentStatus.COMPLETED).aggregate(Sum('amount'))['amount__sum'] or 0
        interest = float(self.amount) * (float(self.loan.interest_rate) / 100)
        total_due = float(self.amount) + interest
        return total_paid >= total_due


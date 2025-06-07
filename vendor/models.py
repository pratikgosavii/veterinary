from django.db import models

# Create your models here.


from django.db import models

# Create your models here.

from users.models import *
from masters.models import *
from pet.models import *



DOCUMENT_CHOICES = [
    ('adhar_card', 'Adhar Card'),
    ('driving_licence', 'Driving Licence'),
    ('passport', 'Passport'),
]


class vendor_kyc(models.Model):
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='vendor_kyc/')
    document_type = models.CharField(max_length=20, choices=DOCUMENT_CHOICES, default='open')
    document_image = models.ImageField(upload_to='vendor_kyc/')
    approved = models.BooleanField(default=False)

    


class vendor_wallet(models.Model):
    user = models.OneToOneField("users.User", on_delete=models.CASCADE, related_name='vendor_wallet')

    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    total_earned = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    total_withdrawn = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)

    is_active = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.mobile} - Wallet"



class vendor_wallet_transaction(models.Model):
    
    
    TRANSACTION_TYPE_CHOICES = [
        ('credit', 'Credit'),
        ('debit', 'Debit'),
    ]

    STATUS_CHOICES = [
        ('open', 'Open'),
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('completed', 'Completed'),
        ('cancelled_by_vendor', 'Cancelled by Vendor'),
        ('cancelled_by_admin', 'Cancelled by Admin'),
    ]

    wallet = models.ForeignKey('vendor_wallet', on_delete=models.CASCADE, related_name='transactions')
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPE_CHOICES)
    description = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='open')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.wallet.user.mobile} - {self.transaction_type} - {self.amount}"
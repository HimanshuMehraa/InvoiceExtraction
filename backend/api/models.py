from django.db import models
from django.contrib.auth.models import User


class Note(models.Model):
    title = models.CharField(max_length= 100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notes")

    def __str__(self):
        return self.title

class Invoice(models.Model):
    file = models.FileField(upload_to='invoices/')
    invoice_date = models.CharField(max_length=100,null=True, blank=True)
    invoice_number = models.CharField(max_length=100, null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    due_date = models.CharField(max_length=100, null=True, blank=True)
    extracted = models.BooleanField(default=False)

    def __str__(self):
        return f"Invoice {self.invoice_number or 'Unprocessed'}"


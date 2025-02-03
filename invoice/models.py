from django.db import models
from django.conf import settings
from decimal import Decimal
from num2words import num2words
import time


class Item(models.Model):
    """Model for individual items on the invoice."""
    description = models.CharField(max_length=255)
    unit_price = models.DecimalField(max_digits=16, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def total_cost(self):
        return self.unit_price * self.quantity

    def __str__(self):
        return self.description


class Invoice(models.Model):
    """Model for the invoice."""
    customer = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="invoices"
    )
    invoice_number = models.CharField(max_length=100, unique=True)
    date = models.DateField(auto_now_add=True)
    billed_to = models.JSONField()
    items = models.ManyToManyField("Item", through="InvoiceItem")
    subtotal = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    vat = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    ncdmb = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    grand_total = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    amount_in_words = models.TextField()
    payment_info = models.JSONField()

    def __str__(self):
        return f"Invoice #{self.invoice_number} - {self.customer.username}"

    @staticmethod
    def create_invoice(user, billed_to, payment_info):
        """
        Create an invoice for the given user using all items currently in the cart.
        """
        cart_items = InvoiceItem.objects.filter(status="CART", customer=user, invoice__isnull=True)

        if not cart_items.exists():
            raise ValueError("No items in the cart to create an invoice.")

        subtotal = sum(item.total_cost() for item in cart_items)
        vat = subtotal * Decimal("0.075")
        ncdmb = subtotal * Decimal("0.02")
        grand_total = subtotal + vat + ncdmb

        invoice = Invoice.objects.create(
            customer=user,
            invoice_number=f"INV-{user.id}-{int(time.time())}",
            subtotal=subtotal,
            vat=vat,
            ncdmb=ncdmb,
            grand_total=grand_total,
            amount_in_words = num2words(grand_total, to='currency', lang='en', currency='USD').replace("dollars", "Naira").replace("cents", "kobo"),
            billed_to=billed_to,
            payment_info=payment_info,
        )

        for item in cart_items:
            item.invoice = invoice
            item.status = "INVOICED"
            item.save()

        return invoice




class InvoiceItem(models.Model):
    """Intermediate model to link items with invoices."""
    STATUS_CHOICES = [
        ("CART", "Cart"),
        ("INVOICED", "Invoiced"),
    ]

    invoice = models.ForeignKey(
        Invoice, on_delete=models.CASCADE, related_name="invoice_items", null=True, blank=True
    )
    customer = models.ForeignKey(  # Add this field
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="cart_items"
    )
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="CART")

    def total_cost(self):
        return self.quantity * self.item.unit_price

    def __str__(self):
        return f"{self.item.description} x {self.quantity}"

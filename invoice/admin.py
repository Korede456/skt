from django.contrib import admin
from .models import Item, Invoice, InvoiceItem

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('description', 'unit_price', 'quantity')
    search_fields = ('description',)

@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('invoice_number', 'customer', 'date', 'subtotal', 'vat', 'ncdmb', 'grand_total')
    search_fields = ('invoice_number', 'customer__username')
    list_filter = ('date',)
    ordering = ('-date',)

@admin.register(InvoiceItem)
class InvoiceItemAdmin(admin.ModelAdmin):
    list_display = ('invoice', 'customer', 'item', 'quantity', 'status')
    search_fields = ('invoice__invoice_number', 'item__description', 'customer__username')
    list_filter = ('status', 'invoice', 'customer')

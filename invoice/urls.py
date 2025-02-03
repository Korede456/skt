from django.urls import path
from .views import (
    ItemCreateView,
    ItemListView,
    add_to_invoice_item,
    cart_view,
    create_invoice,
    invoice_detail,
    invoice_list,
    print_invoice,
)

app_name = 'invoice'

urlpatterns = [
    path('add_item/', ItemCreateView.as_view(), name='add_item'),
    path('dashboard/', ItemListView.as_view(), name='item_list'),
    path("add_to_cart/", add_to_invoice_item, name="add_to_invoice_item"),
    path('selected_items/', cart_view, name='cart'),
    path('create_invoice/', create_invoice, name='create_invoice'),
    path("invoice/<int:invoice_id>/", invoice_detail, name="invoice_detail"),
    path("invoices/", invoice_list, name='invoice_list' ),
    path("print_invoice/<int:invoice_id>/", print_invoice, name='print_invoice'),
]
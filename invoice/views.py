from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views import View
from .models import Item, Invoice, InvoiceItem
from .forms import ItemForm, InvoiceForm
from django.http import JsonResponse
from django.views.decorators.http import require_POST
import json
from django.contrib import messages
import os
from django.http import HttpResponse
from django.conf import settings
from .utils.invoice_utils import print_pdf  
from django.utils import timezone



class ItemCreateView(View):
    def get(self, request):
        form = ItemForm()
        return render(request, 'invoice/item_form.html', {'form': form})

    def post(self, request):
        form = ItemForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('invoice:item_list')  # Assuming you have a view named 'item_list'
        return render(request, 'invoice/item_form.html', {'form': form})


class ItemListView(View):
    def get(self, request):
        query = request.GET.get('q')
        items = Item.objects.all()
        cartItem = InvoiceItem.objects.filter(status="CART")
        quantity = sum(item.quantity for item in cartItem)
        if query:
            items = items.filter(description__icontains=query)
        return render(request, 'invoice/item_list.html', {'items': items, 'quantity': quantity})


@require_POST
def add_to_invoice_item(request):
    """
    Adds an item to the InvoiceItem model.
    If the item is already in the cart for the user, its quantity will be updated.
    """
    if not request.user.is_authenticated:
        return JsonResponse({"error": "You must be logged in to add items to the cart."}, status=401)

    try:
        data = json.loads(request.body)  # Parse JSON body
        item_id = data.get("item_id")
        quantity = int(data.get("quantity", 1))

        # Retrieve the item from the database
        item = get_object_or_404(Item, id=item_id)

        # Ensure the item is added to the cart for the logged-in user
        invoice_item, created = InvoiceItem.objects.get_or_create(
            item=item, 
            customer=request.user,  # Add this
            status="CART", 
            defaults={"quantity": quantity}
        )

        if not created:
            # Update the quantity if the item already exists in the cart
            invoice_item.quantity += quantity
            invoice_item.save()

        return JsonResponse({
            "message": "Item added to cart successfully.",
            "item_id": invoice_item.id,
            "quantity": invoice_item.quantity,
        })
    
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON data"}, status=400)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)



@login_required
def cart_view(request):
    """Display all items currently in the cart."""
    cart_items = InvoiceItem.objects.filter(status="CART", invoice__isnull=True)
    total_quantity = sum(item.quantity for item in cart_items)
    total_cost = sum(item.total_cost() for item in cart_items)
    
    context = {
        "cart_items": cart_items,
        "total_quantity": total_quantity,
        "total_cost": total_cost,
    }
    return render(request, "invoice/invoice_items.html", context)


#invoice creation view

@login_required
def create_invoice(request):
    if request.method == "POST":
        form = InvoiceForm(request.POST)
        if form.is_valid():
            try:
                invoice = Invoice.create_invoice(
                    user=request.user, 
                    billed_to=form.cleaned_data["billed_to"], 
                    payment_info=form.cleaned_data["payment_info"]
                )
                invoice.save()
                messages.success(request, f"Invoice {invoice.invoice_number} created successfully!")
                return redirect("invoice:invoice_detail", invoice_id=invoice.id)
            except ValueError as e:
                messages.error(request, str(e))
        else:
            print("Form is not valid")  # Debug
            print(form.errors)  # Debug
    else:
        form = InvoiceForm()

    return render(request, "invoice/invoice_form.html", {"form": form})

#invoice details view

@login_required
def invoice_detail(request, invoice_id):
    invoice = get_object_or_404(Invoice, id=invoice_id, customer=request.user)
    return render(request, "invoice/invoice_detail.html", {"invoice": invoice})

@login_required
def invoice_list(request):
    invoices = Invoice.objects.filter(customer=request.user)  # Get invoices for the logged-in user
    return render(request, "invoice/invoice_list.html", {"invoices": invoices})


def print_invoice(request, invoice_id):
    # Retrieve the invoice from the database
    invoice = get_object_or_404(Invoice, id=invoice_id)

    # Prepare the data for the PDF
    invoice_number = invoice.invoice_number
    date = invoice.date.strftime("%d %B, %Y")
    billed_to = [
        invoice.billed_to['line_1'],
        invoice.billed_to['line_2'],
        invoice.billed_to['line_3'],
    ]
    payment_info = [
        invoice.payment_info['detail_1'],
        invoice.payment_info['detail_2'],
        invoice.payment_info['detail_3'],
        invoice.payment_info['detail_4'],
        invoice.payment_info['detail_5'],
        invoice.payment_info['detail_6'],
    ]
    
    # Prepare items for the PDF
    items = [(item.item.description, item.total_cost()) for item in invoice.invoice_items.all()]

    # Calculate totals
    subtotal = invoice.subtotal
    vat = invoice.vat
    ncdmb = invoice.ncdmb
    grand_total = invoice.grand_total
    amount_in_words = invoice.amount_in_words

    # Create a filename based on the first line of billed_to and current date/time
    first_line_billed_to = billed_to[0].replace(" ", "_")  # Replace spaces with underscores for filename
    timestamp = timezone.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{first_line_billed_to}_{timestamp}.pdf"
    
    # Define the path to save the PDF
    pdf_path = os.path.join(settings.MEDIA_ROOT, 'invoices', filename)

    # Create the PDF
    print_pdf(
        invoice_number=invoice_number,
        date=date,
        billed_to=billed_to,
        payment_info=payment_info,
        items=items,
        subtotal=subtotal,
        vat=vat,
        ncdmb=ncdmb,
        grand_total=grand_total,
        amount_in_words=amount_in_words,
        filename=pdf_path,
    )

    # Return the generated PDF as a response
    with open(pdf_path, 'rb') as pdf:
        response = HttpResponse(pdf.read(), content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        return response
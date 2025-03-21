from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Shipment, ShipmentLineItem ,Factory
from inventory.models import Product
from .forms import ShipmentForm, ShipmentLineItemForm,ShipmentLineItemFormSet
from django.http import JsonResponse


@login_required
def shipment_list(request):
    shipments = Shipment.objects.all()
    return render(request, 'shipments/shipment_list.html', {'shipments': shipments})


@login_required
def shipment_detail(request, shipment_id):
    shipment = get_object_or_404(Shipment, id=shipment_id)
    return render(request, 'shipments/shipment_detail.html', {'shipment': shipment})


@login_required
def add_shipment(request):
    if request.method == "POST":
        shipment_form = ShipmentForm(request.POST)

        if shipment_form.is_valid():
            shipment = shipment_form.save(commit=False)
            shipment.created_by = request.user
            shipment.save()

            product_ids = request.POST.getlist("products[]")
            quantities = request.POST.getlist("quantities[]")

            for product_id, quantity in zip(product_ids, quantities):
                ShipmentLineItem.objects.create(
                    shipment=shipment,
                    product_id=int(product_id),
                    quantity=int(quantity)
                )

            messages.success(request, "Shipment created successfully!")
            return redirect("shipment_list")

    else:
        shipment_form = ShipmentForm()

    products = Product.objects.all()
    factories = Factory.objects.all()

    return render(request, "shipments/shipment_form.html", {
        "shipment_form": shipment_form,
        "products": products,
        "factories": factories,
    })


def remove_shipment_item(request, item_id):
    if request.method == "POST":
        item = get_object_or_404(ShipmentLineItem, id=item_id)
        item.delete()
        return JsonResponse({"success": True})
    return JsonResponse({"success": False}, status=400)

@login_required
def edit_shipment(request, shipment_id):
    shipment = get_object_or_404(Shipment, id=shipment_id)
    products = Product.objects.all()
    shipment_items = list(ShipmentLineItem.objects.filter(shipment=shipment))

    if request.method == "POST":
        form = ShipmentForm(request.POST, instance=shipment)
        if form.is_valid():
            form.save()

            product_ids = request.POST.getlist("products[]")
            quantities = request.POST.getlist("quantities[]")

            if product_ids:
                ShipmentLineItem.objects.filter(shipment=shipment).delete()
                for product_id, quantity in zip(product_ids, quantities):
                    product = Product.objects.get(id=product_id)
                    ShipmentLineItem.objects.create(
                        shipment=shipment,
                        product=product,
                        quantity=int(quantity),
                    )

            messages.success(request, "Shipment updated successfully!")
            return redirect("shipment_list")

    else:
        form = ShipmentForm(instance=shipment)

    return render(request, "shipments/edit_shipment.html", {
        "shipment": shipment,
        "shipment_form": form,
        "products": products,
        "shipment_items": shipment_items,
    })


@login_required
def confirm_shipment(request, shipment_id):
    shipment = get_object_or_404(Shipment, id=shipment_id)

    if not request.user.is_manager:
        messages.error(request, "Only managers can confirm shipments.")
        return redirect('shipment_list')

    if shipment.status != 'Shipped':
        shipment.status = 'Shipped'
        shipment.save()

        for item in shipment.line_items.all():
            item.product.quantity += item.quantity
            item.product.save()

        messages.success(request, "Shipment confirmed and inventory updated successfully!")
    else:
        messages.warning(request, "This shipment has already been confirmed before.")

    return redirect('shipment_list')


@login_required
def delete_shipment(request, shipment_id):
    shipment = get_object_or_404(Shipment, id=shipment_id)

    if not request.user.is_manager:
        return JsonResponse({"error": "Only managers can delete shipments."}, status=403)

    if request.method == "POST":
        shipment.delete()

        if request.headers.get("X-Requested-With") == "XMLHttpRequest":
            return JsonResponse({"success": True, "message": "Shipment deleted successfully!"})

        messages.success(request, "Shipment deleted successfully!")
        return redirect("shipment_list")

    return JsonResponse({"error": "Invalid request."}, status=400)


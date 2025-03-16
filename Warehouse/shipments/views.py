from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Shipment, ShipmentLineItem
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
            messages.success(request, "Shipment created successfully! Now add items.")
            return redirect('add_shipment_items', shipment_id=shipment.id)
    else:
        shipment_form = ShipmentForm()

    return render(request, 'shipments/shipment_form.html', {'shipment_form': shipment_form})

@login_required
def add_shipment_items(request, shipment_id):
    shipment = get_object_or_404(Shipment, id=shipment_id)

    if request.method == "POST":
        form = ShipmentLineItemForm(request.POST)
        if form.is_valid():
            shipment_item = form.save(commit=False)
            shipment_item.shipment = shipment
            shipment_item.save()
            messages.success(request, "Item added successfully!")
            return redirect('add_shipment_items', shipment_id=shipment.id)

    else:
        form = ShipmentLineItemForm()

    shipment_items = shipment.line_items.all()
    return render(request, 'shipments/add_shipment_items.html', {
        'shipment': shipment,
        'form': form,
        'shipment_items': shipment_items
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

    if not request.user.is_manager():
        messages.error(request, "Only managers can edit shipments.")
        return redirect('shipment_list')

    if request.method == "POST":
        shipment_form = ShipmentForm(request.POST, instance=shipment)

        if shipment_form.is_valid():
            shipment_form.save()
            messages.success(request, "Shipment updated successfully!")
            return redirect('add_shipment_items', shipment_id=shipment.id)
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        shipment_form = ShipmentForm(instance=shipment)

    return render(request, 'shipments/edit_shipment.html', {
        'shipment_form': shipment_form
    })


@login_required
def confirm_shipment(request, shipment_id):
    shipment = get_object_or_404(Shipment, id=shipment_id)
    if not request.user.is_manager():
        messages.error(request, "Only managers can confirm shipments.")
        return redirect('shipment_list')

    shipment.status = 'Shipped'
    shipment.save()
    messages.success(request, "Shipment confirmed and marked as 'Shipped'.")
    return redirect('shipment_detail', shipment_id=shipment.id)

@login_required
def delete_shipment(request, shipment_id):
    shipment = get_object_or_404(Shipment, id=shipment_id)

    if not request.user.is_manager():
        messages.error(request, "Only managers can delete shipments.")
        return redirect('shipment_list')

    if request.method == "POST":
        shipment.delete()
        messages.success(request, "Shipment deleted successfully!")
        return redirect('shipment_list')

    return render(request, 'shipments/confirm_delete.html', {'shipment': shipment})


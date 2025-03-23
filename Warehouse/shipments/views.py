from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.http import JsonResponse
from django.core.exceptions import ValidationError
from django.db import transaction
from .models import Shipment, ShipmentLineItem, Factory
from inventory.models import Product
from .forms import ShipmentForm, ShipmentLineItemForm, FactoryForm
from .transactions import mark_shipment_as_delivered


@login_required
def shipment_list(request):
    shipments = Shipment.objects.select_related('factory', 'created_by').all()
    factories = Factory.objects.all()

    return render(request, 'shipments/shipment_list.html', {
        'shipments': shipments,
        'factories': factories
    })

@login_required
def shipment_detail(request, shipment_id):
    shipment = get_object_or_404(
        Shipment.objects.select_related('factory', 'created_by').prefetch_related('line_items__product'),
        id=shipment_id
    )
    return render(request, 'shipments/shipment_detail.html', {'shipment': shipment})


@login_required
@permission_required('shipments.add_shipment', raise_exception=True)
def add_shipment(request):
    if request.method == "POST":
        shipment_form = ShipmentForm(request.POST)

        if shipment_form.is_valid():
            with transaction.atomic():
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
            messages.error(request, "Please correct the errors below.")
    else:
        shipment_form = ShipmentForm()

    products = Product.objects.all()
    factories = Factory.objects.all()

    return render(request, "shipments/shipment_form.html", {
        "shipment_form": shipment_form,
        "products": products,
        "factories": factories,
    })


@login_required
@permission_required('shipments.delete_shipmentlineitem', raise_exception=True)
def remove_shipment_item(request, item_id):
    if request.method == "POST":
        item = get_object_or_404(ShipmentLineItem, id=item_id)
        item.delete()
        return JsonResponse({"success": True})
    return JsonResponse({"success": False}, status=400)


@login_required
@permission_required('shipments.change_shipment', raise_exception=True)
def edit_shipment(request, shipment_id):
    shipment = get_object_or_404(Shipment, id=shipment_id)
    products = Product.objects.all()
    shipment_items = list(ShipmentLineItem.objects.filter(shipment=shipment))

    if request.method == "POST":
        form = ShipmentForm(request.POST, instance=shipment)
        if form.is_valid():
            with transaction.atomic():
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
@permission_required('shipments.confirm_shipment', raise_exception=True)
def confirm_shipment(request, shipment_id):
    shipment = get_object_or_404(Shipment, id=shipment_id)

    if shipment.status == 'Pending':
        shipment.status = 'Confirmed'
        shipment.save()
        messages.success(request, "Shipment confirmed successfully!")
    return redirect('shipment_list')


@login_required
@permission_required('shipments.deliver_shipment', raise_exception=True)
def delivered_shipment(request, shipment_id):
    shipment = get_object_or_404(Shipment, id=shipment_id)

    if shipment.status == 'Confirmed':
        try:
            mark_shipment_as_delivered(shipment)
            messages.success(request, "Shipment delivered successfully!")
            return redirect('shipment_list')
        except ValidationError as e:
            messages.error(request, str(e))
            return redirect('shipment_list')
    else:
        messages.error(request, "Shipment must be confirmed before it can be delivered.")
        return redirect('shipment_list')


@login_required
@permission_required('shipments.delete_shipment', raise_exception=True)
def cancel_shipment(request, shipment_id):
    shipment = get_object_or_404(Shipment, id=shipment_id)

    if request.method == "POST" and shipment.status == 'Pending':
        shipment.delete()

        if request.headers.get("X-Requested-With") == "XMLHttpRequest":
            return JsonResponse({"success": True, "message": "Shipment deleted successfully!"})

        messages.success(request, "Shipment deleted successfully!")
        return redirect("shipment_list")

    return JsonResponse({"error": "Invalid request."}, status=400)


@login_required
def factory_list(request):
    factories = Factory.objects.all()
    return render(request, 'factory/factory_list.html', {'factories': factories})


@login_required
def factory_detail(request, factory_id):
    factory = get_object_or_404(Factory, id=factory_id)
    return render(request, 'factory/factory_detail.html', {'factory': factory})


@login_required
@permission_required('shipments.add_factory', raise_exception=True)
def add_factory(request):
    if request.method == "POST":
        factory_form = FactoryForm(request.POST)
        if factory_form.is_valid():
            factory_form.save()
            messages.success(request, "Factory created successfully!")
            return redirect('factory_list')
    else:
        factory_form = FactoryForm()

    return render(request, 'factory/factory_form.html', {'form': factory_form})


@login_required
@permission_required('shipments.change_factory', raise_exception=True)
def edit_factory(request, factory_id):
    factory = get_object_or_404(Factory, id=factory_id)
    if request.method == "POST":
        factory_form = FactoryForm(request.POST, instance=factory)
        if factory_form.is_valid():
            factory_form.save()
            messages.success(request, "Factory updated successfully!")
            return redirect('factory_list')
    else:
        factory_form = FactoryForm(instance=factory)

    return render(request, 'factory/factory_form.html', {'form': factory_form})


@login_required
@permission_required('shipments.delete_factory', raise_exception=True)
def delete_factory(request, factory_id):
    factory = get_object_or_404(Factory, id=factory_id)
    if request.method == "POST":
        factory.delete()
        messages.success(request, "Factory deleted successfully!")
        return redirect('factory_list')
    return render(request, 'factory/factory_confirm_delete.html', {'factory': factory})
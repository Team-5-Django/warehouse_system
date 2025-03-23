from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Order, OrderLineItem, Supermarket
from .forms import OrderForm, OrderLineItemFormSet, SupermarketForm
from .filters import OrderFilter
from django.db.models import Q
from .models import Order
from .transactions import process_order
from django.urls import reverse_lazy

# List all orders
class OrderListView(ListView):
    model = Order
    template_name = 'orders/order_list.html'
    context_object_name = 'orders'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = OrderFilter(self.request.GET, queryset=queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = OrderFilter(self.request.GET, queryset=self.get_queryset())
        
        # Search functionality
        search_query = self.request.GET.get('search', '')
        if search_query:
            context['orders'] = self.get_queryset().filter(
                Q(supermarket__name__icontains=search_query) |
                Q(status__icontains=search_query)
            )
        return context

# View order details
class OrderDetailView(DetailView):
    model = Order
    template_name = 'orders/order_detail.html'

# Create a new order
class OrderCreateView(CreateView):
    model = Order
    form_class = OrderForm
    template_name = 'orders/order_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['formset'] = OrderLineItemFormSet(self.request.POST, instance=self.object)
        else:
            context['formset'] = OrderLineItemFormSet(instance=self.object)
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['formset']
        if formset.is_valid():
            self.object = form.save()
            formset.instance = self.object
            formset.save()
            return redirect('order_list')
        else:
            return self.render_to_response(self.get_context_data(form=form))
# Update an existing order
class OrderUpdateView(UpdateView):
    model = Order
    form_class = OrderForm
    template_name = 'orders/order_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['formset'] = OrderLineItemFormSet(self.request.POST, instance=self.object)
        else:
            context['formset'] = OrderLineItemFormSet(instance=self.object)
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['formset']
        if formset.is_valid():
            self.object = form.save()
            formset.instance = self.object
            formset.save()
            return redirect('order_list')
        else:
            # If the formset is invalid, re-render the form with errors
            return self.render_to_response(self.get_context_data(form=form))



def Confirm_order_view(request, pk):
    order = get_object_or_404(Order, id=pk)
    try:
        process_order(order)
        context = {
            'order': order,
            'message': 'Order processed successfully!',
        }
        return render(request, 'orders/order_confirmation.html', context)

    except Exception as e:
        context = {
            'order': order,
            'message': f'Error processing order: {str(e)}',
        }
        return render(request, 'orders/order_confirmation.html', context)
def shipping_order_view(request, pk):
    order = get_object_or_404(Order, id=pk)
    try:
        order.shipping()
        context = {
            'order': order,
            'message': 'Order shipped successfully!',
        }
        return render(request, 'orders/order_confirmation.html', context)
    except Exception as e:
        context = {
            'order': order,
            'message': f'Error shipping order: {str(e)}',
        }
        return render(request, 'orders/order_confirmation.html', context)

def delivery_order_view(request, pk):
    order = get_object_or_404(Order, id=pk)
    try:
        order.delivery()
        context = {
            'order': order,
            'message': 'Order delivered successfully!',
        }
        return render(request, 'orders/order_confirmation.html', context)
    except Exception as e:
        context = {
            'order': order,
            'message': f'Error delivering order: {str(e)}',
        }
        return render(request, 'orders/order_confirmation.html', context)

def cancel_order_view(request, pk):
    order = get_object_or_404(Order, id=pk)
    try:
        order.cancel()
        context = {
            'order': order,
            'message': 'Order cancelled successfully!',
        }
        return render(request, 'orders/order_confirmation.html', context)
    except Exception as e:
        context = {
            'order': order,
            'message': f'Error cancelling order: {str(e)}',
        }
        return render(request, 'orders/order_confirmation.html', context)
    

class SupermarketListView(ListView):
    model = Supermarket
    template_name = 'orders/supermarket_list.html'
    context_object_name = 'supermarkets'

class SupermarketCreateView(CreateView):
    model = Supermarket
    form_class = SupermarketForm
    template_name = 'orders/supermarket_form.html'
    success_url = reverse_lazy('supermarket_list')

class SupermarketUpdateView(UpdateView):
    model = Supermarket
    form_class = SupermarketForm
    template_name = 'orders/supermarket_form.html'
    success_url = reverse_lazy('supermarket_list')

class SupermarketDeleteView(DeleteView):
    model = Supermarket
    template_name = 'orders/supermarket_confirm_delete.html'
    success_url = reverse_lazy('supermarket_list')
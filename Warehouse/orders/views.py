from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from .models import Order, OrderLineItem
from .forms import OrderForm, OrderLineItemFormSet

# List all orders
class OrderListView(ListView):
    model = Order
    template_name = 'orders/order_list.html'
    context_object_name = 'orders'
    paginate_by = 10

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
            context['line_items'] = OrderLineItemFormSet(self.request.POST)
        else:
            context['line_items'] = OrderLineItemFormSet()
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        line_items = context['line_items']
        if line_items.is_valid():
            self.object = form.save()
            line_items.instance = self.object
            line_items.save()
            return redirect('order_list')
        return self.render_to_response(self.get_context_data(form=form))

# Update an existing order
class OrderUpdateView(UpdateView):
    model = Order
    form_class = OrderForm
    template_name = 'orders/order_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['line_items'] = OrderLineItemFormSet(self.request.POST, instance=self.object)
        else:
            context['line_items'] = OrderLineItemFormSet(instance=self.object)
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        line_items = context['line_items']
        if line_items.is_valid():
            self.object = form.save()
            line_items.instance = self.object
            line_items.save()
            return redirect('order_list')
        return self.render_to_response(self.get_context_data(form=form))
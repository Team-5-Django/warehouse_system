from django import forms
from django_filters import rest_framework as filters
from .models import Order, Supermarket
import django_filters

class OrderFilter(django_filters.FilterSet):
    supermarket = django_filters.ModelChoiceFilter(
        field_name='supermarket',
        queryset=Supermarket.objects.all(),
        label='Supermarket',
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    created_at = django_filters.DateFilter(field_name='created_at', lookup_expr='date')
    created_at__gte = django_filters.DateFilter(field_name='created_at', lookup_expr='date__gte')
    created_at__lte = django_filters.DateFilter(field_name='created_at', lookup_expr='date__lte')

    class Meta:
        model = Order
        fields = ['reference', 'status', 'supermarket']
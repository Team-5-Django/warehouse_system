from django.shortcuts import render

def get_dashboard_page(request):
    return render(request, 'dashboard.html')
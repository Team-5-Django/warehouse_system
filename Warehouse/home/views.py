from django.shortcuts import render

# Create your views here.
def get_home_page(request):
    return render(request, 'base.html')

def custom_404_view(request, exception):
    return render(request, 'home/404.html', status=404)


from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, 'quotes/index.html', {})

def about(request):
    return render(request, 'quotes/about.html', {})

def blog(request):
    return render(request, 'quotes/blog.html', {})
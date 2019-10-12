from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, 'quotes/index.html')

def about(request):
    return render(request, 'quotes/autors.html')

def blog(request):
    return render(request, 'quotes/topic.html')

def autor(request):
    return render(request, 'quotes/autor.html')

def simple_topic(request):
    return render(request, 'quotes/simple_topic.html')
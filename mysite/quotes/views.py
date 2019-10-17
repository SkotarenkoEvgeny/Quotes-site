from django.shortcuts import render
from django.views import generic

from .models import Author, Quote

import random


# Create your views here.


class AutorView(generic.DetailView):
    model = Author
    template_name = 'quotes/autor.html'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(AutorView, self).get_context_data(**kwargs)
        # Add in a QuerySet of all the quotes
        raw_context = Quote.objects.all()
        context['two_quotes'] = {random.choice(raw_context),
                                 random.choice(raw_context)}
        # print(random.choice(Quote.objects.all()))
        print(type(context))
        return context


# http://127.0.0.1:8000/quotes/autor/maya-angelou


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

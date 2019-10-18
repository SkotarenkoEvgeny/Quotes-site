from django.shortcuts import render
from django.views import generic

from .models import Author, Quote


# Create your views here.


class AutorView(generic.DetailView):
    """
    the view about curent autor
    """
    model = Author
    template_name = 'quotes/autor.html'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(AutorView, self).get_context_data(**kwargs)
        # Add in a QuerySet of all the quotes
        context['two_quotes'] = Quote.objects.order_by('?')[:2]
        return context


class MainPageView(generic.ListView):
    """
    the main page view
    """
    template_name = 'quotes/index.html'
    context_object_name = 'quotes_list'
    queryset = Quote.objects.order_by('?')[:4]

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(MainPageView, self).get_context_data(**kwargs)
        # Add in a QuerySet of all the quotes
        context['autors_list'] = Author.objects.order_by('?')[:4]
        return context


class TopicListView(generic.ListView):
    """
    the list of topics
    """
    template_name = 'quotes/topic.html'


def about(request):
    return render(request, 'quotes/autors.html')


def blog(request):
    return render(request, 'quotes/topic.html')


def simple_topic(request):
    return render(request, 'quotes/simple_topic.html')

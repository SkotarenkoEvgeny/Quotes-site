from django.shortcuts import render, get_object_or_404
from django.views import generic

from .models import Author, Quote, Topic


# Create your views here.


class AutorView(generic.DetailView):
    """
    the view about curent autor
    """
    model = Author
    template_name = 'quotes/autor.html'

    def get_context_data(self, **kwargs):
        context = super(AutorView, self).get_context_data(**kwargs)
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
        context = super(MainPageView, self).get_context_data(**kwargs)
        context['autors_list'] = Author.objects.order_by('?')[:4]
        return context


class TopicListView(generic.ListView):
    """
    the list of topics
    """
    template_name = 'quotes/topic.html'
    model = Topic
    context_object_name = 'topics_list'


class AutorListView(generic.ListView):
    """
    the list of autors
    """
    template_name = 'quotes/autors.html'
    model = Author
    context_object_name = 'autor_list'


class SimpleTopicList(generic.ListView):
    """
    the list of quotes from curent topic
    """
    template_name = 'quotes/simple_topic.html'
    model = Quote
    context_object_name = 'quote_list'

    def get_context_data(self, **kwargs):
        context = super(SimpleTopicList, self).get_context_data(**kwargs)
        context['topic_category'] = get_object_or_404(Topic, slug=self.kwargs['slug'])
        return context

    def get_queryset(self):
        self.topic = get_object_or_404(Topic, slug=self.kwargs['slug'])
        return Quote.objects.filter(topic=self.topic)

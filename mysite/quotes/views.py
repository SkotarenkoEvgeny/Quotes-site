from django.shortcuts import render, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.views import generic
from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

from .models import Author, Quote, Topic, MessagesToAdmin
from .forms import AdminContactForm

import datetime


# Create your views here.


class AutorView(generic.DetailView):
    """
    the view about curent autor
    """
    model = Author
    template_name = 'quotes/autor.html'

    def get_context_data(self, **kwargs):
        context = super(AutorView, self).get_context_data(**kwargs)
        author = self.request.GET.get('author')
        author_id = self.get_object()
        context['two_quotes'] = Quote.objects.filter(author=author_id)
        return context


class MainPageView(generic.ListView):
    """
    the main page view
    """
    template_name = 'quotes/index.html'
    context_object_name = 'topics_list'

    queryset = Topic.objects.order_by('?')[:24]

    def get_context_data(self, **kwargs):
        context = super(MainPageView, self).get_context_data(**kwargs)
        context['autors_list'] = Author.objects.order_by('?')[:24]

        # add the method searching a authors who born in today month
        today = str(datetime.date.today().month)
        context['born_autors_list'] = Author.objects.filter(
            born_date__month=today)
        return context


class TopicListView(generic.ListView):
    """
    the list of topics
    """
    template_name = 'quotes/topic.html'
    model = Topic
    context_object_name = 'topics_list'
    paginate_by = 48


class AutorListView(generic.ListView):
    """
    the list of autors
    """
    template_name = 'quotes/autors.html'
    model = Author
    context_object_name = 'autor_list'

    def get_queryset(self):
        order = self.request.GET.get('order_by', None)
        print(self.queryset)
        context = Author.objects.all()
        if order:
            context = context.order_by(order)
        return context


class SimpleTopicList(generic.ListView):
    """
    the list of quotes from curent topic
    """
    template_name = 'quotes/simple_topic.html'
    model = Quote
    context_object_name = 'quote_list'

    def get_context_data(self, **kwargs):
        context = super(SimpleTopicList, self).get_context_data(**kwargs)
        context['topic_category'] = get_object_or_404(Topic,
                                                      slug=self.kwargs['slug'])

        return context

    def get_queryset(self):
        self.topic = get_object_or_404(Topic, slug=self.kwargs['slug'])
        return Quote.objects.filter(topic=self.topic)


class AdminContactView(generic.CreateView):
    template_name = 'quotes/admin_contact_form.html'
    model = MessagesToAdmin
    form_class = AdminContactForm

    def get_success_url(self):
        return '%s?status_message=Form sended!' % reverse(
            'index')

    def post(self, request, *args, **kwargs):
        # the Admin-contact form logic
        if 'cancel' in request.POST:
            return HttpResponseRedirect(
                u'%s?status_message=Form chanceled!' % reverse('index'))
        elif 'reset' in request.POST:
            return HttpResponseRedirect(reverse('admin-contact'))
        else:
            return super(AdminContactView, self).post(request, *args, **kwargs)


class SearchIndexView(generic.ListView):
    template_name = 'quotes/index_search.html'
    model = Quote

    def get_context_data(self, **kwargs):
        query = self.request.GET.get('search', None)
        context = super(SearchIndexView, self).get_context_data(**kwargs)

        try:
            context['autors_list'] = Author.objects.filter(
            last_name=query.capitalize())
            print('autors_list', context['autors_list'])
        except ObjectDoesNotExist:
            pass

        try:
            topic_id = Topic.objects.get(topic=query.capitalize()).id
            context['topics_list'] = Quote.objects.filter(topic=topic_id)
            print('topics_list', context['topics_list'])
        except ObjectDoesNotExist:
            pass

        return context

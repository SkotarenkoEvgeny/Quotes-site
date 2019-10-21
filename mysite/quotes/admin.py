from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin

# Register your models here.

from quotes.models import Author, Topic, Quote, MessagesToAdmin


class AuthorAdmin(SummernoteModelAdmin):

    list_display = ['first_name', 'last_name', 'profesion', 'nationality']
    list_filter = ['profesion', 'nationality']
    search_fields = ['description']
    summernote_fields = ('description')


class QuoteAdmin(SummernoteModelAdmin):
    list_display = ['author', 'topic']
    list_filter = ['author', 'topic']
    search_fields = ['author', 'topic']
    summernote_fields = ('quote')


class MessagesToAdminAdmin(SummernoteModelAdmin):
    list_display = ['from_email', 'subject']
    list_filter = ['from_email', 'subject']
    search_fields = ['from_email', 'subject']
    summernote_fields = ('message')

admin.site.register(Author, AuthorAdmin)
admin.site.register(Topic)
admin.site.register(Quote, QuoteAdmin)
admin.site.register(MessagesToAdmin, MessagesToAdminAdmin)



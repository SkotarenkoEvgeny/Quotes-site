from django.contrib import admin

# Register your models here.

from quotes.models import Author, Topic, Quote, MessagesToAdmin

class AuthorAdmin(admin.ModelAdmin):

    list_display = ['first_name', 'last_name']

admin.site.register(Author, AuthorAdmin)
admin.site.register(Topic)
admin.site.register(Quote)
admin.site.register(MessagesToAdmin)



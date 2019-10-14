from django.core.management.base import BaseCommand
from requests_html import HTMLSession
from threading import Thread



def crawler(url):

    with HTMLSession() as session:
        response = session.get(url)

    list = response.html.find('#grid', first=True).find('li')

    for i in list:
        print(i.text, '#####', i.find('img', first=True).attrs['src'])


class Command(BaseCommand):
    help = 'find the topics and add to the base'


    def handle(self, *args, **options):
        url = 'https://www.quotetab.com/topics#P8D0DR8TCvugF7CF.97'
        Thread(target=crawler, args=(url,)).start()
        print('Done!')
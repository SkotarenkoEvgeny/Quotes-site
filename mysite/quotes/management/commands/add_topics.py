from django.core.management.base import BaseCommand
from requests_html import HTMLSession
from threading import Thread
import requests, os
from superslug import slugify

from quotes.models import Topic


def crawler(url):
    with HTMLSession() as session:
        response = session.get(url)

    list = response.html.find('#grid', first=True).find('li')

    for i in list:  #restriction 60

        image_url = i.find('img', first=True).attrs['src']
        image_name = i.find('img', first=True).attrs['src'].rsplit(sep='/')[-1]
        topic_name = i.text

        topic_obj = Topic(topic=topic_name, foto='/topics/' + image_name,
                          slug=slugify(topic_name))

        topic_obj.save()
        print(topic_obj.id)

        with HTMLSession() as session2:
            img_response = session2.get('http:' + image_url)

        with open(f'media/topics/{image_name}', 'wb') as imgf:
            imgf.write(img_response.content)

        print(topic_name, '#####', image_name)

        del img_response


class Command(BaseCommand):
    help = 'find the topics and add to the base'

    def handle(self, *args, **options):
        url = 'https://www.quotetab.com/topics#P8D0DR8TCvugF7CF.97'
        Thread(target=crawler, args=(url,)).start()
        print('Done!')

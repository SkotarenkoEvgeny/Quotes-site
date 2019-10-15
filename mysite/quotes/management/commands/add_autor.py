from django.core.management.base import BaseCommand
from requests_html import HTMLSession
from threading import Thread
import requests, os

from quotes.models import Author

def crawler(url):

    with HTMLSession() as session:
        response = session.get(url)

    list_links = response.html.find('.listing', first=True).absolute_links

    for autor_link in list(list_links)[:1]:
        # autor_link = 'https://www.quotetab.com/quotes/by-muhammad-ali#QUZKMIOD0h1T8D3X.97'
        print(autor_link)
        with HTMLSession() as session2:
            autor_resp = session2.get(autor_link)

    first_name = autor_resp.html.xpath('//*[@id="main"]/section[4]/div[1]/ul/li/div[1]/h2/text()')[0]
    print(autor_resp.html.xpath('//*[@id="main"]/section[4]/div[1]/ul/li/div[1]/h2/text()'))

    print(first_name)

    # last_name =
    #
    # born_date =
    #
    # dead_date =
    #
    # profesion =
    #
    # nationality =
    #
    # description =
    #
    # foto =
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # for i in list[:1]:# change for mass scraping
    #     image_url = i.find('img', first=True).attrs['src']
    #     image_name = i.find('img', first=True).attrs['src'].rsplit(sep='/')[-1]
    #     topic_name = i.text
    #     print(topic_name, '#####', image_name)
    #
    # topic_obj = Topic(topic=topic_name, foto='/autors/' + image_name)
    # topic_obj.save()
    # print(topic_obj.id)
    #
    # with HTMLSession() as session2:
    #     img_response = session2.get('http:' + image_url)
    #
    # with open(f'media/topics/{image_name}', 'wb') as imgf:
    #     imgf.write(img_response.content)



class Command(BaseCommand):
    help = 'find the autors and add to the base'


    def handle(self, *args, **options):
        url = 'https://www.quotetab.com/authors/a#xDqdYK3QQFVI65lp.97'
        Thread(target=crawler, args=(url,)).start()
        print('Done!')

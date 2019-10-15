from django.core.management.base import BaseCommand
from requests_html import HTMLSession
from threading import Thread
import requests, os

from quotes.models import Author


def crawler(url):
    with HTMLSession() as session:
        response = session.get(url)

    list_links = response.html.find('.listing', first=True).absolute_links

    for autor_link in list(list_links)[:30]:
        print(autor_link)

        with HTMLSession() as session2:
            autor_resp = session2.get(autor_link)

        try:
            full_name = autor_resp.html.xpath(
                '//*[@id="main"]/section[4]/div[1]/ul/li/div[1]/h2/text()')[
                0].split()
        except Exception as e:
            full_name = autor_resp.html.xpath(
                '//*[@id="main"]/section[3]/div[1]/ul/li/div[1]/h2/text()')[
                0].split()

        first_name = full_name[0]
        if len(full_name) > 1:
            last_name = full_name[1]
        else:
            last_name = ''

        try:
            born_date = autor_resp.html.xpath(
                '//*[@id="main"]/section[4]/div[2]/ul/li[1]/a/span[2]/span[@itemprop="birthDate"]/text()')[
                0]
        except Exception as e:
            born_date = 'not information'
            pass

        try:
            dead_date = autor_resp.html.xpath(
                '//*[@id="main"]/section[4]/div[1]/ul/li/div[2]/ul/li/div/span/span[@itemprop="deathDate"]/text()')[
                0]
        except Exception as e:
            dead_date = 'not information'
            pass

        try:
            profesion = autor_resp.html.xpath(
                '//*[@id="main"]/section[4]/div[2]/ul/li[3]/a/@title')[
                0].split()[2]
        except Exception as e:
            profesion = 'not information'
            pass

        try:
            nationality = autor_resp.html.xpath(
                '//*[@id="main"]/section[4]/div[2]/ul/li[2]/a/@title')[
                0].split()[2]
        except Exception as e:
            nationality = 'not information'
            pass

        try:
            description = autor_resp.html.xpath(
                '//*[@id="main"]/section[4]/div[1]/ul/li/div[2]/div/p/text()')[
                0]
        except Exception as e:
            description = 'not information'
            pass

        try:
            image_url = autor_resp.html.xpath(
                '//*[@id="main"]/section[4]/div[1]/ul/li/div[1]/img/@src')[0]
            foto = '/authors/' + image_url.rsplit(sep='/')[-1]
            with HTMLSession() as session2:
                img_response = session2.get('http:' + image_url)

            with open(f'media{foto}', 'wb') as imgf:
                imgf.write(img_response.content)
        except Exception as e:
            foto = ''
            pass

        author_dict = {'first_name': first_name,
                       'last_name': last_name,
                       'born_date': born_date,
                       'dead_date': dead_date,
                       'profesion': profesion,
                       'nationality': nationality,
                       'description': description,
                       'foto': foto}

        try:
            Author.objects.create(**author_dict)
            print("suceess")
        except Exception as e:
            print(type(e), e)
            return


class Command(BaseCommand):
    help = 'find the autors and add to the base'

    def handle(self, *args, **options):
        url = 'https://www.quotetab.com/authors/a#xDqdYK3QQFVI65lp.97'
        Thread(target=crawler, args=(url,)).start()
        print('Done!')

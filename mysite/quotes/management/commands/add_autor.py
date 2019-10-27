from django.core.management.base import BaseCommand
from requests_html import HTMLSession
from threading import Thread
import requests, os
import datetime
from superslug import slugify

from quotes.models import Author, Topic, Quote

topics = [i.topic for i in Topic.objects.all()]  # create list of topics


def date_converter(date):
    month_dict = {'January': 1, 'February': 2, 'March': 3, 'April': 4, 'May': 5,
                  'June': 6, 'July': 7, 'August': 8, 'September': 9,
                  'October': 10,
                  'November': 11, 'December': 12}
    raw_date = date.split()
    raw_date[0] = str(month_dict[raw_date[0]])
    raw_date[1] = raw_date[1][:-1]

    return '{}-{}-{}'.format(raw_date[2], raw_date[0], raw_date[1])


def crawler(url):
    with HTMLSession() as session:
        response = session.get(url)

    pagination = response.html.find('.pagination', first=True).absolute_links
    print('Pagination ', len(list(pagination)))

    for page in list(pagination):
        with HTMLSession() as session2:
            response = session.get(page)

        list_links = response.html.find('.listing', first=True).absolute_links
        print('list links', list(list_links))

        for autor_link in list(list_links):

            print(autor_link)

            with HTMLSession() as session3:
                autor_resp = session3.get(autor_link)

            try:
                full_name = autor_resp.html.xpath(
                    '//*[@id="main"]/section[4]/div[1]/ul/li/div[1]/h2/text()')[
                    0].split()
            except Exception as e:
                full_name = autor_resp.html.xpath(
                    '//*[@id="main"]/section[3]/div[1]/ul/li/div[1]/h2/text()')[
                    0].split()

            last_name = full_name[-1]
            if len(full_name) > 1:
                first_name = ' '.join(full_name[:-1])
            else:
                first_name = ''

            slug = slugify(first_name + ' ' + last_name)

            try:
                raw_born_date = autor_resp.html.xpath(
                    '//*[@id="main"]/section[4]/div[2]/ul/li[1]/a/span[2]/span[@itemprop="birthDate"]/text()')[
                    0]
                born_date = date_converter(raw_born_date)
            except Exception as e:
                born_date = None
                pass

            try:
                raw_dead_date = autor_resp.html.xpath(
                    '//*[@id="main"]/section[4]/div[1]/ul/li/div[2]/ul/li/div/span/span[@itemprop="deathDate"]/text()')[
                    0]
                raw_dead_date = raw_dead_date.split('/')
                dead_date = '{}-{}-{}'.format(raw_dead_date[2],
                                              raw_dead_date[0],
                                              raw_dead_date[1])
            except Exception as e:
                dead_date = None
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
                    '//*[@id="main"]/section[4]/div[1]/ul/li/div[1]/img/@src')[
                    0]
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
                           'slug': slug,
                           'foto': foto}

            try:
                author = Author.objects.create(**author_dict)
                print("suceess", author_dict['slug'])
            except Exception as e:
                print(type(e), e)
                continue

            # create the quotes from this author

            slug_number = 1

            topics_for_quotes = autor_resp.html.xpath(
                '//*[@id="grid"]/div/ul/li/div/div/div')
            for criterion in topics_for_quotes:
                rav_topic = criterion.text.split()
                slug_quote = slug + '-' + rav_topic[0] + '-' + slugify(
                    ' '.join(rav_topic[2:15]))
                if Quote.objects.filter(slug=slug_quote):
                    slug_quote += str(slug_number)
                    slug_number += 1
                if rav_topic[0] in topics:
                    quote = ' '.join(rav_topic[2:])
                    topic = Topic.objects.get(topic=rav_topic[0])
                    quote_dict = {'quote': quote,
                                  'slug': slug_quote,
                                  'author': author,
                                  'topic': topic}

                    try:
                        Quote.objects.create(**quote_dict)
                        print("suceess quote")
                    except Exception as e:
                        print(type(e), e)
                        return


class Command(BaseCommand):
    help = 'find the autors and add to the base'

    def handle(self, *args, **options):
        url = 'https://www.quotetab.com/authors/popular#uGf3h1Ak4OkgVovL.97'
        # url = 'https://www.quotetab.com/authors/a#xDqdYK3QQFVI65lp.97'
        Thread(target=crawler, args=(url,)).start()
        print('Done!')

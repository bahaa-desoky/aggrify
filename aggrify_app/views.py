from django.shortcuts import render
import requests
from . import all_sources


# Create your views here.
def main(request):
    titles = []
    authors = []
    dates = []
    descriptions = []
    links = []
    images = []

    if request.method == 'POST':
        sources = request.POST.getlist('sources')
        str_sources = ','.join(sources)
        pg_size = str(len(sources) * 20)

        if len(sources) == 0:
            pass

        else:
            url = 'http://newsapi.org/v2/everything?sources=' + str_sources + '&pageSize=' + pg_size + '&language=en&apiKey=23104fb4ccaa4f0da2d50e47d8930e12'
            page = requests.get(url)
            print(url)

            articles = page.json()['articles']

            for article in articles:
                del article['source']

            articles = [dict(t) for t in {tuple(dict_val.items()) for dict_val in articles}]

            for article in articles:
                title = article['title']
                titles.append(title)

                author = article['author']
                if author is not None:
                    if '[' in author:
                        author = 'N/A'
                    authors.append(author)

                date = article['publishedAt'].replace('-', '/').replace('2020/', '').replace('T', ' ')
                dates.append(date[:11])

                description = article['description'].replace('<li>', '').replace('<ul>', '').replace('<ol>',
                                                                                                     '').replace(
                    '</li>', '').replace('</ul>', '').replace('</ol>', '')
                descriptions.append(description)

                link = article['url']
                links.append(link)

                image = article['urlToImage']
                images.append(image)

    combined_items = zip(titles, authors, dates, descriptions, links, images, )
    combined_items = [list(a) for a in combined_items]

    sources_list = all_sources.all_sources

    context = {
        'main': combined_items,
        'sources_list': sources_list,
    }

    return render(request, 'aggrify_app/index.html', context)


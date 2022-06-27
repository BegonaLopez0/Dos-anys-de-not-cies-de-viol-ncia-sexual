from datetime import datetime
import numpy as np
import regex as re


def format_string(input_string):
    '''
    Remove spaces at the beginning and replace multiple withe spaces by one.
    '''
    string = re.sub(' +,', ' ', input_string).strip()
    return re.sub('\n', ' ', string).strip()


def obtain_information_20m(t_id, soup):
    '''
    Given the soup (html) of a new from the webpage of '20m' returns a list of
    fields to store the new's info in NewsML-G2 format (xml)
    '''
    news_author = format_string(soup.find_all("span", class_="article-author")[0].get_text())
    news_provider = format_string(soup.find_all("meta", {"name": "author"})[0]["content"])
    news_creation_datetime = format_string(soup.find_all("meta", {"property": "article:published_time"})[0]["content"])
    news_uri = soup.find_all("link", {'rel': 'canonical'})[0]['href']

    news_title = format_string(soup.find_all("meta", {"name": "title"})[0]["content"])
    news_headline = format_string(soup.find_all("meta", {"name": "description"})[0]["content"])

    news_guid = "urn:newsml:{}:{}:{}".format(news_provider, datetime.now().strftime("%Y%m%d"), t_id)

    text = soup.find_all("div", class_="article-text")
    paragraphs = []
    for i in np.arange(0, len(text)):
        for part in text[i].find_all("p"):
            paragraphs.append(part.get_text())

    news_article = format_string(" ".join(paragraphs))

    return news_author, news_provider, news_creation_datetime, news_uri, news_title, news_headline, news_guid, news_article


def obtain_information_A3Noticias(t_id, soup):
    '''
    Given the soup (html) of a new from the webpage of 'A3Noticias' returns a list of
    fields to store the new's info in NewsML-G2 format (xml)
    '''
    news_author = format_string(soup.find_all('div', class_='article-author__name')[0].get_text())
    news_provider = format_string(soup.find('meta', {'property': 'og:site_name'})['content'])
    news_creation_datetime = format_string(soup.find_all('meta', {'property': 'article:published_time'})['content'])
    news_uri = soup.find('link', {'rel': 'canonical'})['href']

    news_title = format_string(soup.find_all('h1', class_='article-main__title')[0].get_text())

    news_headline = format_string(soup.find_all('h2', class_='article-main__description')[0].get_text())
    if len(news_headline) == 0:
        news_headline = 'Not Specified'

    news_guid = "urn:newsml:{}:{}:{}".format(news_provider, datetime.now().strftime("%Y%m%d"), t_id)

    text = soup.find_all("div", class_="article-main")
    paragraphs = []
    for i in np.arange(0, len(text)):
        for part in text[i].find_all("p"):
            paragraphs.append(part.get_text())

    news_article = format_string(" ".join(paragraphs))

    return news_author, news_provider, news_creation_datetime, news_uri, news_title, news_headline, news_guid, news_article


def obtain_information_abc_es(t_id, soup):
    '''
    Given the soup (html) of a new from the webpage of 'abc_es' returns a list of
    fields to store the new's info in NewsML-G2 format (xml)
    '''
    try:
        news_author = format_string(soup.find('span', class_='autor').find('a', class_='nombre').get_text())
    except:
        news_author = 'Not Specified'
    news_provider = 'ABC.es'
    news_creation_datetime = soup.find('meta', {'property':'article:published_time'})['content']
    news_uri = soup.find("link", {'rel': 'canonical'})['href']

    news_title = format_string(soup.find('span', class_='titular').get_text())
    try:
        news_headline = format_string(soup.find('h2', class_='subtitulo').get_text())
    except:
        news_headline = 'Not Specified'
    news_guid = "urn:newsml:{}:{}:{}".format(news_provider, datetime.now().strftime("%Y%m%d"), t_id)

    text = soup.find_all('span', class_='cuerpo-texto')
    paragraphs = []
    for i in np.arange(0, len(text)):
        for part in text[i].find_all("p"):
            paragraphs.append(part.get_text())

    news_article = format_string(" ".join(paragraphs))

    return news_author, news_provider, news_creation_datetime, news_uri, news_title, news_headline, news_guid, news_article


def obtain_information_cope(t_id, soup):
    '''
    Given the soup (html) of a new from the webpage of 'cope' returns a list of
    fields to store the new's info in NewsML-G2 format (xml)
    '''

    news_author = soup.find('meta', {'name': 'author'})['content']
    news_provider = "Cope"
    news_creation_datetime = soup.find('meta', {'property':'article:published_time'})['content']
    news_uri = soup.find("link", {'rel': 'canonical'})['href']
    news_title = soup.find('h1', class_='title').get_text()
    news_headline = soup.find('div', class_='subtitle').get_text()
    news_guid = "urn:newsml:{}:{}:{}".format(news_provider, datetime.now().strftime("%Y%m%d"), t_id)

    text = soup.find_all('div', class_='detail-body')
    paragraphs = []
    for i in np.arange(0, len(text)):
        for part in text[i].find_all("p"):
            paragraphs.append(part.get_text())

    news_article = format_string(" ".join(paragraphs))

    return news_author, news_provider, news_creation_datetime, news_uri, news_title, news_headline, news_guid, news_article


def obtain_information_EFEnoticias(t_id, soup):
    '''
    Given the soup (html) of a new from the webpage of 'EFE_noticias_ES' returns a list of
    fields to store the new's info in NewsML-G2 format (xml)
    '''

    news_author = soup.find('meta', {'property': 'article:author'})['content']
    news_provider = soup.find('meta', {'name': 'organization'})['content']
    news_creation_datetime = soup.find('meta', {'itemprop': 'datePublished'})['content']
    news_uri = soup.find("link", {'rel': 'canonical'})['href']
    news_title = soup.find('h1', class_='titulo').get_text()
    news_headline = 'Not specified'
    news_guid = "urn:newsml:{}:{}:{}".format(news_provider, datetime.now().strftime("%Y%m%d"), t_id)

    text = soup.find_all('div', class_='texto dont-break-out')
    paragraphs = []
    for i in np.arange(0, len(text)):
        for part in text[i].find_all("p"):
            paragraphs.append(part.get_text())

    news_article = format_string(" ".join(paragraphs))

    return news_author, news_provider, news_creation_datetime, news_uri, news_title, news_headline, news_guid, news_article


def obtain_information_elconfidencial(t_id, soup):
    '''
    Given the soup (html) of a new from the webpage of 'elconfidencial' returns a list of
    fields to store the new's info in NewsML-G2 format (xml)
    '''
    news_uri = soup.find("link", {'rel': 'canonical'})['href']
    try:
        news_author = soup.find('a', class_='news-def-author').get_text()
        news_provider = "Blogs, El Confidencial"
        news_creation_datetime = soup.find('time', class_='news-def-date')['datetime']

        news_title = soup.find('h1', class_='news-header-tit').get_text()
        news_headline = soup.find('h2', class_='news-header-opening-txt').get_text()

        news_guid = "urn:newsml:{}:{}:{}".format(news_provider, datetime.now().strftime("%Y%m%d"), t_id)

        text = soup.find_all('div', class_='news-body-center cms-format')
        paragraphs = []
        for i in np.arange(0, len(text)):
            for part in text[i].find_all("p"):
                paragraphs.append(part.get_text())

        news_article = format_string(" ".join(paragraphs))

    except:
        news_author = format_string(soup.find_all("div", class_="authorSignature")[0].get_text().replace('Por', ''))
        news_provider = "Vanitatis, El Confidencial"
        news_creation_datetime = format_string(soup.find_all("div", class_="dateTime")[0].find('time')['datetime'])

        news_title = format_string(soup.find_all("title")[0].get_text())
        news_headline = format_string(soup.find_all("meta", {'name': 'description'})[0]['content'])

        news_guid = "urn:newsml:{}:{}:{}".format(news_provider, datetime.now().strftime("%Y%m%d"), t_id)

        text = soup.find_all("div", class_="newsType__content")
        paragraphs = []
        for i in np.arange(0, len(text)):
            for part in text[i].find_all("p"):
                paragraphs.append(part.get_text())

        news_article = format_string(" ".join(paragraphs))

    return news_author, news_provider, news_creation_datetime, news_uri, news_title, news_headline, news_guid, news_article


def obtain_information_eldiarioes(t_id, soup):
    '''
    Given the soup (html) of a new from the webpage of 'eldiarioes' returns a list of
    fields to store the new's info in NewsML-G2 format (xml)
    '''

    news_author = soup.find('meta', {'name': 'author'})['content']
    news_provider = soup.find('meta', {'name': 'publisher'})['content']
    news_creation_datetime = soup.find('time', class_='date')['datetime']
    news_uri = soup.find("link", {'rel': 'canonical'})['href']

    news_title = soup.find('title').get_text()
    headline = soup.find_all('h2')

    headline_paragraphs = []
    for i in np.arange(0, len(headline)):
        for part in headline[i]:
            headline_paragraphs.append(part.get_text())

    news_headline = format_string(" ".join(headline_paragraphs))
    if len(news_headline) == 0:
        news_headline = 'Not Specified'

    news_guid = "urn:newsml:{}:{}:{}".format(news_provider, datetime.now().strftime("%Y%m%d"), t_id)

    text = soup.find_all('p', class_='article-text')
    paragraphs = []
    for i in np.arange(0, len(text)):
        for part in text[i]:
            paragraphs.append(part.get_text())

    news_article = format_string(" ".join(paragraphs))

    return news_author, news_provider, news_creation_datetime, news_uri, news_title, news_headline, news_guid, news_article


def obtain_information_elespanolcom(t_id, soup):
    '''
    Given the soup (html) of a new from the webpage of 'elespanolcom' returns a list of
    fields to store the new's info in NewsML-G2 format (xml)
    '''

    news_author = soup.find('meta', property='nrbi:authors')['content']
    news_provider = "El Español"
    news_creation_datetime = soup.find('meta', property='article:published_time')['content']
    news_uri = soup.find("link", {'rel': 'canonical'})['href']
    news_title = soup.find('h1', class_='article-header__heading article-header__heading--s3').get_text()
    news_headline = soup.find('h2', class_='article-header__subheading').get_text()
    news_guid = "urn:newsml:{}:{}:{}".format(news_provider, datetime.now().strftime("%Y%m%d"), t_id)

    text = soup.find_all('div', class_='article-body__content')
    paragraphs = []
    for i in np.arange(0, len(text)):
        for part in text[i].find_all("p"):
            paragraphs.append(part.get_text())

    news_article = format_string(" ".join(paragraphs))

    return news_author, news_provider, news_creation_datetime, news_uri, news_title, news_headline, news_guid, news_article


def obtain_information_ElHuffPost(t_id, soup):
    '''
    Given the soup (html) of a new from the webpage of 'ElHuffPost' returns a list of
    fields to store the new's info in NewsML-G2 format (xml)
    '''
    try:
        news_author = soup.find('span', {'class': 'entry-wirepartner__byline'}).get_text()
    except:
        news_author = soup.find('a', {'data-vars-subunit-name': 'author'}).get_text()

    news_provider = "El HuffPost"
    news_creation_datetime = soup.find('meta', property='article:published_time')['content']
    news_uri = soup.find("link", {'rel': 'canonical'})['href']
    news_title = soup.find('meta', {'property': 'og:title'})['content']
    news_headline = soup.find('meta', {'name': 'description'})['content']
    if len(news_headline)==0:
        news_headline = 'Not Specified'
    news_guid = "urn:newsml:{}:{}:{}".format(news_provider, datetime.now().strftime("%Y%m%d"), t_id)

    text = soup.find_all('div', class_='primary-cli cli cli-text')
    paragraphs = []
    for i in np.arange(0, len(text)):
        for part in text[i].find_all("p"):
                paragraphs.append(part.get_text())

    news_article = format_string(" ".join(paragraphs))

    return news_author, news_provider, news_creation_datetime, news_uri, news_title, news_headline, news_guid, news_article


def obtain_information_elmundoes(t_id, soup):
    '''
    Given the soup (html) of a new from the webpage of 'El mundo' returns a list of
    fields to store the new's info in NewsML-G2 format (xml)
    '''

    news_author = soup.find('div', class_='ue-c-article__byline-name').get_text()
    news_provider = 'El Mundo'
    news_creation_datetime = soup.find('meta', {'name': 'date'})['content']
    news_uri = soup.find('link', {'rel': 'canonical'})['href']

    news_title = soup.find('h1').get_text()
    try:
        news_headline = soup.find('p', class_='ue-c-article__standfirst').get_text()
    except:
        news_headline = 'Not Specified'

    news_guid = "urn:newsml:{}:{}:{}".format(news_provider, datetime.now().strftime("%Y%m%d"), t_id)

    text = soup.find_all('div', {'data-section': 'articleBody'})
    paragraphs = []
    for i in np.arange(0, len(text)):
        for part in text[i].find_all("p"):
            paragraphs.append(part.get_text())

    news_article = format_string(" ".join(paragraphs))

    return news_author, news_provider, news_creation_datetime, news_uri, news_title, news_headline, news_guid, news_article


def obtain_information_el_pais(t_id, soup):
    '''
    Given the soup (html) of a new from the webpage of 'el_pais' returns a list of
    fields to store the new's info in NewsML-G2 format (xml)
    '''

    news_author = soup.find('meta', {'name': 'author'})['content']
    try:
        news_provider = soup.find('meta', {'name': 'organization'})['content']
    except:
        news_provider = 'Ediciones El País'

    news_creation_datetime = soup.find('meta', {'name': 'date'})['content']
    news_uri = soup.find('link', {'rel': 'canonical'})['href']

    try:
        news_title = soup.find('h1', class_='a_t').get_text()
    except:
        news_title = soup.find('meta', {'property': 'og:title'})['content']

    news_headline = soup.find('h2', class_='a_st').get_text()
    if len(news_headline) == 0:
        news_headline = soup.find('meta', {'property': 'og:description'})['content']

    news_guid = "urn:newsml:{}:{}:{}".format(news_provider, datetime.now().strftime("%Y%m%d"), t_id)

    text = soup.find_all('div', class_='a_c clearfix')
    if len(text)==0:
        text = soup.find_all('div', {'itemprop': 'articleBody'})

    paragraphs = []
    for i in np.arange(0, len(text)):
        for part in text[i].find_all("p"):
            paragraphs.append(part.get_text())

    news_article = format_string(" ".join(paragraphs))

    return news_author, news_provider, news_creation_datetime, news_uri, news_title, news_headline, news_guid, news_article


def obtain_information_elperiodico(t_id, soup):
    '''
    Given the soup (html) of a new from the webpage of 'el periodico' returns a list of
    fields to store the new's info in NewsML-G2 format (xml)
    '''

    news_author = soup.find('meta', {'name': 'author'})['content']
    news_provider = 'El periodico'
    news_creation_datetime = soup.find('meta', {'property': 'article:published_time'}).get('content')
    news_uri = soup.find('link', {'rel': 'canonical'})['href']

    news_title = soup.find('h1', class_='title').get_text()

    try:
        news_headline = soup.find('h2', class_='subtitle').get_text()
    except:
        news_headline = 'Not Specified'

    news_guid = "urn:newsml:{}:{}:{}".format(news_provider, datetime.now().strftime("%Y%m%d"), t_id)

    text = soup.find_all('div', class_='ep-detail-body')
    paragraphs = []
    for i in np.arange(0, len(text)):
        for part in text[i].find_all("p"):
            paragraphs.append(part.get_text())

    news_article = format_string(" ".join(paragraphs))

    return news_author, news_provider, news_creation_datetime, news_uri, news_title, news_headline, news_guid, news_article


def obtain_information_europapress(t_id, soup):
    '''
    Given the soup (html) of a new from the webpage of 'europapress' returns a list of
    fields to store the new's info in NewsML-G2 format (xml)
    '''

    news_author = soup.find('meta', {'itemprop': 'name'})['content']
    news_provider = 'Europa Press'
    news_creation_datetime = soup.find('meta', {'name': 'date'})['content']
    news_uri = soup.find('link', {'rel': 'canonical'})['href']

    news_title = soup.find('h1', class_='titular').get_text()
    news_headline = 'Not specified'

    news_guid = "urn:newsml:{}:{}:{}".format(news_provider, datetime.now().strftime("%Y%m%d"), t_id)

    text = soup.find_all('div', class_='NormalTextoNoticia')
    paragraphs = []
    for i in np.arange(0, len(text)):
        for part in text[i].find_all("p"):
            paragraphs.append(part.get_text())

    news_article = format_string(" ".join(paragraphs))

    return news_author, news_provider, news_creation_datetime, news_uri, news_title, news_headline, news_guid, news_article


def obtain_information_informativost5(t_id, soup):
    # Given the soup (html) of a new from the webpage of 'el periodico' returns a list of
    # fields to store the new's info in NewsML-G2 format (xml)

    news_author = 'Not specified'

    try:
        news_author = soup.find('span', class_ = 'authorComponent__gray-7_zA autor-nombre').get_text()
    except:
        try:
            news_author = soup.find('span', class_='authorComponent__gray-7_zA autor-signature').get_text()
        except:
            pass

    news_provider = 'Informativos T5'
    news_creation_datetime = soup.find('time').get('datetime')
    news_uri = soup.find('link', {'rel': 'canonical'}).get('href')

    news_title = soup.find('h1').get_text()
    news_headline = " ".join([element.get_text() for element in soup.find_all('h2')])

    news_guid = "urn:newsml:{}:{}:{}".format(news_provider, datetime.now().strftime("%Y%m%d"), t_id)


    text = soup.find_all('div')
    paragraphs = []
    for i in np.arange(0, len(text)):
        for part in text[i].find_all("p", class_='color_eta'):
            paragraphs.append(part.get_text())

    news_article = format_string(" ".join(paragraphs))

    return news_author, news_provider, news_creation_datetime, news_uri, news_title, news_headline, news_guid, news_article


def obtain_information_larazon_es(t_id, soup):
    # Given the soup (html) of a new from the webpage of 'La razon' returns a list of
    # fields to store the new's info in NewsML-G2 format (xml)

    try:
        news_author = soup.find('meta', {'property': 'nrbi:authors'})['content']
    except:
        news_author = soup.find

    news_provider = 'La Razón'
    news_creation_datetime = soup.find('meta', {'property':'article:published_time'})['content']
    news_uri = soup.find('link', {'rel': 'canonical'})['href']

    news_title = soup.find('h1').get_text()
    news_headline = soup.find('h2').get_text()
    if len(news_headline)==0:
        news_headline = 'Not Specified'

    news_guid = "urn:newsml:{}:{}:{}".format(news_provider, datetime.now().strftime("%Y%m%d"), t_id)

    text = soup.find_all('section')
    paragraphs = []
    for i in np.arange(0, len(text)):
        for part in text[i].find_all("p"):
            paragraphs.append(part.get_text())

    news_article = format_string(" ".join(paragraphs))

    return news_author, news_provider, news_creation_datetime, news_uri, news_title, news_headline, news_guid, news_article


def obtain_information_La_SER(t_id, soup):
    # Given the soup (html) of a new from the webpage of 'Cadena SER' returns a list of
    # fields to store the new's info in NewsML-G2 format (xml)

    news_author = soup.find('meta', {'name': 'author'})['content']
    news_provider = 'Cadena SER'
    news_creation_datetime = soup.find('meta', {'property': 'article:published_time'})['content']
    news_uri = soup.find('link', {'rel': 'canonical'})['href']

    news_title = soup.find('h1').get_text()
    news_headline = soup.find('h2').get_text()

    news_guid = "urn:newsml:{}:{}:{}".format(news_provider, datetime.now().strftime("%Y%m%d"), t_id)

    text = soup.find_all('div', class_='cnt-txt')
    paragraphs = []
    for i in np.arange(0, len(text)):
        for part in text[i].find_all("p"):
            paragraphs.append(part.get_text())

    news_article = format_string(" ".join(paragraphs))

    return news_author, news_provider, news_creation_datetime, news_uri, news_title, news_headline, news_guid, news_article


def obtain_information_laSextaTV(t_id, soup):
    # Given the soup (html) of a new from the webpage of 'La Sexta TV' returns a list of
    # fields to store the new's info in NewsML-G2 format (xml)

    news_author = soup.find('a', class_='article-author__is').get_text()
    news_provider = soup.find('meta', {'name': 'organization'})['content']
    news_creation_datetime = soup.find('meta', {'property': 'article:published_time'})['content']
    news_uri = soup.find('link', {'rel': 'canonical'})['href']

    news_title = soup.find('meta', {'name': 'title'})['content']
    news_headline = soup.find('meta', {'name': 'description'})['content']

    news_guid = "urn:newsml:{}:{}:{}".format(news_provider, datetime.now().strftime("%Y%m%d"), t_id)

    text = soup.find_all('div', class_='articleBody')
    paragraphs = []
    for i in np.arange(0, len(text)):
        for part in text[i].find_all("p"):
            paragraphs.append(part.get_text())

    news_article = format_string(" ".join(paragraphs))
    return news_author, news_provider, news_creation_datetime, news_uri, news_title, news_headline, news_guid, news_article


def obtain_information_laVanguardia(t_id, soup):
    # Given the soup (html) of a new from the webpage of 'La Vanguardia' returns a list of
    # fields to store the new's info in NewsML-G2 format (xml)

    news_author = soup.find('div', class_='author-name').get_text()
    news_provider = 'La vanguardia'
    news_creation_datetime = soup.find('time').get('datetime')
    news_uri = soup.find('link', {'rel': 'canonical'})['href']

    news_title = soup.find('h1', class_='title').get_text()
    news_headline = ". ".join([elem.get_text() for elem in soup.find_all('h2', class_='epigraph')])

    news_guid = "urn:newsml:{}:{}:{}".format(news_provider, datetime.now().strftime("%Y%m%d"), t_id)

    text = soup.find_all('div', class_='article-modules')
    paragraphs = []
    for i in np.arange(0, len(text)):
        for part in text[i].find_all("p"):
            paragraphs.append(part.get_text())

    news_article = format_string(" ".join(paragraphs))
    return news_author, news_provider, news_creation_datetime, news_uri, news_title, news_headline, news_guid, news_article


def obtain_information_libertaddigital(t_id, soup):
    # Given the soup (html) of a new from the webpage of 'Libertad Digital' returns a list of
    # fields to store the new's info in NewsML-G2 format (xml)

    news_author = soup.find('meta', {'name':'author'})['content']
    news_provider = 'Libertad Digital'
    news_creation_datetime = soup.find('meta', {'property': 'article:published_time'})['content']
    news_uri = soup.find('link', {'rel': 'canonical'})['href']

    news_title = soup.find('meta', {'property': 'og:title'})['content']
    news_headline = soup.find('meta', {'name': 'description'})['content']

    news_guid = "urn:newsml:{}:{}:{}".format(news_provider, datetime.now().strftime("%Y%m%d"), t_id)

    text = soup.find_all('div')
    paragraphs = []
    for i in np.arange(0, len(text)):
        for part in text[i].find_all("p"):
            paragraphs.append(part.get_text())
    news_article = format_string(" ".join(paragraphs))

    return news_author, news_provider, news_creation_datetime, news_uri, news_title, news_headline, news_guid, news_article


def obtain_information_noticias_cuatro(t_id, soup):
    # Given the soup (html) of a new from the webpage of 'Noticias Cuatro' returns a list of
    # fields to store the new's info in NewsML-G2 format (xml)

    news_author = soup.find('span', class_='authorComponent__gray-7_zA autor-signature').get_text()
    news_provider = 'Noticias Cuatro'
    news_creation_datetime = soup.find('meta', {'property': 'article:published_time'})['content']
    news_uri = soup.find('link', {'rel': 'canonical'})['href']

    news_title = soup.find('meta', {'property': 'og:title'})['content']
    news_headline = soup.find('meta', {'name': 'description'})['content']

    news_guid = "urn:newsml:{}:{}:{}".format(news_provider, datetime.now().strftime("%Y%m%d"), t_id)

    text = soup.find_all('div')
    paragraphs = []
    for i in np.arange(0, len(text)):
        for part in text[i].find_all("p"):
            paragraphs.append(part.get_text())
    news_article = format_string(" ".join(paragraphs))

    return news_author, news_provider, news_creation_datetime, news_uri, news_title, news_headline, news_guid, news_article


def obtain_information_okdiario(t_id, soup):
    # Given the soup (html) of a new from the webpage of 'okdiario' returns a list of
    # fields to store the new's info in NewsML-G2 format (xml)

    news_author = soup.find('li', class_='author-name').get_text()
    news_provider = 'OKDIARIO'
    news_creation_datetime = soup.find('meta', {'property': 'article:published_time'})['content']

    news_uri = soup.find('link', {'rel': 'canonical'})['href']

    news_title = soup.find('h1', class_='entry-title').get_text()

    try:
        news_headline = soup.find('h2').get_text()
    except:
        news_headline = 'Not Specified'

    news_guid = "urn:newsml:{}:{}:{}".format(news_provider, datetime.now().strftime("%Y%m%d"), t_id)

    text = soup.find_all('div', class_='entry-content')
    paragraphs = []
    for i in np.arange(0, len(text)):
        for part in text[i].find_all("p"):
            paragraphs.append(part.get_text())

    news_article = format_string(" ".join(paragraphs))
    return news_author, news_provider, news_creation_datetime, news_uri, news_title, news_headline, news_guid, news_article


def obtain_information_OndaCero_es(t_id, soup):
    # Given the soup (html) of a new from the webpage of 'Onda Cero' returns a list of
    # fields to store the new's info in NewsML-G2 format (xml)

    news_author = format_string(soup.find('p', class_ = 'articleSignature-name').get_text())
    news_provider = format_string(soup.find('meta', {'name': 'organization'})['content'])
    news_creation_datetime = soup.find('meta', {'property': 'article:published_time'})['content']

    news_uri = soup.find('link', {'rel': 'canonical'})['href']

    news_title = soup.find('title').get_text()
    news_headline = soup.find('meta', {'name':'description'})['content']


    news_guid = "urn:newsml:{}:{}:{}".format(news_provider, datetime.now().strftime("%Y%m%d"), t_id)

    text = soup.find_all('div', class_='articleContent')
    paragraphs = []
    for i in np.arange(0, len(text)):
        for part in text[i].find_all("p"):
            paragraphs.append(part.get_text())

    news_article = format_string(" ".join(paragraphs))
    return news_author, news_provider, news_creation_datetime, news_uri, news_title, news_headline, news_guid, news_article


def obtain_information_publico_es(t_id, soup):
    # Given the soup (html) of a new from the webpage of 'publico.es' returns a list of
    # fields to store the new's info in NewsML-G2 format (xml)


    news_author = format_string(soup.find('p', class_='signature').get_text())
    news_provider = 'Público'

    news_creation_datetime = soup.find('time')['datetime']

    news_uri = soup.find('link', {'rel': 'canonical'})['href']

    news_title = soup.find('meta', {'property': 'og:title'})['content']
    news_headline = soup.find('meta', {'name': 'description'})['content']


    news_guid = "urn:newsml:{}:{}:{}".format(news_provider, datetime.now().strftime("%Y%m%d"), t_id)

    text = soup.find_all('div', class_='article-text')
    paragraphs = []
    for i in np.arange(0, len(text)):
        for part in text[i].find_all("p"):
            paragraphs.append(part.get_text())

    news_article = format_string(" ".join(paragraphs))
    return news_author, news_provider, news_creation_datetime, news_uri, news_title, news_headline, news_guid, news_article

def obtain_information_rtve(t_id, soup):
    # Given the soup (html) of a new from the webpage of 'rtve' returns a list of
    # fields to store the new's info in NewsML-G2 format (xml)

    news_author = format_string(soup.find('span', {'itemprop': 'author'}).get_text())
    news_provider = 'rtve'
    news_creation_datetime = soup.find('time')['datetime']
    news_uri = soup.find('link', {'rel': 'canonical'})['href']

    news_title = soup.find('span', class_='maintitle').get_text()
    news_headline = format_string(". ".join([elem.get_text() for elem in soup.find_all('div', class_='summary')]))

    news_guid = "urn:newsml:{}:{}:{}".format(news_provider, datetime.now().strftime("%Y%m%d"), t_id)

    text = soup.find_all('div', class_='artBody')
    paragraphs = []
    for i in np.arange(0, len(text)):
        for part in text[i].find_all("p"):
            paragraphs.append(part.get_text())

    news_article = format_string(" ".join(paragraphs))
    return news_author, news_provider, news_creation_datetime, news_uri, news_title, news_headline, news_guid, news_article


def obtain_information_voz_populi(t_id, soup):
    # Given the soup (html) of a new from the webpage of 'Voz Populi' returns a list of
    # fields to store the new's info in NewsML-G2 format (xml)
    try:
        news_author = soup.find('a', class_= 'author-link').get_text()
    except:
        news_author = 'Not Specified'

    news_provider = 'Voz Populi'
    news_creation_datetime = soup.find('time', class_='date')['datetime']
    news_uri = soup.find('link', {'rel': 'canonical'})['href']

    news_title = soup.find('meta', {'property': 'og:title'})['content']
    news_headline = soup.find('meta', {'name': 'description'})['content']

    news_guid = "urn:newsml:{}:{}:{}".format(news_provider, datetime.now().strftime("%Y%m%d"), t_id)

    text = soup.find_all('div', {'id': 'post-text'})
    paragraphs = []
    for i in np.arange(0, len(text)):
        for part in text[i].find_all("p"):
            paragraphs.append(part.get_text())

    news_article = format_string(" ".join(paragraphs))
    return news_author, news_provider, news_creation_datetime, news_uri, news_title, news_headline, news_guid, news_article

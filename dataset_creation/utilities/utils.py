import os

import pandas as pd
import jsonlines

from parse_news import *
from datetime import datetime
import lxml.etree as ET

import pyppeteer
import asyncio

from contextlib import contextmanager
import signal


def get_links_media(media, tweets_path):
    '''
    Given tweets path and a media name returns a dictionary with the tweets id
    of those tweets related to sexual assault and the link corresponding to the
    news' page
    '''
    # Set paths
    csv_path = "{}/{}/predicted".format(tweets_path, media)
    json_path = "{}/{}/extended_jsonL".format(tweets_path, media)

    csv_dir = os.path.abspath(csv_path)
    id_url_dict = {}

    # Get tweet ids of tweets classified as sexual assault
    for file in os.listdir(csv_dir):
        csv = csv_path + "/" + file
        jsonl = json_path + "/" + file.split(".")[0] + ".jsonl"
        csv_file = pd.read_csv(csv, sep=",")
        ids = list(csv_file[csv_file["sexual_assault"] == 1]["id"])

        # Get news' url from json only for sexual_assualt related tweets

        if ids:
            with open(jsonl, "r") as f:
                for json_tweet in jsonlines.Reader(f):

                    if int(json_tweet["id"]) in ids:
                        try:
                            id_url_dict[json_tweet["id"]] = json_tweet["entities"]["urls"][0]["expanded_url"]
                        except:
                            pass

    return id_url_dict


def extract_information(path, media, tweet_id, soup, debug=False):
    if media == '20m':
        if debug: print(tweet_id, "entered in store_news")
        news_author, news_provider, news_creation_datetime, news_uri, \
        news_title, news_headline, news_guid, news_article = obtain_information_20m(tweet_id, soup)

    elif media == 'A3noticias':
        if debug: print(tweet_id, "entered in store_news")
        news_author, news_provider, news_creation_datetime, news_uri, \
        news_title, news_headline, news_guid, news_article = obtain_information_A3Noticias(tweet_id, soup)

    elif media == 'abc_es':
        if debug: print(tweet_id, "entered in store_news")
        news_author, news_provider, news_creation_datetime, news_uri, \
        news_title, news_headline, news_guid, news_article = obtain_information_abc_es(tweet_id, soup)

    elif media == 'COPE':
        if debug: print(tweet_id, "entered in store_news")
        news_author, news_provider, news_creation_datetime, news_uri, \
        news_title, news_headline, news_guid, news_article = obtain_information_cope(tweet_id, soup)

    elif media == 'EFEnoticias_ES':
        if debug: print(tweet_id, "entered in store_news")
        news_author, news_provider, news_creation_datetime, news_uri, \
        news_title, news_headline, news_guid, news_article = obtain_information_EFEnoticias(tweet_id, soup)

    elif media == 'elconfidencial':
        if debug: print(tweet_id, "entered in store_news")
        news_author, news_provider, news_creation_datetime, news_uri, \
        news_title, news_headline, news_guid, news_article = obtain_information_elconfidencial(tweet_id, soup)

    elif media == 'eldiarioes':
        if debug: print(tweet_id, "entered in store_news")
        news_author, news_provider, news_creation_datetime, news_uri, \
        news_title, news_headline, news_guid, news_article = obtain_information_eldiarioes(tweet_id, soup)

    elif media == 'elespanolcom':
        if debug: print(tweet_id, "entered in store_news")
        news_author, news_provider, news_creation_datetime, news_uri, \
        news_title, news_headline, news_guid, news_article = obtain_information_elespanolcom(tweet_id, soup)

    elif media == 'ElHuffPost':
        if debug: print(tweet_id, "entered in store_news")
        news_author, news_provider, news_creation_datetime, news_uri, \
        news_title, news_headline, news_guid, news_article = obtain_information_ElHuffPost(tweet_id, soup)

    elif media == 'elmundoes':
        if debug: print(tweet_id, "entered in store_news")
        news_author, news_provider, news_creation_datetime, news_uri, \
        news_title, news_headline, news_guid, news_article = obtain_information_elmundoes(tweet_id, soup)

    elif media == 'el_pais':
        if debug: print(tweet_id, "entered in store_news")
        news_author, news_provider, news_creation_datetime, news_uri, \
        news_title, news_headline, news_guid, news_article = obtain_information_el_pais(tweet_id, soup)

    elif media == 'elperiodico':
        if debug: print(tweet_id, "entered in store_news")
        news_author, news_provider, news_creation_datetime, news_uri, \
        news_title, news_headline, news_guid, news_article = obtain_information_elperiodico(tweet_id, soup)

    elif media == 'europapress':
        if debug: print(tweet_id, "entered in store_news")
        news_author, news_provider, news_creation_datetime, news_uri, \
        news_title, news_headline, news_guid, news_article = obtain_information_europapress(tweet_id, soup)

    elif media == 'informativost5':
        if debug: print(tweet_id, "entered in store_news")
        news_author, news_provider, news_creation_datetime, news_uri, \
        news_title, news_headline, news_guid, news_article = obtain_information_informativost5(tweet_id, soup)

    elif media == 'larazon_es':
        if debug: print(tweet_id, "entered in store_news")
        news_author, news_provider, news_creation_datetime, news_uri, \
        news_title, news_headline, news_guid, news_article = obtain_information_larazon_es(tweet_id, soup)

    elif media == 'La_SER':
        if debug: print(tweet_id, "entered in store_news")
        news_author, news_provider, news_creation_datetime, news_uri, \
        news_title, news_headline, news_guid, news_article = obtain_information_La_SER(tweet_id, soup)

    elif media == 'laSextaTV':
        if debug: print(tweet_id, "entered in store_news")
        news_author, news_provider, news_creation_datetime, news_uri, \
        news_title, news_headline, news_guid, news_article = obtain_information_laSextaTV(tweet_id, soup)

    elif media == 'LaVanguardia':
        if debug: print(tweet_id, "entered in store_news")
        news_author, news_provider, news_creation_datetime, news_uri, \
        news_title, news_headline, news_guid, news_article = obtain_information_laVanguardia(tweet_id, soup)

    elif media == 'libertaddigital':
        if debug: print(tweet_id, "entered in store_news")
        news_author, news_provider, news_creation_datetime, news_uri, \
        news_title, news_headline, news_guid, news_article = obtain_information_libertaddigital(tweet_id, soup)

    elif media == 'noticias_cuatro':
        if debug: print(tweet_id, "entered in store_news")
        news_author, news_provider, news_creation_datetime, news_uri, \
        news_title, news_headline, news_guid, news_article = obtain_information_noticias_cuatro(tweet_id, soup)

    elif media == 'okdiario':
        if debug: print(tweet_id, "entered in store_news")
        news_author, news_provider, news_creation_datetime, news_uri, \
        news_title, news_headline, news_guid, news_article = obtain_information_okdiario(tweet_id, soup)

    elif media == 'OndaCero_es':
        if debug: print(tweet_id, "entered in store_news")
        news_author, news_provider, news_creation_datetime, news_uri, \
        news_title, news_headline, news_guid, news_article = obtain_information_OndaCero_es(tweet_id, soup)

    elif media == 'publico_es':
        if debug: print(tweet_id, "entered in store_news")
        news_author, news_provider, news_creation_datetime, news_uri, \
        news_title, news_headline, news_guid, news_article = obtain_information_publico_es(tweet_id, soup)

    elif media == 'rtve':
        if debug: print(tweet_id, "entered in store_news")
        news_author, news_provider, news_creation_datetime, news_uri, \
        news_title, news_headline, news_guid, news_article = obtain_information_rtve(tweet_id, soup)

    elif media == 'voz_populi':
        if debug: print(tweet_id, "entered in store_news")
        news_author, news_provider, news_creation_datetime, news_uri, \
        news_title, news_headline, news_guid, news_article = obtain_information_voz_populi(tweet_id, soup)

    return news_author, news_provider, news_creation_datetime, news_uri, \
           news_title, news_headline, news_guid, news_article


def write_newsml(path, media, tweet_id, news_author, news_provider, news_creation_datetime, news_uri, \
                 news_title, news_headline, news_guid, news_article, debug=False):
    newsItem = ET.Element("newsItem")
    newsItem.set("standard", "NewsML-G2")
    newsItem.set("guid", news_guid)
    newsItem.set("version", "1")
    newsItem.set("conformance", "power")
    newsItem.set("standardversion", "2.15")

    catalogRef = ET.SubElement(newsItem, "catalogReg")
    catalogRef.set("href", "http://www.iptc.org/std/catalog/catalog.IPTC-G2-Standards_22.xml")

    ######################## item meta
    itemMeta = ET.SubElement(newsItem, "itemMeta")

    itemClass = ET.SubElement(itemMeta, "itemClass")
    itemClass.set("qcode", "ninat:text")

    provider = ET.SubElement(itemMeta, "provider")
    provider.set("qcode", "ninat:{}".format(news_provider))

    versionCreate = ET.SubElement(itemMeta, "itemMeta")
    versionCreate.text = datetime.now().strftime("%Y-%m-%dT%H:%M:%S+02:00")

    pubStatus = ET.SubElement(itemMeta, "pubStatus")
    pubStatus.set("qcode", "stat:usable")

    contributor = ET.SubElement(itemMeta, "contributor")
    name = ET.SubElement(contributor, "name")
    name.text = "Twitter"

    t_id = ET.SubElement(contributor, "tweet_id")
    t_id.text = str(tweet_id)

    ######################## content meta

    contentMeta = ET.SubElement(newsItem, "contentMeta")

    contentCreated = ET.SubElement(contentMeta, "contentCreated")
    contentCreated.text = news_creation_datetime

    located = ET.SubElement(contentMeta, "located")
    located.set("type", "cptype:country")
    located.set("qcode", "iso3166-1a2:ES")
    locality = ET.SubElement(located, "name")
    locality.text = "Spain"

    author = ET.SubElement(contentMeta, "creator")
    creator = ET.SubElement(author, "name")
    creator.text = news_author

    headline_lang = ET.SubElement(contentMeta, "headline")
    headline_lang.set("xml_lang", "es")
    headline_lang.text = "ES"

    info_source = ET.SubElement(contentMeta, "infoSource")
    info_source.set("uri", news_uri)

    ######################## main information
    groupSet = ET.SubElement(newsItem, "groupSet")
    groupSet.set("root", "G1")

    group = ET.SubElement(groupSet, "grup")
    group.set("id", "G1")
    group.set("role", "group:main")

    item1 = ET.SubElement(group, "itemRef")
    item1.set("residref", "{}:headline".format(news_guid))

    item1Class = ET.SubElement(item1, "itemClass")
    item1Class.set("qcode", "ninat:text")

    provider1 = ET.SubElement(item1, "provider")
    provider1.set("qcode", "ninat:{}".format(news_provider))

    pubStatus1 = ET.SubElement(item1, "pubStatus")
    pubStatus1.set("qcode", "stat:usable")

    title1 = ET.SubElement(item1, "title")
    title1.text = news_title

    description1 = ET.SubElement(item1, "description")
    description1.set("role", "drol:headline")
    description1.text = news_headline

    ############################ article

    item2 = ET.SubElement(group, "itemRef")
    item2.set("residref", "{}:article".format(news_guid))

    item2Class = ET.SubElement(item2, "itemClass")
    item2Class.set("qcode", "ninat:text")

    provider2 = ET.SubElement(item2, "provider")
    provider2.set("qcode", "ninat:{}".format(news_provider))

    pubStatus2 = ET.SubElement(item2, "pubStatus")
    pubStatus2.set("qcode", "stat:usable")

    description2 = ET.SubElement(item2, "description")
    description2.set("role", "drol:article")
    description2.text = news_article

    if debug: print("{}/{}_{}.xml".format(path, media, news_guid))
    with open("{}/{}_{}.xml".format(path, media, news_guid), "wb") as f:
        f.write(ET.tostring(newsItem, pretty_print=True))


async def nofollow_link(tweet_url):
    try:
        # with time_limit(200):
        browser = await pyppeteer.launch(headless=False)  # To visualize the browser set headless=False
        page = await browser.newPage()
        await page.goto(tweet_url)

        url_accessed = page.url
        if "google" in url_accessed:  # if the tweet is no longer available, it will be searched in google
            await browser.close()
            return None

        await page.waitFor(3000)
        await asyncio.wait([
            page.click('.css-1dbjc4n')
        ])
        await page.waitFor(5000)

        urls = []
        web_pages = await browser.pages()
        for p in web_pages:
            urls.append(p.url)

        await browser.close()
        if urls[-1] == tweet_url:
            return None
        return urls[-1]

    # except TimeoutException:
    # await browser.close()
    # print("Problem collecting no-follow link from {}".format(tweet_url))
    # return None

    except:
        try:
            await browser.close()
        except:
            pass
        print("Problem collecting no-follow link from {}".format(tweet_url))
        return None


def obtain_nofollow_links(tweet_url):
    '''
    Given a tweet url, obtain the url of the reference in the tweet
    '''
    news_link = asyncio.get_event_loop().run_until_complete(nofollow_link(tweet_url))
    return news_link

import warnings
warnings.filterwarnings('ignore')

from nltk.corpus import stopwords
from datetime import datetime
import lxml.etree as ET
import pandas as pd
import regex as re
import unidecode
import html
import os

INPUT_FILE_PATH = 'data/cases_labeled.csv'
NEWS_PATH = 'data/news/'

def listdir_checked(path, unwanted = ['.DS_Store']):
    '''
    Discard unwanted files or directories when listing the elements in a given path
    '''
    return (f for f in os.listdir(path) if f not in unwanted)

def normalize_string(to_normalize, encoded = False):
    '''
    Normalize text given a string
    '''
    text = str(to_normalize).lower()  # lowering text
    if encoded:
        text = ' '.join([html.unescape(term) for term in text.split()])
    text = unidecode.unidecode(text)

    text = re.sub(r'[^\w\s]', '', text)  # removing all the punctuations
    last_text = text.split()  # tokenize the text

    # remove stopwords
    stopwords_set = set(stopwords.words("spanish"))
    stopwords_set = stopwords_set.union(set(["name", "email", "organization"]))

    last_text = ' '.join([x for x in last_text if (x not in stopwords_set)])
    return last_text


def create_articles_dictionary(NEWS_PATH):
    '''
    Import articles information.
    Articles are stored in directories in the NEWS_PATH.
    '''
    data = {}               # keys: media, value: list of dictionaries with info about the news articles of the given media
    unique_urls = []        # list to store unique urls to discard repeated ones
    repeated_data = {}      # store repeated articles following the same format as 'data' dictionary


    for year in listdir_checked(NEWS_PATH):

        if(year=='2020'):
            for month in listdir_checked(NEWS_PATH + '/' + year):
                if month in ['1', '2', '3']:
                    for file in listdir_checked(NEWS_PATH + '/' + year + '/' + month):
                        full_path = NEWS_PATH + '/' + year + '/' + month + '/' + file
                        # Read xml file - info stored following NewsML-G2 format
                        root = ET.parse(full_path).getroot()
                        # Parse news
                        media = file.rsplit('_', 1)[0]
                        # Check repeated urls
                        url = root.findall(".//infoSource")[0].get("uri")
                        str_date = root.findall('.//contentMeta')[0].find('contentCreated').text[:10]
                        info = {
                            'id': file.split(':')[-1].replace('.xml', ''),
                            'media': media,
                            'publication_date': datetime.strptime(str_date, '%Y-%m-%d'),
                            'title': normalize_string(root.findall('.//itemRef')[0].find('title').text, encoded = True),
                            'headline': normalize_string(root.findall(".//itemRef")[0].find('description').text.strip(), encoded = True),
                            'article': normalize_string(root.findall('.//itemRef')[1].find('description').text.strip(), encoded = True),                'url': url
                        }

                        if url not in unique_urls:
                            unique_urls.append(url)
                            try:
                                data[media].append(info)
                            except:
                                data[media] = [info]

                        else:
                            try:
                                repeated_data[media].append(info)
                            except:
                                repeated_data[media] = [info]

    return data, repeated_data


data, repeated_data = create_articles_dictionary(NEWS_PATH)
counter = 500

cases_df = pd.read_csv(INPUT_FILE_PATH, sep=';')
cases_df['tweet_id'] = cases_df['tweet_id'].apply(lambda x: str(x))

cases_df = cases_df[cases_df['checked'] == 1]

for media in data.keys():
    for new in data[media]:
        tweet_id = new['id']
        if tweet_id not in list(cases_df['tweet_id']):
            case_id = counter
            counter += 1
            checked = 0
            title = normalize_string(new['title'])
            headline = normalize_string(new['headline'])
            url = new['url']
            publication_date = new['publication_date']

            cases_df = cases_df.append({'tweet_id': tweet_id, 'media': media, 'checked': checked, 'case_id': case_id,
                                       'title': title, 'headline': headline, 'url': url, 'publication_date': publication_date},
                                       ignore_index=True)

print(cases_df.info())
cases_df.to_csv('data/cases_labeled_2020_1.csv', sep=';', index=False)
cases_df.info()

import pandas as pd
from searchtweets import collect_results, load_credentials, gen_request_parameters
import os
import json
import time
import scrubadub
import nltk

nltk.download('punkt')

# GLOBAL VARIABLES

ACCOUNTS = ["20m", "el_pais", "laSextaTV", "elconfidencial", "rtve", "LaVanguardia", "abc_es", "La_SER", "okdiario",
            "eldiarioes", "elperiodico", "larazon_es", "informativost5", "elmundoes", "A3noticias", "noticias_cuatro",
            "COPE", "OndaCero_es", "publico_es", "ElHuffPost", "elespanolcom", "libertaddigital", "europapress",
            "EFEnoticias_ES", "voz_populi"]

FREQ = "D"
#DATA_PATH = "/mnt/vmdata/tweetsprocessing-wssc/data/tweets/"
DATA_PATH = "data/tweets/"
MAX_TWEETS = 500
START_DAY = "2021-8-01"
FINAL_DAY = "2021-9-01"
MONTH = "8"
YEAR = "2021"


def get_tweets(account, start_time, end_time):
    rule = gen_request_parameters("from:" + account,  # account name
                                  start_time=start_time,
                                  end_time=end_time,
                                  tweet_fields="id,text,created_at,author_id,entities,in_reply_to_user_id," +
                                               "possibly_sensitive,public_metrics",
                                  # comma-delimted list of Tweet JSON attributes wanted in endpoint responses
                                  results_per_call=MAX_TWEETS,
                                  granularity=None)

    tweets = collect_results(rule, max_tweets=MAX_TWEETS, result_stream_args=search_args)

    return tweets


def tweets_to_df(tweets):
    df = pd.json_normalize(tweets[0]["data"])

    annotations_list = []
    urls_list = []
    hashtags_list = []
    mentions_list = []

    for i in df.iterrows():
        try:
            annotations = df["entities.annotations"][i[0]]
            annotations_text = [a["normalized_text"] for a in annotations]
        except (TypeError, KeyError):
            annotations_text = None

        try:
            url = df["entities.urls"][i[0]][0]["expanded_url"]
        except (TypeError, KeyError):
            url = None

        try:
            hashtags = df["entities.hashtags"][i[0]]
            hashtags_text = [h["tag"] for h in hashtags]
        except (TypeError, KeyError):
            hashtags_text = None

        try:
            mentions = df["entities.mentions"][i[0]]
            mentions_text = [m["username"] for m in mentions]
        except (TypeError, KeyError):
            mentions_text = None

        annotations_list.append(annotations_text)
        urls_list.append(url)
        hashtags_list.append(hashtags_text)
        mentions_list.append(mentions_text)

    df["entities.urls"] = urls_list
    df["entities.annotations"] = annotations_list
    df["entities.hashtags"] = hashtags_list
    df["entities.mentions"] = mentions_list

    return df


if __name__ == "__main__":

    search_args = load_credentials("twitter_keys.yaml",  # Config file
                                   yaml_key="search_tweets_v2",
                                   env_overwrite=False)

    scrubber = scrubadub.Scrubber()
    scrubber.add_detector(scrubadub.detectors.TextBlobNameDetector)

    out_path = os.path.abspath(f'''{DATA_PATH}{YEAR}/{MONTH}''')

    if not os.path.exists(out_path):
        os.makedirs(out_path)

    out_filename = f'''{out_path}/out.txt'''  # Name of out file
    out = open(out_filename, 'w')

    for account in ACCOUNTS:  # For each account
        print("Starting with: ", account)
        tweets_for_account = 0

        #  Define directories
        dir_path = os.path.abspath(f'''{DATA_PATH}{YEAR}/{MONTH}/{account}''')
        dir_path_jsonl = os.path.abspath(f'''{DATA_PATH}{YEAR}/{MONTH}/{account}/{"extended_jsonL"}''')

        if not os.path.exists(dir_path_jsonl):
            os.makedirs(dir_path_jsonl)

        # List of days to take tweets of each day
        day_list = pd.date_range(START_DAY, FINAL_DAY, freq=FREQ)

        #  For each day get the tweets
        for i in range(0, len(day_list) - 1):
            start_time = str(day_list[i].date())
            end_time = str(day_list[i + 1].date())

            filename = f'''{dir_path}/{account}_{start_time}_{end_time}.csv'''
            tweets = get_tweets(account, start_time, end_time)

            if tweets:

                for tweet in tweets[0]["data"]:
                    tweet["text"] = scrubber.clean(tweet["text"])

                df = tweets_to_df(tweets)

                # Save tweets
                df.to_csv(filename, index=False, header=True)

                json_filename = f'''{dir_path_jsonl}/{account}_{start_time}_{end_time}.jsonl'''  # Name of json file
                with open(json_filename, 'w') as outfile:  # PATH to directory and name of the file
                    for tweet in tweets[0]["data"]:
                        outfile.write(str(json.dumps(tweet)) + '\n')

                #  If we have the maximum number of tweets print the day
                if df.shape[0] == MAX_TWEETS:
                    print("MAX NUM OF TWEETS!!")
                    print(start_time, end_time)
                    print(df.shape[0])
                else:
                    tweets_for_account += df.shape[0]
            time.sleep(5)
        #  Write the output of the account
        print("Downloaded", tweets_for_account, "tweets")
        out.write(str(account) + " " + str(tweets_for_account) + "\n")
        time.sleep(5)
    out.close()

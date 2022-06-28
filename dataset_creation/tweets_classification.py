from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from nltk.corpus import stopwords
from pathlib import Path
from sklearn.metrics import roc_auc_score,  precision_recall_curve
import pandas as pd
import unidecode
import argparse
import os
import re
import nltk
import numpy as np
from sklearn.metrics import confusion_matrix

nltk.download('stopwords')



# Function to avoid unwanted paths
def checked(path, unwanted=["extended_jsonL", "out.txt", "Classified", "predicted"]):
    # unwanted = [".DS_Store", "__Interval.csv", "Json", "Classified", "Logistic predictor.ipynb", "extended_json"]
    return (f for f in os.listdir(path) if f not in unwanted)


def normalize_string(to_normalize):
    # Normalize text given a string,
    text = str(to_normalize).lower()  # lowering text
    text = unidecode.unidecode(text)
    text = re.sub(r'[^\w\s]', '', text)  # removing all the punctuations
    last_text = text.split()
    try:
        if last_text[-1][:5] == 'https':
            last_text.pop(-1)
    except IndexError:
        pass
    stopwords_set = set(stopwords.words("spanish"))
    stopwords_set = stopwords_set.union(set(["name", "email", "organization"]))
    last_text = ' '.join([x for x in last_text if (x not in stopwords_set)])
    return last_text


# FEATURE EXTRACTION
# returns train, test and CountVectorizer object
def extract_features(df, field, training_data, testing_data):
    # binary feature representation
    cv = CountVectorizer()
    cv.fit_transform(training_data[field].values)  # creates a vocabulary based on the training set

    # transforms the text according to the vocabulary in the training set
    train_feature_set = cv.transform(training_data[field].values)
    test_feature_set = cv.transform(testing_data[field].values)

    return train_feature_set, test_feature_set, cv


# TRAINING FUNCTION
def train(df):
    # split training / test data
    training_data, testing_data = train_test_split(df, random_state=2000, test_size=0.1)

    # get labels
    Y_train = training_data["sexual_assault"].values
    Y_test = testing_data["sexual_assault"].values
    # get features
    X_train, X_test, feature_transformer = extract_features(df, "text", training_data, testing_data)
    # logistic regression classifier
    scikit_log_reg = LogisticRegression(verbose=1, solver='liblinear', C=5, penalty='l2', max_iter=1000)

    model = scikit_log_reg.fit(X_train, Y_train.astype(int))
    score = model.score(X_test, Y_test.astype(int))

    precision, recall, thresholds = precision_recall_curve(Y_test.astype(int), model.predict_proba(X_test)[:, 1])

    numerator = 2 * recall * precision
    denom = recall + precision  
    f1_scores = np.divide(numerator, denom, out=np.zeros_like(denom), where=(denom != 0))

    best_threshold = thresholds[np.argmax(f1_scores)]



    print('Best threshold: ', best_threshold)
    print('Precision', precision[np.argmax(f1_scores)])
    print('Recall', recall[np.argmax(f1_scores)])
    print('Best F1-Score: ', np.max(f1_scores))

    print("Testing accuracy = ", score)
    print("Testing AUC score = ", roc_auc_score(Y_test, model.predict_proba(X_test)[:, 1]))

    Y_labels = model.predict_proba(X_test)[:, 1]
    Y_labels[Y_labels >= best_threshold] = 1
    Y_labels[Y_labels < best_threshold] = 0

    print(confusion_matrix(Y_test, Y_labels))


    return model, feature_transformer, best_threshold


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("-data", nargs='*', help='Absolute path to data directories')
    parser.add_argument("-train", nargs='*', help='Path to directories with CSV files containing labeled tweets')
    parser.add_argument("-predict", nargs='*',
                        help='Path to directories with CSV files containing tweets to be predicted')
    args = parser.parse_args()

    train_set = args.train
    predict_set = args.predict
    tweets_path = args.data[0]

    # IMPORT CLASSIFIED DATASET
    classified_df = pd.DataFrame()

    for directory in train_set:
        training_path = os.path.abspath(tweets_path + directory)
        for file in checked(training_path):
            if file[:10] == "classified":
                f_path = training_path + "/" + file
                try:
                    aux = pd.read_csv(f_path, sep=";")[["sexual_assault", "text"]]
                except:
                    aux = pd.read_csv(f_path, sep=",")[["sexual_assault", "text"]]

                aux['text'] = aux['text'].apply(lambda x: normalize_string(x))

                classified_df = classified_df.append(aux)

    # Ambiguous strings labeled as 2 must be dropped out
    classified_df.drop(classified_df[classified_df['sexual_assault'] == 2].index, inplace=True)

    print(classified_df[classified_df['sexual_assault']==1].shape[0])
    print(classified_df.shape[0])

    # TRAIN
    model, feature_transf, best_threshold = train(classified_df)

    # PREDICT
    for directory in predict_set:
        print('PREDICT DIRECTORY:', directory)
        predicting_path = os.path.abspath(tweets_path + directory)

        for media in checked(predicting_path):
            print('----- PREDICTING:', media)
            media_path = os.path.abspath(predicting_path + '/' + media)

            for f in checked(media_path):   
                df = pd.read_csv(media_path + "/" + f)
                tweets_list = []
                for t in df["text"]:
                    tweets_list.append(normalize_string(str(t)))
                tweets = feature_transf.transform(tweets_list)

                tweets_labels = model.predict_proba(tweets)[:, 1]
                tweets_labels[tweets_labels >= best_threshold] = 1
                tweets_labels[tweets_labels < best_threshold] = 0

                df.insert(0, "predicted_proba", model.predict_proba(tweets)[:, 1], True)
                df.insert(0, "sexual_assault", tweets_labels, True)

                Path(f'{media_path}/predicted').mkdir(parents=True,
                                                       exist_ok=True)  # Check if the output directory exists, else create it
                df.to_csv(media_path + "/predicted/" + f)

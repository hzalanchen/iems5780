'''
# -*- coding: utf-8 -*-
@FileName: anime.py
'''

import pandas as pd
import pickle
import os

from surprise import Dataset
from surprise import Reader
from surprise import SVD
from surprise import dump
from surprise.model_selection import cross_validate

from surprise.model_selection import train_test_split
from collections import defaultdict


def process_data():
    '''
    Use the first 4000 users as 5-fold cross validation, and leave the last 1000 users as a testing set.
    :return:
    '''
    df_ratings = pd.read_csv('anime/anime_ratings.dat', sep='\t')
    df_info = pd.read_csv('anime/anime_info.dat', sep='\t')
    df_ratings_train = df_ratings[df_ratings['User_ID'] <= 4000]
    df_ratings_test = df_ratings[df_ratings['User_ID'] > 4000]

    reader = Reader(rating_scale=(1, 10))
    training_set = Dataset.load_from_df(df_ratings_train[['User_ID', 'Anime_ID', 'Feedback']], reader)
    testing_set = Dataset.load_from_df(df_ratings_test[['User_ID', 'Anime_ID', 'Feedback']], reader)

    return df_info, training_set, testing_set



def cross_valdation_and_svd_model(training_set, k=5):
    '''
    Compute the RMSE (root mean square error) for the 5-fold cross validation.
    Generate a SVD model using all training data, and save the model as
    anime_model.pickle using dump.
    :param ratings_data:
    :param k:
    :return: svd model
    '''

    svd = SVD(verbose=True, n_epochs=10)
    print("Compute the RMSE (root mean square error) for the 5-fold cross validation:")
    cross_validate(svd, training_set, measures=['RMSE'], cv=k, verbose=True)

    train_set = training_set.build_full_trainset()
    svd.fit(train_set)
    dump.dump("./anime_model.pickle", algo=svd, verbose=1)
    return svd



def precision_recall_at_k(predictions, k=10, threshold=3.5):
    '''Returns the precision and recall when recommending k items for each user.'''

    # First map the predicted values to each user
    user_est_true = defaultdict(list)
    for uid, _, true_r, est, _ in predictions:
        user_est_true[uid].append((est, true_r))

    precisions = dict()
    recalls = dict()
    for uid, user_ratings in user_est_true.items():

        # Sort user ratings by estimated value
        user_ratings.sort(key=lambda x: x[0], reverse=True)

        # Number of relevant items
        n_rel = sum((true_r >= threshold) for (_, true_r) in user_ratings)

        # Number of recommended items in top k
        n_rec_k = sum((est >= threshold) for (est, _) in user_ratings[:k])

        # Number of relevant and recommended items in top k
        n_rel_and_rec_k = sum(((true_r >= threshold) and (est >= threshold))
                              for (est, true_r) in user_ratings[:k])

        # Precision@K: Proportion of recommended items that are relevant
        precisions[uid] = n_rel_and_rec_k / n_rec_k if n_rec_k != 0 else 1

        # Recall@K: Proportion of relevant items that are recommended
        recalls[uid] = n_rel_and_rec_k / n_rel if n_rel != 0 else 1

    return precisions, recalls



def evaluate(testing_set, algo):
    '''
    Compute accuracy based on the testing set using top-10 predictions.
    For each of the top 10 predictions, if the actual score is greater than 5, it is regarded as a correct prediction.
    :param testing_set:
    :param algo: Model of SVD
    :return:
    '''

    trainset, testset = train_test_split(testing_set, test_size=0.00001)
    testset = trainset.build_testset()

    predictions = algo.test(testset)
    precisions, recalls = precision_recall_at_k(predictions, k=10, threshold=5)
    acc = sum(prec for prec in precisions.values()) / len(precisions)
    print("The accuracy on the testing set using top-10 predictions is: ", acc)



def main():
    df_info, training_set, testing_set = process_data()
    svd = cross_valdation_and_svd_model(training_set)
    evaluate(testing_set, svd)


if __name__ == '__main__':
    main()







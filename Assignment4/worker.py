'''
# -*- coding: utf-8 -*-
@FileName: worker.py
'''

import heapq
import time
import pickle
from collections import defaultdict
from operator import itemgetter

import pandas as pd
from redis import StrictRedis
from celery import Celery
from surprise import Reader, Dataset, dump

broker = 'redis://localhost:6379/0'
backend = 'redis://localhost:6379/1'

app = Celery('tasks', broker = broker, backend = backend)


def load_dataset():
    '''
    Use the first 4000 users as 5-fold cross validation, and leave the last 1000 users as a testing set.
    :return:
    '''
    reader = Reader(rating_scale=(1, 10))
    anime_ratings = pd.read_table('anime/anime_ratings.dat')
    ratings_dataset = Dataset.load_from_df(anime_ratings[['User_ID', 'Anime_ID', 'Feedback']], reader)
    animeID_to_name = {}
    with open('anime/anime_info.dat', 'r', encoding='utf-8') as FH:
        for file in FH.readlines():
            line = file.strip()
            context = line.split('	')

            if context[0] != 'anime_ids':
                animeID = int(context[0])
                anime_name = context[1]
                animeID_to_name[animeID] = anime_name
    return (ratings_dataset, animeID_to_name)


@app.task
def subscribe():
    '''
    Process the request from the bot in channel "anime.request"
    Then publish the result of recommendations to user in channel "anime.respones"
    :return:
    '''

    _, model = dump.load('anime_model.pickle')
    # model = pickle.load('anime_model.pickle')
    # load dataset
    dataset, animeID_to_name = load_dataset()
    # Build the train set
    trainset = dataset.build_full_trainset()
    # Computer the similarity matrix
    similarity_matrix = model.fit(trainset).compute_similarities()

    pubsub = StrictRedis(host='localhost', port=6379).pubsub()
    pubsub.subscribe('anime_request')
    message = pubsub.get_message()

    def getAnimeName(animeID):
        if int(animeID) in animeID_to_name: return animeID_to_name[int(animeID)]
        else: return ""

    while True:
        message = pubsub.get_message()
        print(message)
        if message and message['data'] != 1:
            #
            arr_str = message['data'].decode("utf-8")
            arr = arr_str.split(",")
            index = 0
            output = []
            for i in range(10):
                sub_res = []
                sub_res.append(int(arr[index]))
                sub_res.append(int(arr[index + 1]))
                output.append(sub_res)
                index = index + 2

            k_neighbors = heapq.nlargest(10, output, key=lambda t: t[1])
            candidates = defaultdict(float)
            # K-neighbors
            for itemID, rating in k_neighbors:
                try:
                    similaritities = similarity_matrix[itemID]
                    for innerID, score in enumerate(similaritities):
                        candidates[innerID] += score * (rating / 5.0)
                except:
                    continue
            # Get the recommendation
            recommendations = []

            position = 0
            reply = "Top 10 recommendation anime for you:"
            reply += '\n'
            # Get the itemId and rating sum
            for itemID, rating_sum in sorted(candidates.items(), key=itemgetter(1), reverse=True):
                # Get the recommendations
                recommendations.append(getAnimeName(trainset.to_raw_iid(itemID)))
                position += 1
                if (position > 9): break
            id = 1
            for rec in recommendations:
                reply += str(id)
                reply += "."
                reply += rec
                reply += '\n'
                id = id + 1

            # Connect the redis channel
            queue = StrictRedis(host='localhost', port=6379)

            # Publish the result into anime_response channel.
            queue.publish("anime_response", reply.encode("utf-8"))
        else:
            time.sleep(1)

subscribe.delay()

'''
# -*- coding: utf-8 -*-
@FileName: bot.py
'''


import time
import logging
from surprise import Reader, Dataset, dump
from telegram.ext.updater import Updater
from telegram.update import Update
from telegram.ext.callbackcontext import CallbackContext
from telegram.ext.commandhandler import CommandHandler
from telegram.ext.messagehandler import MessageHandler
from telegram.ext.filters import Filters
from collections import defaultdict
from redis import StrictRedis
import pandas as pd
import random

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)


def start(update: Update, context: CallbackContext):
    update.message.reply_text("Hello sir, Welcome to IEMS5780_1155161034_bot.")


def load_dataset():
    '''
    Load the dataset of the anime_ratings.dat
    :return:
    '''
    reader = Reader(rating_scale=(1, 10))

    anime_ratings = pd.read_table('anime/anime_ratings.dat')
    ratings_dataset = Dataset.load_from_df(anime_ratings[['User_ID', 'Anime_ID', 'Feedback']], reader)
    animeID_name = {}
    with open('anime/anime_info.dat', 'r',encoding='utf-8') as File:
        for file in File.readlines():
            line = file.strip()
            context = line.split('	')

            # for row in line.strip(" "):
            if context[0] != 'anime_ids':
                animeID = int(context[0])
                anime_name = context[1]
                animeID_name[animeID] = anime_name
    return (ratings_dataset, animeID_name)


def help(update: Update, context: CallbackContext):
    update.message.reply_text("""Available Commands :-
    /rate_and_recommend: Rate ten animes and get the recommendation.
    """)


class State:
    def __init__(self):
        self.statenum = 'general'
        self.res = []
        self.temp = ''
        self.animeID = 0
        self.sendContext = ""


def general(update: Update, context: CallbackContext):
    if s.statenum == "start_predict":
        rand_num = random.randint(1, 7390)

        update.message.reply_text(
            "Rating the ten anime with score with 1 to 10 \n" + animeID_to_name[rand_num])
        response = int(update.message.text)
        if int(response) < 0 or int(response) > 10:
            update.message.reply_text("Please input the integer from 1 to 10: ")
        else:
            s.res.append([s.animeID, response])
            s.statenum = "question2"
            s.animeID = rand_num

        return
    if s.statenum == "question2":
        rand_num = random.randint(1, 7390)

        update.message.reply_text(
            "Rating the ten anime with score with 1 to 10 \n" + animeID_to_name[rand_num])
        response = int(update.message.text)
        if int(response) < 0 or int(response) > 10:
            update.message.reply_text("Please input the integer from 1 to 10: ")
        else:
            s.res.append([s.animeID, response])
            s.statenum = "question3"
            s.animeID = rand_num

        return

    if s.statenum == "question3":
        rand_num = random.randint(1, 7390)

        update.message.reply_text(
            "Rating the ten anime with score with 1 to 10 \n" + animeID_to_name[rand_num])
        response = int(update.message.text)
        if int(response) < 0 or int(response) > 10:
            update.message.reply_text("Please input the integer from 1 to 10: ")
        else:
            s.res.append([s.animeID, response])
            s.statenum = "question4"
            s.animeID = rand_num

        return
    if s.statenum == "question4":
        rand_num = random.randint(1, 7390)

        update.message.reply_text(
            "Rating the ten anime with score with 1 to 10 \n" + animeID_to_name[rand_num])
        response = int(update.message.text)
        if int(response) < 0 or int(response) > 10:
            update.message.reply_text("Please input the integer from 1 to 10: ")
        else:
            s.res.append([s.animeID, response])
            s.statenum = "question5"
            s.animeID = rand_num

        return

    if s.statenum == "question5":
        rand_num = random.randint(1, 7390)

        update.message.reply_text(
            "Rating the ten anime with score with 1 to 10 \n" + animeID_to_name[rand_num])
        response = int(update.message.text)
        if int(response) < 0 or int(response) > 10:
            update.message.reply_text("Please input the integer from 1 to 10: ")
        else:
            s.res.append([s.animeID, response])
            s.statenum = "question6"
            s.animeID = rand_num

        return

    if s.statenum == "question6":
        rand_num = random.randint(1, 7390)

        update.message.reply_text(
            "Rating the ten anime with score with 1 to 10 \n" + animeID_to_name[rand_num])
        response = int(update.message.text)
        if int(response) < 0 or int(response) > 10:
            update.message.reply_text("Please input the integer from 1 to 10: ")
        else:
            s.res.append([s.animeID, response])
            s.statenum = "question7"
            s.animeID = rand_num

        return

    if s.statenum == "question7":
        rand_num = random.randint(1, 7390)

        update.message.reply_text(
            "Rating the ten anime with score with 1 to 10 \n" + animeID_to_name[rand_num])
        response = int(update.message.text)
        if int(response) < 0 or int(response) > 10:
            update.message.reply_text("Please input the integer from 1 to 10: ")
        else:
            s.res.append([s.animeID, response])
            s.statenum = "question8"
            s.animeID = rand_num

        return

    if s.statenum == "question8":
        rand_num = random.randint(1, 7390)

        update.message.reply_text(
            "Rating the ten anime with score with 1 to 10 \n" + animeID_to_name[rand_num])
        response = int(update.message.text)
        if int(response) < 0 or int(response) > 10:
            update.message.reply_text("Please input the integer from 1 to 10: ")
        else:
            s.res.append([s.animeID, response])
            s.statenum = "question9"
            s.animeID = rand_num

        return

    if s.statenum == "question9":
        rand_num = random.randint(1, 7390)

        update.message.reply_text(
            "Rating the ten anime with score with 1 to 10 \n" + animeID_to_name[rand_num])
        response = int(update.message.text)
        if int(response) < 0 or int(response) > 10:
            update.message.reply_text("Please input the integer from 1 to 10: ")
        else:
            s.res.append([s.animeID, response])
            s.statenum = "predict"
            s.animeID = rand_num

        return

    if s.statenum == "predict":
        response = int(update.message.text)
        if int(response) < 0 or int(response) > 10:
            update.message.reply_text("Please input the integer from 1 to 10: "
                                      "")
        else:
            s.res.append([s.animeID, response])
            queue = StrictRedis(host='localhost', port=6379)
            message_send = ""
            for i in range(9):
                for j in range(2):
                    message_send += str(s.res[i][j])
                    message_send += ","
            message_send += str(s.res[9][0])
            message_send += ","
            message_send += str(s.res[9][1])

            queue.publish("anime_request", message_send.encode("utf-8"))

            flag = True
            pubsub = StrictRedis(host='localhost', port=6379).pubsub()
            pubsub.subscribe('anime_response')
            # The first message you receive will be a confirmation of subscription
            message = pubsub.get_message()
            while flag:

                message = pubsub.get_message()
                print(message)
                if message and message['data'] != 1:
                    msg = message['data'].decode("utf-8")
                    update.message.reply_text(msg)
                    flag = False

                else:
                    time.sleep(1)

            s.statenum = "general"
        return


def rate_and_recommend(update: Update, context: CallbackContext):
    rand_num = random.randint(1, 7390)
    update.message.reply_text(
        "Rating the ten anime with score with 1 to 10 \n" + animeID_to_name[rand_num])
    s.statenum = "start_predict"
    s.animeID = rand_num




if __name__ == "__main__":
    # Provide your bot's token
    updater = Updater("5253385256:AAFpLJLoS4bG2YT4UxX0Msmrr-YdWJWEpsM", use_context=True)
    dispatcher = updater.dispatcher
    s = State()
    dataset, animeID_to_name = load_dataset()

    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CommandHandler('help', help))
    dispatcher.add_handler(CommandHandler('rate_and_recommend', rate_and_recommend))
    dispatcher.add_handler(MessageHandler(Filters.text, general))
    updater.start_polling()
    updater.idle()
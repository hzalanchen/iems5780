import logging
from telegram.ext import dispatcher
from telegram.ext.updater import Updater
from telegram.update import Update
from telegram.ext.callbackcontext import CallbackContext
from telegram.ext.commandhandler import CommandHandler
from telegram.ext.messagehandler import MessageHandler
from telegram.ext import ConversationHandler
from telegram.ext.filters import Filters
from joblib import load


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)


Title1, Text1, Title2, Text2 = range(4)
gTitle1, gTitle2 = "", ""

def start(update: Update, context: CallbackContext):
    update.message.reply_text("Hello sir, Welcome to IEMS5780_1155161034_bot.")

def help(update: Update, context: CallbackContext):
    update.message.reply_text("""Available Commands :
    /count_model: Use CounterVectorizer model.
    /tfidf_model: Use TfidfVectorizer model.
    """
    )

def general(update: Update, context: CallbackContext):
    update.message.reply_text("This is a Telegram bot to test the message is REAL or FAKE.\nType /help to display the commands.")

# CountVectorize
def count_model(update: Update, context: CallbackContext):
    print("This is the count_model")
    update.message.reply_text(
        "This is CounterVectorizer model.\nWhat is the title of your message?"
    )

    return Title1

def title1(update: Update, context: CallbackContext):
    print(update.message.text)
    global gTitle1 
    gTitle1 = update.message.text
    update.message.reply_text("What is the content of your message?")

    return Text1

def text1(update: Update, context: CallbackContext):
    global gTitle1
    total_text = gTitle1 + ". " + update.message.text
    print(total_text)
    pred = countModel.predict_proba([total_text])[0][1]
    Msg = ""
    if pred < 0.4: Msg = "Your message is FAKE (p = {:.4s})".format(str(pred))
    elif pred > 0.6: Msg = "Your message is REAL (p = {:.4s})".format(str(pred))
    else: Msg = "Sorry, cannot determine if the message is fake or real."

    update.message.reply_text(Msg)
    return ConversationHandler.END


# TfidfVectorize
def tfidf_model(update: Update, context: CallbackContext):
    print("This is the tfidf_model")
    update.message.reply_text(
        "This is TfidfVectorizer model.\nWhat is the title of your message?"
    )

    return Title2

def title2(update: Update, context: CallbackContext):
    print(update.message.text)
    global gTitle2
    gTitle2 = update.message.text
    update.message.reply_text("What is the content of your message?")

    return Text2

def text2(update: Update, context: CallbackContext):
    global gTitle2
    total_text = gTitle2 + ". " + update.message.text
    print(total_text)
    pred = tfidfModel.predict_proba([total_text])[0][1]
    Msg = ""
    if pred < 0.4: Msg = "Your message is FAKE (p = {:.4s})".format(str(pred))
    elif pred > 0.6: Msg = "Your message is REAL (p = {:.4s})".format(str(pred))
    else: Msg = "Sorry, cannot determine if the message is fake or real."

    update.message.reply_text(Msg)
    return ConversationHandler.END

def cancel(update: Update, context: CallbackContext):
    update.message.reply_text("Cancel the conversation.")
    return ConversationHandler.END
    

if __name__ == "__main__":
    
    # Provide your bot's token
    updater = Updater("XXX", use_context=True)
    dispatcher = updater.dispatcher


    # In assignment, if you need to load the model, load it here
    countModel = load("count_model.pkl")
    tfidfModel = load("tfidf_model.pkl")
    

    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CommandHandler('help', help))
    count_handler = ConversationHandler(
        entry_points=[CommandHandler('count_model',count_model)],
        states={
                Title1 : [MessageHandler(Filters.text, title1)],
                Text1 : [MessageHandler(Filters.text, text1)]
        },
        fallbacks=[CommandHandler('cancel', cancel)],

    )
    dispatcher.add_handler(count_handler)


    tfidf_handler = ConversationHandler(
        entry_points=[CommandHandler('tfidf_model',tfidf_model)],
        states={
                Title2 : [MessageHandler(Filters.text, title2)],
                Text2 : [MessageHandler(Filters.text, text2)]
        },
        fallbacks=[CommandHandler('cancel', cancel)],

    )
    dispatcher.add_handler(tfidf_handler)

    dispatcher.add_handler(MessageHandler(Filters.text, general))
    updater.start_polling()
    updater.idle()


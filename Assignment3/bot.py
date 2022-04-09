import re
import socket
import logging
from urllib.request import urlretrieve
from queue import Queue
from threading import Thread
from telegram.ext.updater import Updater
from telegram.update import Update
from telegram.ext.callbackcontext import CallbackContext
from telegram.ext.commandhandler import CommandHandler
from telegram.ext.messagehandler import MessageHandler
from telegram.ext.filters import Filters
import telegram

chat_id = 0

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


def start(update: Update, context: CallbackContext):
    update.message.reply_text("Hello sir, Welcome to IEMS5780_1155161034_bot.")


def general_and_getlink(update: Update, context: CallbackContext):
    global chat_id
    chat_id = update.message.chat_id
    logger.info("General and get link")
    img_format = ['jpg', 'jpeg', 'png', 'gif', 'bmp', 'tif', 'pcx', 'tga', 'exif', 'fpx', 'svg', 'psd', 'cdr', 'pcd', 'dxf', 'ufo', 'webp', 'apng', 'eps', 'raw', 'wmf', 'avif']
    img_format_upper = list(map(lambda x: x.upper(), img_format))
    msg = update.message.text
    if re.match(r'^https?:/{2}\w.+$', msg):
        if msg.split('.')[-1] not in img_format and msg.split('.')[-1] not in img_format_upper:
            update.message.reply_text("The url link is not an image.")
        else:
            urlretrieve(msg, 'user_image.jpg')
            with open('user_image.jpg', 'rb') as file:
                q1.put(file.read())
            conn = Thread(target=comm_with_server)
            conn.start()
            update.message.reply_text("The image is processing...")
    else:
        update.message.reply_text(
        """This is a Telegram bot to classify the four types of migratory birds. You can send an image or a url to the image to get the probabilities of the four types of the migratory birds.""")


def get_photo(update: Update, context: CallbackContext):
    global chat_id
    image_file = update.message.photo[-1].get_file()
    logger.info(image_file)
    # Get user chat id
    chat_id = update.message.chat_id
    logger.info(chat_id)
    logger.info("Getting photo")
    process_msg = Thread(target=process_image, args=(image_file,))
    process_msg.start()

    #update.message.reply_text("Image")


def process_image(image_file):
    logger.info("Processing image")
    image_file.download('user_image.jpg')
    with open('user_image.jpg', 'rb') as file:
        q1.put(file.read())
    conn = Thread(target=comm_with_server)
    conn.start()


def comm_with_server():
    logger.info("Connect with server.")
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(("47.99.244.231", 50001))
    img_data = q1.get()
    s.sendall(img_data)
    res = s.recv(2048)
    res = res.decode('utf-8')
    logger.info(res)
    q2.put(res)

    resp = Thread(target=resp_to_user())
    resp.start()


def resp_to_user():
    global chat_id
    msg = q2.get()
    bot.send_message(chat_id, msg)



if __name__ == "__main__":
    updater = Updater("xxx", use_context=True)
    dispatcher = updater.dispatcher
    bot = telegram.Bot("xxx")
    q1 = Queue()
    q2 = Queue()

    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CommandHandler('help', help))
    dispatcher.add_handler(MessageHandler(Filters.text, general_and_getlink))
    dispatcher.add_handler(MessageHandler(Filters.photo, get_photo))
    updater.start_polling()
    updater.idle()
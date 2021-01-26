import logging
from flask import Flask, request
from dotenv import load_dotenv
import os
from telegram.ext import Updater, CommandHandler
from telegram.ext import Dispatcher
from telegram.ext.callbackcontext import CallbackContext
from telegram.ext.filters import Filters
from telegram.ext.messagehandler import MessageHandler
from telegram.update import Update
from telegram import Bot, ReplyKeyboardMarkup
from utils import fetch_news, get_reply, topics_keyboard

# enabling logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

# loading the Token
load_dotenv()
TOKEN = os.getenv("TOKEN")
app = Flask(__name__)


@app.route("/")
def index():
    return "Hello World"


@app.route(f"/{TOKEN}", methods=['GET', 'POST'])
def webhook():
    update = Update.de_json(request.get_json(), bot)
    dp.process_update(update)
    return "Webhook SetUp complete."


# function to reply to the /start message
def start(update: Update, context: CallbackContext):
    # print(update)
    author = update.message.from_user.first_name
    reply = f"Hi {author}"
    bot.send_message(chat_id=update.message.chat_id, text=reply)


def _help(update: Update, context: CallbackContext):
    help_text = """
    Hey, this is the Help Center.\n
    You can ask the me to show you news from anywhere.
    Example: 'Show me Sports News from India in Hindi'
    Will show you Sports news from India in Hindi Language
    """
    bot.send_message(chat_id=update.message.chat_id, text=help_text)


def news(update: Update, context: CallbackContext):
    bot.send_message(chat_id=update.message.chat_id, text="Choose a Category:",
                     reply_markup=ReplyKeyboardMarkup(keyboard=topics_keyboard, one_time_keyboard=True))


def error(update: Update, context: CallbackContext):
    logger.error(f"Update {update} has caused Error: {update.error}")


def reply(update: Update, context: CallbackContext):
    intent, reply = get_reply(update.message.text, update.message.chat_id)

    if(intent == "get_news"):
        articles = fetch_news(reply)
        for article in articles:
            bot.send_message(chat_id=update.message.chat_id,
                             text=article['link'])
    else:
        bot.send_message(chat_id=update.message.chat_id, text=reply)


bot = Bot(TOKEN)
try:
    bot.set_webhook("https://676df01c7e24.ngrok.io/" + TOKEN)
except Exception as e:
    print(e)

dp = Dispatcher(bot, None)
dp.add_handler(CommandHandler("start", start))
dp.add_handler(CommandHandler("help", _help))
dp.add_handler(CommandHandler("news", news))
dp.add_handler(MessageHandler(Filters.text, reply))

if __name__ == "__main__":

    app.run(port=8443)

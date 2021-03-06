from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging
import os
import json
from dotenv import load_dotenv, find_dotenv
import telebot

logger = logging.getLogger('sd')


def start(bot, update):
    update.message.reply_text('Hi!')

def help(bot, update):
    update.message.reply_text('Help!')

def echo(bot, update):
    client_credentials = json.load(open(os.environ['GOOGLE_APPLICATION_CREDENTIALS']))
    project_id = client_credentials['project_id']
    session_id = update.message.chat_id
    answer = detect_intent_texts(project_id, session_id, update.message.text, 'ru')
    update.message.reply_text(answer)

def error(bot, update, error):
    logger.warning('Update "%s" caused error "%s"', update, error)

def detect_intent_texts(project_id, session_id, text, language_code):
    from google.cloud import dialogflow

    session_client = dialogflow.SessionsClient()

    session = session_client.session_path(project_id, session_id)
    text_input = dialogflow.TextInput(text=text, language_code=language_code)
    query_input = dialogflow.QueryInput(text=text_input)
    response = session_client.detect_intent(
        request={"session": session, "query_input": query_input}
    )

    return response.query_result.fulfillment_text

def main():
    """Start the bot."""
    tg_bot = telebot.TeleBot(os.environ['TOKEN_LOGGER_BOT'])
    chat_id = os.environ['CHAT_ID']
    class TelegramLogsHandler(logging.Handler):

        def __init__(self, tg_bot, chat_id):
            super().__init__()
            self.chat_id = chat_id
            self.tg_bot = tg_bot

        def emit(self, record):
            log_entry = self.format(record)
            self.tg_bot.send_message(chat_id=self.chat_id, text=log_entry)

    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
    logger.setLevel(logging.INFO)
    logger.addHandler(TelegramLogsHandler(tg_bot, chat_id))
    logger.info("?????? ???? ????????????????????")

    # Create the EventHandler and pass it your bot's token.
    load_dotenv(find_dotenv())
    token_tg_publ = os.environ['TOKEN_TG_PUBL']
    updater = Updater(token_tg_publ)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, echo))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()

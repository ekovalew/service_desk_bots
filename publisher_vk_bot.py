import random
import json
import os
import vk_api as vk
from vk_api.longpoll import VkLongPoll, VkEventType
import requests
import time
import logging
import telebot


logger = logging.getLogger('sd')

def echo(event, vk_api):
    client_credentials = json.load(open(os.environ['GOOGLE_APPLICATION_CREDENTIALS']))
    project_id = client_credentials['project_id']
    session_id = event.user_id
    answer = detect_intent_texts(project_id, session_id, event.text, 'ru')
    if answer:
        vk_api.messages.send(
            user_id=event.user_id,
            message=answer,
            random_id=random.randint(1,1000)
        )

def detect_intent_texts(project_id, session_id, text, language_code):
    from google.cloud import dialogflow

    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, session_id)

    text_input = dialogflow.TextInput(text=text, language_code=language_code)

    query_input = dialogflow.QueryInput(text=text_input)

    response = session_client.detect_intent(
        request={"session": session, "query_input": query_input}
    )

    if not response.query_result.intent.is_fallback:
        return response.query_result.fulfillment_text

def main():
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

    logger.setLevel(logging.INFO)
    logger.addHandler(TelegramLogsHandler(tg_bot, chat_id))
    logger.info("Бот ВК запустился")

    token = os.environ['TOKEN_VK']
    vk_session = vk.VkApi(token=token)
    vk_api = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            try:
                echo(event, vk_api)
            except requests.exceptions.ReadTimeout:
                continue
            except requests.exceptions.ConnectionError:
                time.sleep(30)
            except requests.exceptions.HTTPError:
                time.sleep(60)

if __name__ == "__main__":
    main()

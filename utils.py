import os
import dialogflow_v2 as dialogflow
from dotenv import load_dotenv
from gnewsclient import gnewsclient

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "client.json"

# creating the dialogflow session
dialogflow_sesiion_client = dialogflow.SessionsClient()
load_dotenv()
PROJECT_ID = os.getenv("PROJECT_ID")

# creating the News client
client = gnewsclient.NewsClient()

# function to detect the intent from the message


def detect_intent_from_text(text, session_id, language_code='en'):
    session = dialogflow_sesiion_client.session_path(
        project=PROJECT_ID, session=session_id)
    text_input = dialogflow.types.TextInput(
        text=text, language_code=language_code)
    query_input = dialogflow.types.QueryInput(text=text_input)
    response = dialogflow_sesiion_client.detect_intent(
        session=session, query_input=query_input)
    return response.query_result


# function to get the reply
def get_reply(query, chat_id):
    response = detect_intent_from_text(query, chat_id)

    if response.intent.display_name == "get_news":
        return "get_news", dict(response.parameters)
    else:
        return "small_talk", response.fulfillment_text


# function to fetch news from Gnewsclient
def fetch_news(parameters):
    client.language = parameters.get("language")
    client.topic = parameters.get("news_topic")
    client.location = parameters.get("geo-country")

    return client.get_news()[:5]


# Keyboard Markup
topics_keyboard = [
    ['Top Stories', 'World', 'Nation'],
    ['Business', 'Technology', 'Entertainment'],
    ['Sports', 'Science', 'Health']
]

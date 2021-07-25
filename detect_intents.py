import logging

from google.cloud import dialogflow


logger = logging.getLogger('intents')


def detect_intent_texts(project_id, session_id, text, language_code):
    try:
        session_client = dialogflow.SessionsClient()
        session = session_client.session_path(project_id, session_id)

        text_input = dialogflow.TextInput(text=text, language_code=language_code)
        query_input = dialogflow.QueryInput(text=text_input)

        response = session_client.detect_intent(
            request={"session": session, "query_input": query_input}
        )
        query_result = response.query_result
    except ConnectionError:
        logger.error('Lost connection to Google Cloud')
    return query_result.fulfillment_text, query_result.intent.is_fallback

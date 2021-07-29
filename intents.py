import argparse
import json
import os

from dotenv import load_dotenv
from google.cloud import dialogflow


def detect_intent_texts(project_id, session_id, text, language_code):
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, session_id)

    text_input = dialogflow.TextInput(text=text, language_code=language_code)
    query_input = dialogflow.QueryInput(text=text_input)

    response = session_client.detect_intent(
        request={"session": session, "query_input": query_input}
    )
    query_result = response.query_result
    return query_result.fulfillment_text, query_result.intent.is_fallback


def create_intent(project_id, display_name,
                  training_phrases_parts, message_texts):
    intents_client = dialogflow.IntentsClient()

    parent = dialogflow.AgentsClient.agent_path(project_id)
    training_phrases = []
    for training_phrases_part in training_phrases_parts:
        part = dialogflow.Intent.TrainingPhrase.Part(
            text=training_phrases_part)

        training_phrase = dialogflow.Intent.TrainingPhrase(parts=[part])
        training_phrases.append(training_phrase)

    text = dialogflow.Intent.Message.Text(text=message_texts)
    message = dialogflow.Intent.Message(text=text)

    intent = dialogflow.Intent(
        display_name=display_name,
        training_phrases=training_phrases,
        messages=[message]
    )

    intents_client.create_intent(request={"parent": parent, "intent": intent})


def get_training_phrases(filepath):
    with open(filepath, 'r', encoding='utf-8') as file:
        return json.load(file)


def create_parser():
    parser = argparse.ArgumentParser(
        description='Creates intents for DialogFlow Google Cloud',
    )
    parser.add_argument(
        'filepath',
        help='Path to json file containing intents',
        type=str,
    )
    return parser


def main():
    load_dotenv()

    project_id = os.getenv('GOOGLE_CLOUD_PROJECT_ID')

    parser = create_parser()
    arguments = parser.parse_args()

    intents = get_training_phrases(arguments.filepath)

    for intent_name, intent_content in intents.items():
        questions, answer = intent_content['questions'], intent_content['answer']
        create_intent(project_id, intent_name, questions, [answer])


if __name__ == '__main__':
    main()

import argparse
import json
import logging
import os

from dotenv import load_dotenv
from google.cloud import dialogflow
from google.api_core.exceptions import InvalidArgument


logger = logging.getLogger('intents')
logging.basicConfig(filename='intents.log', level=logging.INFO)


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

    response = intents_client.create_intent(
        request={"parent": parent, "intent": intent}
    )

    logger.debug("Intent created: {}".format(response))


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
    filepath = arguments.filepath

    intents = get_training_phrases(filepath)

    for intent_name, intent_content in intents.items():
        try:
            questions, answer = intent_content['questions'], intent_content['answer']
            create_intent(project_id, intent_name, questions, [answer])
        except KeyError:
            logger.exception('Wrong json key')
        except ConnectionError:
            logger.exception('Lost connection to Google Cloud')
        except InvalidArgument:
            logger.exception(f'Intent {intent_name} already exists')


if __name__ == '__main__':
    main()

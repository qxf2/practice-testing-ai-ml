"""
Figure out if a message sent is a PTO or not
"""
import os
import pickle
import re

CURRENT_DIRECTORY = os.path.dirname(__file__)
MODEL_FILENAME = os.path.join(CURRENT_DIRECTORY, 'pto_classifier.pickle')
QUERIES_FILENAME = os.path.join(CURRENT_DIRECTORY,'queries.log')

def get_clean_message(message):
    "Clean the message"
    cleaned_message = re.sub(r'<.*</.*?>', '', message) #quoted message
    cleaned_message = re.sub(r'\B@\w+', '', cleaned_message) #@mentions
    cleaned_message = re.sub(r'&.*?;', '', cleaned_message) #encoded strings
    cleaned_message = re.sub(r'^(\s)*$\n', '', cleaned_message) #emtpy lines
    cleaned_message = cleaned_message.replace('<legacyquote>', '')
    cleaned_message = cleaned_message.replace(',', '')
    cleaned_message = cleaned_message.replace('.', '')
    cleaned_message = cleaned_message.replace('"', '')
    cleaned_message = cleaned_message.replace("'", '')
    cleaned_message = cleaned_message.replace('\\', '')

    return cleaned_message

def is_this_a_pto(message):
    "Return a prediction of whether this is a PTO or not"
    model = pickle.load(open(MODEL_FILENAME, 'rb'))
    message = get_clean_message(message)
    with open(QUERIES_FILENAME,'a') as file_handler:
        file_handler.write(message + "\n")

    return model.predict([message])[0]

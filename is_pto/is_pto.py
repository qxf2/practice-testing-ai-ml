"""
Figure out if a message sent is a PTO or not
"""
import os
import pickle
import re
import preprocess_message

CURRENT_DIRECTORY = os.path.dirname(__file__)
MODEL_FILENAME = os.path.join(CURRENT_DIRECTORY, 'pto_classifier.pickle')
QUERIES_FILENAME = os.path.join(CURRENT_DIRECTORY,'queries.log')

def is_this_a_pto(message):
    "Return a prediction of whether this is a PTO or not"
    model = pickle.load(open(MODEL_FILENAME, 'rb'))
    message = preprocess_message.get_clean_message(message)
    with open(QUERIES_FILENAME,'a') as file_handler:
        file_handler.write(message + "\n")

    return model.predict([message])[0]

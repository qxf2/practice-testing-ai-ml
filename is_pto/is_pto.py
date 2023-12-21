"""
Figure out if a message sent is a PTO or not and show the explanations for the prediction
"""
import os
import pickle
import re
import is_pto.preprocess_message as message_cleaner
from lime.lime_text import LimeTextExplainer

CURRENT_DIRECTORY = os.path.dirname(__file__)
MODEL_FILENAME = os.path.join(CURRENT_DIRECTORY, 'pto_classifier.pickle')
QUERIES_FILENAME = os.path.join(CURRENT_DIRECTORY,'queries.log')

def get_model():
    "Return the model"
    return pickle.load(open(MODEL_FILENAME, 'rb'))

def store_message(message):
    "Store the input message to file for analysis at a later time"
    with open(QUERIES_FILENAME,'a') as file_handler:
        file_handler.write(message + "\n")

def is_this_a_pto(message):
    "Return a prediction of whether this is a PTO or not"
    answer = 0
    model = get_model()
    if len(message.strip().split()) == 1:
        answer = 0
    else:
        message = message_cleaner.get_clean_message(message)
        store_message(message)
        answer = model.predict([message])[0]

    return answer

def lime_explainer(message):   
    "Return the Lime explanations" 
    class_names = ['0', '1']
    model = get_model()
    message = message_cleaner.get_clean_message(message)    
    explainer = LimeTextExplainer(class_names=class_names)    
    exp = explainer.explain_instance(message, model.predict_proba, num_features=50, num_samples=100)
   
    return exp

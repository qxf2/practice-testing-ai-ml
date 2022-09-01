"""
Figure out if a message sent is a PTO or not
"""
import os
import pickle
import re
#import is_pto.preprocess_message as message_cleaner
#from memory_profiler import profile

import re
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer
NOT_STOP_WORDS = ['not','off','be','will','before','after','out']
ADD_STOP_WORDS = ['today', 'tomorrow', 'yesterday']

CURRENT_DIRECTORY = os.path.dirname(__file__)
MODEL_FILENAME = os.path.join(CURRENT_DIRECTORY, 'pto_classifier.pickle')
QUERIES_FILENAME = os.path.join(CURRENT_DIRECTORY,'queries.log')

def clean_sqs_skype_formatting(message):
    "Clean up unwanted Skype and SQS formatting"
    cleaned_message = re.sub(r'<quote.*</quote>', '', message)
    cleaned_message = re.sub(r'<.*</.*?>', '', cleaned_message) #quoted message
    cleaned_message = re.sub(r'\B@\w+', '', cleaned_message) #@mentions
    cleaned_message = re.sub(r'&.*?;', '', cleaned_message) #encoded strings
    cleaned_message = re.sub(r'^(\s)*$\n', '', cleaned_message) #emtpy lines
    cleaned_message = cleaned_message.replace('<legacyquote>', '')
    cleaned_message = cleaned_message.replace(',', ' ')
    cleaned_message = cleaned_message.replace('.', ' ')
    cleaned_message = cleaned_message.replace('"', ' ')
    cleaned_message = cleaned_message.replace("'", ' ')
    cleaned_message = cleaned_message.replace('\\', ' ')

    return cleaned_message

def preprocess_message(message):
    "Preprocess the message"
    stemmer = SnowballStemmer('english')
    words = stopwords.words("english")
    for word in NOT_STOP_WORDS:
        words.remove(word)
    for word in ADD_STOP_WORDS:
        words.append(word)
    clean_message = " ".join([stemmer.stem(i) for i in re.sub("[^a-zA-Z]", " ", message).split() if i not in words]).lower()

    return clean_message

def get_clean_message(message):
    "Clean the message"
    message = clean_sqs_skype_formatting(message)
    message = preprocess_message(message)

    return message

def get_model():
    "Return the model"
    return pickle.load(open(MODEL_FILENAME, 'rb'))

def store_message(message):
    "Store the input message to file for analysis at a later time"
    with open(QUERIES_FILENAME,'a') as file_handler:
        file_handler.write(message + "\n")

@profile
def is_this_a_pto(message):
    "Return a prediction of whether this is a PTO or not"
    answer = 0
    model = get_model()
    if len(message.strip().split()) == 1:
        answer = 0
    else:
        message = get_clean_message(message)
        store_message(message)
        answer = model.predict([message])[0]
    return answer


if __name__=='__main__':
    ans = is_this_a_pto('I am taking PTO tomorrow')
    print(f'\nANSWER : {ans}\n')
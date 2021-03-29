"""
Preprocess incoming message to match what the training model uses
a) Clean the unwanted portions of the Skype message and SQS formatting
b) Mimic the training model - remove stop words and stem the words
"""
import re
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer
NOT_STOP_WORDS = ['not','off','be','will','before','after','out']
ADD_STOP_WORDS = ['today', 'tomorrow', 'yesterday']

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

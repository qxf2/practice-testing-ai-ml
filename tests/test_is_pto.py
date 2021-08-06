import os,sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from is_pto.preprocess_message import clean_sqs_skype_formatting
from is_pto.preprocess_message import preprocess_message
from is_pto.preprocess_message import get_clean_message
from is_pto.is_pto import is_this_a_pto

def test_clean_sqs_skype_formatting():
    "Test to check if if we get message cleaned"
    message = "I am 'on' pto"
    result = clean_sqs_skype_formatting(message)
    assert result == "I am  on  pto"

def test_preprocess_message():
    "Test to check message get cleaned"
    message = "I am on PTO today"
    result = preprocess_message(message)
    assert result == "i pto"

def test_clean_message():
    "Test to check clean_message function"
    message = "  I am  on,PTO"
    result = get_clean_message(message)
    assert result == "i pto"

def test_is_this_a_pto():
    "Test to check whether message is a pto message or not"
    message = "I am on PTO today"
    result = is_this_a_pto(message)
    assert result == 0
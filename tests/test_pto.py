import os,sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from unittest import mock
from is_pto import is_pto
import pytest

@mock.patch('is_pto.preprocess_message.get_clean_message')
def test_actual_pto_message(mock_clean_message):
    # Testing the actual PTO message
    message = "I am sick"
    #it returns a desired value as response to the patched method.
    mock_clean_message.return_value = message #what is message getting here? we are assigning returnvalue = 1 or message itself?
    result = is_pto.is_this_a_pto(message) #what is message getting here?
    #I dont understand the order of what is happening here
    assert result == 1
    assert mock_clean_message.call_count == 1

@mock.patch('is_pto.preprocess_message.get_clean_message')
def test_non_pto_message(mock_clean_message):
    # Testing a non-PTO message
    message = "Good morning"
    mock_clean_message.return_value = message
    result = is_pto.is_this_a_pto(message)
    assert result == 0    
    assert mock_clean_message.call_count == 1    
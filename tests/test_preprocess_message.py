"""
Unit test for testing fix for markdown message
"""
import unittest
from unittest.mock import patch
import os,sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from is_pto.preprocess_message import clean_sqs_skype_formatting


def test_cleaned_message():

    cleaned_sqs_skype_formatting = clean_sqs_skype_formatting('<I am on PTO today>')
    assert cleaned_sqs_skype_formatting == ''

    cleaned_sqs_skype_formatting = clean_sqs_skype_formatting('<I am on PTO today>I will take PTO on 23rd March')
    assert cleaned_sqs_skype_formatting == 'I will take PTO on 23rd March'
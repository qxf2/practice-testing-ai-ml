"""
Unit tests for is_this_a_pto method in is_pto
"""

from unittest.mock import Mock, patch
import is_pto.is_pto

@patch('is_pto.is_pto.is_this_a_pto') 
def test_is_pto(mock_is_this_a_pto):
    # Configure the mock to return a value of 1
    message = "I am sick"
    mock_is_this_a_pto.return_value = 1    
    result = is_pto.is_pto.is_this_a_pto(message)
    assert mock_is_this_a_pto.call_count == 1
       
@patch('is_pto.is_pto.is_this_a_pto') 
def test_not_a_pto(mock_is_this_a_pto):
    # Configure the mock to return a value of 0
    message = "Good Morning"
    mock_is_this_a_pto.return_value = 0
    result = is_pto.is_pto.is_this_a_pto(message)
    assert result == 0
    assert mock_is_this_a_pto.call_count == 1
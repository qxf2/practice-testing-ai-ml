"""
Unit tests for is_pto method in ai_ml_app.py. 
This test verifies the response status code and score for the given sample PTO messages
"""
import requests
from parameterized import parameterized_class

@parameterized_class(("url","message", "score", "expected_status_code"), 
[
  ("https://practice-testing-ai-ml.qxf2.com/is-pto","I am not well today I am Sick", 1, 200),
  ("https://practice-testing-ai-ml.qxf2.com/is-pto","I am leaving now will see you day after tomorrow", 0, 200)
])

class Testispto(object):
    """
    Test class for is pto method
    """
    #@responses.activate
    def test_unit_is_pto(self):
        """
        Unit test for the pto message and score
        """
        response = requests.post(self.url, data={"message":self.message})
        print ("PTO messages that were tested and the corresponding score:",(response.text))
        assert response.status_code == self.expected_status_code
        assert response.json()['score'] == self.score

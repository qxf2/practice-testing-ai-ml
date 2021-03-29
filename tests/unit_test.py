"""
Unit tests for get_is_pto method of pto_detector lambda
"""
import requests
from parameterized import parameterized_class

@parameterized_class(("url", "message", "score", "expected_status_code"), [
   ("http://localhost:6464/is-pto","<quote author=-smitha.ryc- authorname=-Smitha Rajesh- timestamp=-1609737742- conversation=-19:f33e901e871d4c3c9ebbbbee66e59ebe@thread.skype- messageid=-1609737741739- cuid=-4887239365922773121->I have been sick for the past few days, going to take off today", 0, 200),
   ("http://localhost:6464/is-pto","I am on PTO today", 1, 200),
])

class Testgetispto(object):
    """
    Test class for get is pto method
    """
    #@responses.activate
    def test_unit_get_is_pto_score(self):
        """
        Unit test for pto_score
        """
        resp = requests.post(self.url, data={"message":self.message})
        assert resp.status_code == self.expected_status_code
        assert resp.json()['score'] == self.score
#-*- encoding: UTF-8 -*-

"""Unit tests for API """

#---------------------------------import---------------------------------------
import unittest
import API
import redis
import json
#------------------------------------------------------------------------------


class TestAPI(unittest.TestCase):
    """Tests for APT.py."""

    def setUp(self):
        """Find the first user_id in zset"""
        self.api = API.ZhihuApi()
        self.r = self.api.r
        for i in range(0, 10000):
            if self.r.zcard(str(i) + ':timeline'):
                self.user_id = str(i)
                break
        self.test_user_timeline()
        self.user_timeline = json.loads(self.api.user_timeline(self.user_id, 0, 10))
        self.question_id = self.user_timeline[0]['question_id']
        self.unix_time = self.user_timeline[0]['unix_time']

    def test_user_timeline(self):
        self.assertTrue(self.api.user_timeline('123', 1, 100))
        self.assertTrue(self.api.user_timeline('123', 1, -100))
        self.assertTrue(self.api.user_timeline('123', -1, 100))
        self.assertTrue(self.api.user_timeline('123', 0, 0))
        self.assertTrue(self.api.user_timeline(123, 1, 100))
        self.assertTrue(self.api.user_timeline(self.user_id, 0, 10))
        self.assertEqual(json.dumps({'r': '0'}), self.api.user_timeline('-1', 0, 10))

    def test_if_hide_question(self):
        """Test that the 'question_id' in zset and not in hide zset"""
        self.assertEqual(None, self.r.zscore(self.user_id + ':hide', self.question_id))

    def test_hide_question(self):
        self.assertTrue(self.api.hide_question(self.user_id, self.question_id))
        self.assertEqual(int(self.unix_time), self.r.zscore(self.user_id + ':hide', self.question_id))
        self.assertEqual(None, self.r.zscore(self.user_id + ':timeline', self.question_id))

    def test_display_question(self):
        self.assertTrue(self.api.display_question(self.user_id + ':timeline', self.question_id))
        self.assertEqual(self.question_id, json.loads(self.api.user_timeline(self.user_id, 0, 10))[0]['question_id'])
        self.assertEqual(None, self.r.zscore(self.user_id + ':hide', self.question_id))

    def test_if_display_question(self):
        """Test that the 'question' display and not in hide zset"""
        self.assertEqual(int(self.unix_time), self.r.zscore(self.user_id + ':timeline', self.question_id))
        self.assertEqual(None, self.r.zscore(self.user_id + ':hide', self.question_id))

if __name__ == '__main__':
    unittest.main()
###############################################################################

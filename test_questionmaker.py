from questionmaker import recr_ques

import unittest

class TestQuestionCreate(unittest.TestCase):
    def test_empty(self):
        #testing empty question and already present question
        self.assertEqual(recr_ques({},""),None)
        self.assertEqual(recr_ques({"How?":()},"How?"),None)
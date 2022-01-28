from bot_new import quering
from bot_new import predict
import numpy as np
import unittest

class TestQuestionQuering(unittest.TestCase):

    # test whether prediction type is float
    def test_predict_type(self):
        response1 = "Happy"
        self.assertIsInstance(predict(response1)[0][0],np.floating)
    
    # test whether prediction score lies between 0 and 1
    def test_predict_score(self):
        response1 = "Sad"
        response2 = "Happy"
        self.assertGreaterEqual(predict(response1),0)
        self.assertLessEqual(predict(response2),1)

    # test return type of querying function    
    def test_query_type(self):
        question = "How are you doing?"
        response = "Very depressed"
        self.assertIsInstance(quering(question,response),tuple)
        self.assertIsInstance(quering(question,response)[0],str)
        self.assertIsInstance(quering(question,response)[1][0][0],np.floating)
        self.assertIsInstance(quering("It was really nice talking to you and I hope that now you feel better after talking to me. Best of luck for your future endeavours. Bye!","Thanks")[0],type(None))

    # test whether correct response score is geneerated
    def test_score(self):
        question = "How are you doing?"
        response1 = "Very depressed"
        response2 = "Happy"
        self.assertLessEqual(quering(question,response1)[1],0.55)
        self.assertGreaterEqual(quering(question,response2)[1],0.5)

    # test whether function raises keyerror on incorrect input
    def test_query_error(self):
        question = "Something"
        response = "Nothing"
        self.assertRaises(KeyError,quering,question,response)


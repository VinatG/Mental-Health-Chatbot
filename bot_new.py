from __future__ import print_function
from gensim.parsing.preprocessing import strip_non_alphanum, preprocess_string
from gensim.corpora.dictionary import Dictionary
from keras.models import load_model
import numpy as np
import os
import subprocess
import pickle

try:
    model = load_model('SentimentAnalysis/model_nn.h5') #load the trained model
except IOError:
    if 'model_nn.tar.gz' not in os.listdir('SentimentAnalysis'):
        raise IOError("Could not find Sentiment Analysis model. Ensure model "\
                      "is present in: ./SentimentAnalysis")
    else:
        process = subprocess.Popen("cd SentimentAnalysis/; "\
                                   "tar -zxf model_nn.tar.gz; cd ..",
                                   shell=True, stdout=subprocess.PIPE)
        process.wait()
        model = load_model('SentimentAnalysis/model_nn.h5') 
vocab = Dictionary.load('SentimentAnalysis/vocab_sentiment')

# The score for the response is generated
def predict(text):
    preprocessed = [word[:-3] if word[-3:] == 'xxx' else word for word in
                    preprocess_string(text.lower().replace('not', 'notxxx'))]
    txt_list = [(vocab.token2id[word] + 1) for word in preprocessed
                if word in vocab.token2id.keys()]
    txt_list = [txt_list]
    max_tweet_len = 20
    if len(txt_list[0]) < max_tweet_len:
        for i in range(max_tweet_len - len(txt_list[0])):
            txt_list[0].append(0)
    elif len(txt_list[0]) > max_tweet_len:
        while len(txt_list[-1]) > max_tweet_len:
            txt_list.append(txt_list[-1][max_tweet_len:])
            txt_list[-2] = txt_list[-2][:max_tweet_len]
    prediction = 0
    for txt in txt_list:
        prediction += model.predict(np.array([txt]), batch_size=1)
    prediction /= len(txt_list)
    return prediction


with open('questiondict_newcopy.pickle','rb') as file: #load the question dictionary
    quer_resp = pickle.load(file)

#The next question and score is generated for the current question and response
def quering(question,response):
    if question in quer_resp: 
        if quer_resp[question][0] != "": 
            T_resp_score,Tquestion,Fquestion = quer_resp[question]
            res_score = predict(response) #the query response score is generated
            if res_score > T_resp_score:
                return (Tquestion,res_score)
            else:
                return (Fquestion,res_score)
        else:
            return (None,0)
    else:
        raise KeyError("Question not found in dictionary")
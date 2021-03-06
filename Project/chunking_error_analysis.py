# -*- coding: utf-8 -*-
"""Chunking_error_analysis.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1IKxIL4WtL6be3l9wpYzeDFVqBQEYessE
"""

import pickle
from collections import defaultdict,OrderedDict
import numpy as np
import matplotlib.pyplot as plt
import itertools
from nltk.corpus import conll2000
import pandas as pd
from pandas_profiling import ProfileReport
import seaborn as sns

TEST_TRAIN_DF_SPLIT_FACTOR = 8937
'''
Reading data into data frame
'''
df_train = pd.read_csv('train.txt', sep=" ",header=None,skip_blank_lines=False, names=['train_word','POS_tag_train','Chunk_tag'])
df_test = pd.read_csv('test.txt', sep=" ",header=None,skip_blank_lines=False, names=['test_word','POS_tag_test','Chunk_tag'])

# prof = ProfileReport(df_train)
# prof.to_file(output_file='train.html')
# prof = ProfileReport(df_test)
# prof.to_file(output_file='test.html')
# df_train['POS_tag_train'].hist(bins= 44,xrot=90,legend= True)
# df_test['POS_tag_test'].hist(bins= 44,xrot=90,legend = True)

# df_train['train_word'].hist(bins= 44,xrot=90,legend= True)
# df_test['test_word'].hist(bins= 44,xrot=90,legend = True)

with open('MEMM_actual_tags.pkl', 'rb') as f:
    MEMM_actual = pickle.load(f)
with open('MEMM_predicted_tags.pkl', 'rb') as f:
    MEMM_predicted = pickle.load(f)

with open('MEMM_test_X.pkl', 'rb') as f: # Will be same for all models
    MEMM_X = pickle.load(f)
    
with open('MEMM_test_Y.pkl', 'rb') as f: # Will be same for all models
    MEMM_Y = pickle.load(f)
    
with open('MEMM_test_Y_pred.pkl', 'rb') as f: #Loading predicted values for MEMM
    MEMM_Y_pred = pickle.load(f)

with open('Bi_LSTM_test_Y_pred.pkl', 'rb') as f: #Loading predicted values for bi-LSTM
    BI_LSTM_Y_pred = pickle.load(f)

with open('test_predCRF_withO.pkl', 'rb') as f: #Loading predicted values for bi-LSTM
    CRF_Y_pred = pickle.load(f)

'''
Function to convert list to string
'''
def listToString(s):  

    str1 = " " 
    return (str1.join(s))



'''
Make a dictionary of occurances of test words
'''
word_count_dict = defaultdict(lambda: 0)
for i in range(0,len(MEMM_Y)):
    for j in range(0,len(MEMM_X[i])):
        word_count_dict[MEMM_X[i]['word'][j]] +=1
        
order_dict_word = {k: v for k, v in sorted(word_count_dict.items(), key=lambda item: item[1],reverse=True)}

'''
Make a dictionary of POS tags
'''

POS_count_dict = defaultdict(lambda: 0)
for i in range(0,len(MEMM_Y)):
    for j in range(0,len(MEMM_X[i])):
        POS_count_dict[MEMM_X[i]['POS_tag'][j]] +=1
        
order_dict_POS = {k: v for k, v in sorted(POS_count_dict.items(), key=lambda item: item[1],reverse=True)}

words = dict(itertools.islice(order_dict_word.items(),20))  
plt.rcParams.update({'font.size': 18})
plt.rcParams["figure.figsize"] = (20,10)
plt.title("Test set") 
plt.ylabel("Count of words") 
plt.xlabel("Word") 
plt.xticks(rotation=90)
plt.bar(words.keys(), words.values(), 0.5, color='b')

POS = dict(itertools.islice(order_dict_POS.items(),45))  
plt.title("Test set") 
plt.ylabel("Count of POS Tags") 
plt.xlabel("Tags") 
plt.xticks(rotation=90)
#plt.rcParams["figure.figsize"] = (20,3)
plt.bar(POS.keys(), POS.values(), 0.5, color='g')

counter_dict_word_MEMM = defaultdict(lambda: defaultdict(lambda:0))
average_mis_count_MEMM = defaultdict(lambda: defaultdict(lambda:0))
'''
Check the words mis-tagged for MEMM . Uncomment print lines to see context
'''
for i in range(0,len(MEMM_Y)):
    l = False
    for j in range(len(MEMM_Y[i])):
        if ( MEMM_Y[i][j] == 'I' and MEMM_Y_pred[i][j]=='O'):
            #if(MEMM_X[i]['word'][j] == 'to'):
            #print("I-O",MEMM_X[i]['word'][j])
            counter_dict_word_MEMM['I-O'][MEMM_X[i]['word'][j]] +=1
            #print("CONTEXT =",list(MEMM_X[i]['word'][j-5:j+5]))
            #print("CONTEXT =",list(MEMM_X[i]['POS_tag'][j-5:j+5]))
            l= True
        if ( MEMM_Y[i][j] == 'B' and MEMM_Y_pred[i][j]=='I'):
            if(MEMM_X[i]['word'][j] == 'other'):
                print("B-I",MEMM_X[i]['word'][j])
                print("CONTEXT =",listToString(list(MEMM_X[i]['word'][j-8:j+8])))
                print("CONTEXT =",listToString(list(MEMM_X[i]['POS_tag'][j-8:j+8])))
                print("ACTUAL CHUNK=",listToString(list(MEMM_Y[i][j-8:j+8])))
                print("pred   CHUNK=",listToString(list(MEMM_Y_pred[i][j-8:j+8])))
            counter_dict_word_MEMM['B-I'][MEMM_X[i]['word'][j]] +=1
            
            l= True
        if ( MEMM_Y[i][j] == 'I' and MEMM_Y_pred[i][j]=='B'):
            #print("I-B",MEMM_X[i]['word'][j])
            counter_dict_word_MEMM['I-B'][MEMM_X[i]['word'][j]] +=1
            if(MEMM_X[i]['word'][j] == 'other'):
                print("I-B",MEMM_X[i]['word'][j])
                print("CONTEXT =",listToString(list(MEMM_X[i]['word'][j-8:j+8])))
                print("CONTEXT =",listToString(list(MEMM_X[i]['POS_tag'][j-8:j+8])))
                print("ACTUAL CHUNK=",listToString(list(MEMM_Y[i][j-8:j+8])))
                print("pred   CHUNK=",listToString(list(MEMM_Y_pred[i][j-8:j+8])))
                print()
            #print("CONTEXT =",list(MEMM_X[i]['word'][j-5:j+5]))
            #print("CONTEXT =",list(MEMM_X[i]['POS_tag'][j-5:j+5]))
            l= True
        if ( MEMM_Y[i][j] == 'B' and MEMM_Y_pred[i][j]=='O'):
            #print("B-O",MEMM_X[i]['word'][j])
            counter_dict_word_MEMM['B-O'][MEMM_X[i]['word'][j]] +=1
            #print("CONTEXT =",list(MEMM_X[i]['word'][j-5:j+5]))
            #print("CONTEXT =",list(MEMM_X[i]['POS_tag'][j-5:j+5]))
            l= True
        if ( MEMM_Y[i][j] == 'O' and MEMM_Y_pred[i][j]=='I'):
            #print("I-O",MEMM_X[i]['word'][j])
            counter_dict_word_MEMM['O-I'][MEMM_X[i]['word'][j]] +=1
            #print("CONTEXT =",list(MEMM_X[i]['word'][j-5:j+5]))
            #print("CONTEXT =",list(MEMM_X[i]['POS_tag'][j-5:j+5]))
            l= True
        if ( MEMM_Y[i][j] == 'O' and MEMM_Y_pred[i][j]=='B'):
            #print("I-O",MEMM_X[i]['word'][j])
            counter_dict_word_MEMM['O-B'][MEMM_X[i]['word'][j]] +=1
            #print("CONTEXT =",list(MEMM_X[i]['word'][j-5:j+5]))
            #print("CONTEXT =",list(MEMM_X[i]['POS_tag'][j-5:j+5]))
            l= True

for k,v in counter_dict_word_MEMM.items():
    for k1,v1 in counter_dict_word_MEMM[k].items():
        average_mis_count_MEMM[k][k1] = v1/counter_dict_word[k1]

counter_dict_word_CRF = defaultdict(lambda: defaultdict(lambda:0))
'''
Check the words mis-tagged for CRF . Uncomment print lines to see context
'''
for i in range(0,len(MEMM_Y)):
    l = False
    for j in range(len(MEMM_Y[i])-1):
        if ( MEMM_Y[i][j] == 'I' and CRF_Y_pred[i][j]=='O'):
            #print("I-O",MEMM_X[i]['word'][j])
            counter_dict_word_CRF['I-O'][MEMM_X[i]['word'][j]] +=1
            #print("CONTEXT =",list(MEMM_X[i]['word'][j-5:j+5]))
            #print("CONTEXT =",list(MEMM_X[i]['POS_tag'][j-5:j+5]))
            l= True
        if ( MEMM_Y[i][j] == 'B' and CRF_Y_pred[i][j]=='I'):
            #print("B-I",MEMM_X[i]['word'][j])
            counter_dict_word_CRF['B-I'][MEMM_X[i]['word'][j]] +=1

            #print("CONTEXT =",list(MEMM_X[i]['word'][j-5:j+5]))
            #print("CONTEXT =",list(MEMM_X[i]['POS_tag'][j-5:j+5]))
            l= True
        if ( MEMM_Y[i][j] == 'I' and CRF_Y_pred[i][j]=='B'):
            #print("I-B",MEMM_X[i]['word'][j])
            counter_dict_word_CRF['I-B'][MEMM_X[i]['word'][j]] +=1
            #print("CONTEXT =",list(MEMM_X[i]['word'][j-5:j+5]))
            #print("CONTEXT =",list(MEMM_X[i]['POS_tag'][j-5:j+5]))
            l= True
        if ( MEMM_Y[i][j] == 'B' and CRF_Y_pred[i][j]=='O'):
            #print("B-O",MEMM_X[i]['word'][j])
            counter_dict_word_CRF['B-O'][MEMM_X[i]['word'][j]] +=1
            #print("CONTEXT =",list(MEMM_X[i]['word'][j-5:j+5]))
            #print("CONTEXT =",list(MEMM_X[i]['POS_tag'][j-5:j+5]))
            l= True
        if ( MEMM_Y[i][j] == 'O' and CRF_Y_pred[i][j]=='I'):
            #print("I-O",MEMM_X[i]['word'][j])
            counter_dict_word_CRF['O-I'][MEMM_X[i]['word'][j]] +=1
            #print("CONTEXT =",list(MEMM_X[i]['word'][j-5:j+5]))
            #print("CONTEXT =",list(MEMM_X[i]['POS_tag'][j-5:j+5]))
            l= True
        if ( MEMM_Y[i][j] == 'O' and CRF_Y_pred[i][j]=='B'):
            #print("I-O",MEMM_X[i]['word'][j])
            counter_dict_word_CRF['O-B'][MEMM_X[i]['word'][j]] +=1
            #print("CONTEXT =",list(MEMM_X[i]['word'][j-5:j+5]))
            #print("CONTEXT =",list(MEMM_X[i]['POS_tag'][j-5:j+5]))
            l= True

counter_dict_pos_CRF = defaultdict(lambda: defaultdict(lambda:0))
average_mis_count_pos_CRF = defaultdict(lambda: defaultdict(lambda:0))
'''
Check the POS mis-tagged for CRF. Uncomment print lines to see context
'''
for i in range(0,len(MEMM_Y)):
    l = False
    for j in range(len(MEMM_Y[i])-1):
        if ( MEMM_Y[i][j] == 'I' and CRF_Y_pred[i][j]=='O'):
            #print("I-O",MEMM_X[i]['POS_tag'][j])
            counter_dict_pos_CRF['I-O'][MEMM_X[i]['POS_tag'][j]] +=1
            #print("CONTEXT =",list(MEMM_X[i]['word'][j-5:j+5]))
            #print("CONTEXT =",list(MEMM_X[i]['POS_tag'][j-5:j+5]))
            l= True
        if ( MEMM_Y[i][j] == 'B' and CRF_Y_pred[i][j]=='I'):
            #print("B-I",MEMM_X[i]['POS_tag'][j])
            counter_dict_pos_CRF['B-I'][MEMM_X[i]['POS_tag'][j]] +=1
            if(MEMM_X[i]['POS_tag'][j] == 'NN'):
                print("I-B",MEMM_X[i]['word'][j])
                print("CONTEXT =",listToString(list(MEMM_X[i]['word'][j-8:j+8])))
                print("CONTEXT =",listToString(list(MEMM_X[i]['POS_tag'][j-8:j+8])))
                print("ACTUAL CHUNK=",listToString(list(MEMM_Y[i][j-8:j+8])))
                print("pred   CHUNK=",listToString(list(MEMM_Y_pred[i][j-8:j+8])))
                print("pred   CHUNK=",listToString(list(CRF_Y_pred[i][j-8:j+8])))
                print("pred   CHUNK=",listToString(list(BI_LSTM_Y_pred[i][j-8:j+8])))
                print()
            #print("CONTEXT =",list(MEMM_X[i]['word'][j-5:j+5]))
            #print("CONTEXT =",list(MEMM_X[i]['POS_tag'][j-5:j+5]))
            l= True
        if ( MEMM_Y[i][j] == 'I' and CRF_Y_pred[i][j]=='B'):
            #print("I-B",MEMM_X[i]['POS_tag'][j])
            counter_dict_pos_CRF['I-B'][MEMM_X[i]['POS_tag'][j]] +=1
            if(MEMM_X[i]['POS_tag'][j] == 'NN'):
                print("I-B",MEMM_X[i]['word'][j])
                print("CONTEXT =",listToString(list(MEMM_X[i]['word'][j-8:j+8])))
                print("CONTEXT =",listToString(list(MEMM_X[i]['POS_tag'][j-8:j+8])))
                print("ACTUAL CHUNK=",listToString(list(MEMM_Y[i][j-8:j+8])))
                print("pred   CHUNK=",listToString(list(MEMM_Y_pred[i][j-8:j+8])))
                print("pred   CHUNK=",listToString(list(CRF_Y_pred[i][j-8:j+8])))
                print("pred   CHUNK=",listToString(list(BI_LSTM_Y_pred[i][j-8:j+8])))
                print()
            #print("CONTEXT =",list(MEMM_X[i]['word'][j-5:j+5]))
            #print("CONTEXT =",list(MEMM_X[i]['POS_tag'][j-5:j+5]))
            l= True
        if ( MEMM_Y[i][j] == 'B' and CRF_Y_pred[i][j]=='O'):
            #print("B-O",MEMM_X[i]['POS_tag'][j])
            counter_dict_pos_CRF['B-O'][MEMM_X[i]['POS_tag'][j]] +=1
            #print("CONTEXT =",list(MEMM_X[i]['word'][j-5:j+5]))
            #print("CONTEXT =",list(MEMM_X[i]['POS_tag'][j-5:j+5]))
            l= True
        if ( MEMM_Y[i][j] == 'O' and CRF_Y_pred[i][j]=='I'):
            #print("I-O",MEMM_X[i]['word'][j])
            counter_dict_pos_CRF['O-I'][MEMM_X[i]['POS_tag'][j]] +=1
            #print("CONTEXT =",list(MEMM_X[i]['word'][j-5:j+5]))
            #print("CONTEXT =",list(MEMM_X[i]['POS_tag'][j-5:j+5]))
            l= True
        if ( MEMM_Y[i][j] == 'O' and CRF_Y_pred[i][j]=='B'):
            #print("I-O",MEMM_X[i]['word'][j])
            counter_dict_pos_CRF['O-B'][MEMM_X[i]['POS_tag'][j]] +=1
            #print("CONTEXT =",list(MEMM_X[i]['word'][j-5:j+5]))
            #print("CONTEXT =",list(MEMM_X[i]['POS_tag'][j-5:j+5]))
            l= True

# for k,v in counter_dict_pos.items():
#     for k1,v1 in counter_dict_pos[k].items():
#         average_mis_count_pos_MEMM[k][k1] = v1/order_dict_POS[k1]

counter_dict_pos = defaultdict(lambda: defaultdict(lambda:0))
average_mis_count_pos_MEMM = defaultdict(lambda: defaultdict(lambda:0))
'''
Check the POS mis-tagged for MEMM. Uncomment print lines to see context
'''
for i in range(0,len(MEMM_Y)):
    l = False
    for j in range(len(MEMM_Y[i])):
        if ( MEMM_Y[i][j] == 'I' and MEMM_Y_pred[i][j]=='O'):
            #print("I-O",MEMM_X[i]['POS_tag'][j])
            counter_dict_pos['I-O'][MEMM_X[i]['POS_tag'][j]] +=1
            #print("CONTEXT =",list(MEMM_X[i]['word'][j-5:j+5]))
            #print("CONTEXT =",list(MEMM_X[i]['POS_tag'][j-5:j+5]))
            l= True
        if ( MEMM_Y[i][j] == 'B' and MEMM_Y_pred[i][j]=='I'):
            #print("B-I",MEMM_X[i]['POS_tag'][j])
            counter_dict_pos['B-I'][MEMM_X[i]['POS_tag'][j]] +=1
            #print("CONTEXT =",list(MEMM_X[i]['word'][j-5:j+5]))
            #print("CONTEXT =",list(MEMM_X[i]['POS_tag'][j-5:j+5]))
            l= True
        if ( MEMM_Y[i][j] == 'I' and MEMM_Y_pred[i][j]=='B'):
            #print("I-B",MEMM_X[i]['POS_tag'][j])
            counter_dict_pos['I-B'][MEMM_X[i]['POS_tag'][j]] +=1
            #print("CONTEXT =",list(MEMM_X[i]['word'][j-5:j+5]))
            #print("CONTEXT =",list(MEMM_X[i]['POS_tag'][j-5:j+5]))
            l= True
        if ( MEMM_Y[i][j] == 'B' and MEMM_Y_pred[i][j]=='O'):
            #print("B-O",MEMM_X[i]['POS_tag'][j])
            counter_dict_pos['B-O'][MEMM_X[i]['POS_tag'][j]] +=1
            #print("CONTEXT =",list(MEMM_X[i]['word'][j-5:j+5]))
            #print("CONTEXT =",list(MEMM_X[i]['POS_tag'][j-5:j+5]))
            l= True
        if ( MEMM_Y[i][j] == 'O' and MEMM_Y_pred[i][j]=='I'):
            #print("I-O",MEMM_X[i]['word'][j])
            counter_dict_pos['O-I'][MEMM_X[i]['POS_tag'][j]] +=1
            #print("CONTEXT =",list(MEMM_X[i]['word'][j-5:j+5]))
            #print("CONTEXT =",list(MEMM_X[i]['POS_tag'][j-5:j+5]))
            l= True
        if ( MEMM_Y[i][j] == 'O' and MEMM_Y_pred[i][j]=='B'):
            #print("I-O",MEMM_X[i]['word'][j])
            counter_dict_pos['O-B'][MEMM_X[i]['POS_tag'][j]] +=1
            #print("CONTEXT =",list(MEMM_X[i]['word'][j-5:j+5]))
            #print("CONTEXT =",list(MEMM_X[i]['POS_tag'][j-5:j+5]))
            l= True

for k,v in counter_dict_pos.items():
    for k1,v1 in counter_dict_pos[k].items():
        average_mis_count_pos_MEMM[k][k1] = v1/order_dict_POS[k1]

average_mis_count_pos_MEMM

counter_dict_word_lstm = defaultdict(lambda: defaultdict(lambda:0))
'''
Check the words mis-tagged for Bi-LSTM . Uncomment print lines to see context
'''
for i in range(0,len(MEMM_Y)):
    l = False
    for j in range(len(MEMM_Y[i])):
        if ( MEMM_Y[i][j] == 'I' and BI_LSTM_Y_pred[i][j]=='O'):
            #print("I-O",MEMM_X[i]['word'][j])
            counter_dict_word_lstm['I-O'][MEMM_X[i]['word'][j]] +=1
            #print("CONTEXT =",list(MEMM_X[i]['word'][j-5:j+5]))
            #print("CONTEXT =",list(MEMM_X[i]['POS_tag'][j-5:j+5]))
            l= True
        if ( MEMM_Y[i][j] == 'B' and BI_LSTM_Y_pred[i][j]=='I'):
            #print("B-I",MEMM_X[i]['word'][j])
            counter_dict_word_lstm['B-I'][MEMM_X[i]['word'][j]] +=1
            #print("CONTEXT =",list(MEMM_X[i]['word'][j-5:j+5]))
            #print("CONTEXT =",list(MEMM_X[i]['POS_tag'][j-5:j+5]))
            l= True
        if ( MEMM_Y[i][j] == 'I' and BI_LSTM_Y_pred[i][j]=='B'):
            #print("I-B",MEMM_X[i]['word'][j])
            counter_dict_word_lstm['I-B'][MEMM_X[i]['word'][j]] +=1
            #print("CONTEXT =",list(MEMM_X[i]['word'][j-5:j+5]))
            #print("CONTEXT =",list(MEMM_X[i]['POS_tag'][j-5:j+5]))
            l= True
        if ( MEMM_Y[i][j] == 'B' and BI_LSTM_Y_pred[i][j]=='O'):
            #print("B-O",MEMM_X[i]['word'][j])
            counter_dict_word_lstm['B-O'][MEMM_X[i]['word'][j]] +=1
            #print("CONTEXT =",list(MEMM_X[i]['word'][j-5:j+5]))
            #print("CONTEXT =",list(MEMM_X[i]['POS_tag'][j-5:j+5]))
            l= True
        if ( MEMM_Y[i][j] == 'O' and BI_LSTM_Y_pred[i][j]=='I'):
            #print("I-O",MEMM_X[i]['word'][j])
            counter_dict_word_lstm['O-I'][MEMM_X[i]['word'][j]] +=1
            #print("CONTEXT =",list(MEMM_X[i]['word'][j-5:j+5]))
            #print("CONTEXT =",list(MEMM_X[i]['POS_tag'][j-5:j+5]))
            l= True
        if ( MEMM_Y[i][j] == 'O' and BI_LSTM_Y_pred[i][j]=='B'):
            #print("I-O",MEMM_X[i]['word'][j])
            counter_dict_word_lstm['O-B'][MEMM_X[i]['word'][j]] +=1
            #print("CONTEXT =",list(MEMM_X[i]['word'][j-5:j+5]))
            #print("CONTEXT =",list(MEMM_X[i]['POS_tag'][j-5:j+5]))
            l= True

# return string    = defaultdict(lambda: defaultdict(lambda:0))
'''
Check the POS mis-tagged for bi-lstm. Uncomment print lines to see context
'''
for i in range(0,len(MEMM_Y)):
    l = False
    for j in range(len(MEMM_Y[i])):
        if ( MEMM_Y[i][j] == 'I' and BI_LSTM_Y_pred[i][j]=='O'):
            #print("I-O",MEMM_X[i]['POS_tag'][j])
            counter_dict_pos_lstm['I-O'][MEMM_X[i]['POS_tag'][j]] +=1
            #print("CONTEXT =",list(MEMM_X[i]['word'][j-5:j+5]))
            #print("CONTEXT =",list(MEMM_X[i]['POS_tag'][j-5:j+5]))
            l= True
        if ( MEMM_Y[i][j] == 'B' and BI_LSTM_Y_pred[i][j]=='I'):
            #print("B-I",MEMM_X[i]['POS_tag'][j])
            counter_dict_pos_lstm['B-I'][MEMM_X[i]['POS_tag'][j]] +=1
            #print("CONTEXT =",list(MEMM_X[i]['word'][j-5:j+5]))
            #print("CONTEXT =",list(MEMM_X[i]['POS_tag'][j-5:j+5]))
            l= True
        if ( MEMM_Y[i][j] == 'I' and BI_LSTM_Y_pred[i][j]=='B'):
            #print("I-B",MEMM_X[i]['POS_tag'][j])
            counter_dict_pos_lstm['I-B'][MEMM_X[i]['POS_tag'][j]] +=1
            #print("CONTEXT =",list(MEMM_X[i]['word'][j-5:j+5]))
            #print("CONTEXT =",list(MEMM_X[i]['POS_tag'][j-5:j+5]))
            l= True
        if ( MEMM_Y[i][j] == 'B' and BI_LSTM_Y_pred[i][j]=='O'):
            #print("B-O",MEMM_X[i]['POS_tag'][j])
            counter_dict_pos_lstm['B-O'][MEMM_X[i]['POS_tag'][j]] +=1
            #print("CONTEXT =",list(MEMM_X[i]['word'][j-5:j+5]))
            #print("CONTEXT =",list(MEMM_X[i]['POS_tag'][j-5:j+5]))
            l= True
        if ( MEMM_Y[i][j] == 'O' and BI_LSTM_Y_pred[i][j]=='I'):
            #print("I-O",MEMM_X[i]['word'][j])
            counter_dict_pos_lstm['O-I'][MEMM_X[i]['POS_tag'][j]] +=1
            #print("CONTEXT =",list(MEMM_X[i]['word'][j-5:j+5]))
            #print("CONTEXT =",list(MEMM_X[i]['POS_tag'][j-5:j+5]))
            l= True
        if ( MEMM_Y[i][j] == 'O' and BI_LSTM_Y_pred[i][j]=='B'):
            #print("I-O",MEMM_X[i]['word'][j])
            counter_dict_pos_lstm['O-B'][MEMM_X[i]['POS_tag'][j]] +=1
            #print("CONTEXT =",list(MEMM_X[i]['word'][j-5:j+5]))
            #print("CONTEXT =",list(MEMM_X[i]['POS_tag'][j-5:j+5]))
            l= True

'''
Build a sorted dictionary for words misclassified for plotting histogram in descending order for memm
'''
rebuilt_dict_word_MEMM        = defaultdict(list)
average_mis_count_MEMM_order  = defaultdict(list)
for k, v in counter_dict_word_MEMM.items():
    rebuilt_dict_word_MEMM[k] = OrderedDict(sorted(v.items(), key=lambda x: float(x[1]),reverse=True))
    
# for k, v in average_mis_count_MEMM.items():
#     average_mis_count_MEMM_order[k] = OrderedDict(sorted(v.items(), key=lambda x: float(x[1]),reverse=True))


'''
Build a sorted dictionary for words misclassified for plotting histogram in descending order for bi-lstm
'''
rebuilt_dict_word_bi_lstm = defaultdict(list)
for k, v in counter_dict_word_lstm.items():
    rebuilt_dict_word_bi_lstm[k] = OrderedDict(sorted(v.items(), key=lambda x: float(x[1]),reverse=True))

    
'''
Build a sorted dictionary for words misclassified for plotting histogram in descending order for CRF
'''
rebuilt_dict_word_crf = defaultdict(list)
for k, v in counter_dict_word_CRF.items():
    rebuilt_dict_word_crf[k] = OrderedDict(sorted(v.items(), key=lambda x: float(x[1]),reverse=True))

'''
Build a sorted dictionary for POS tagged word misclassified for plotting histogram in descending order for memm
'''
rebuilt_dict_pos_MEMM = defaultdict(list)
for k, v in counter_dict_pos.items():
    rebuilt_dict_pos_MEMM[k] = OrderedDict(sorted(v.items(), key=lambda x: float(x[1]),reverse=True))

'''
Build a sorted dictionary for POS tagged word misclassified for plotting histogram in descending order for bilstm
'''
rebuilt_dict_pos_bi_lstm = defaultdict(list)
for k, v in counter_dict_pos_lstm.items():
    rebuilt_dict_pos_bi_lstm[k] = OrderedDict(sorted(v.items(), key=lambda x: float(x[1]),reverse=True))    

'''
Build a sorted dictionary for POS tagged word misclassified for plotting histogram in descending order for CRF
'''
rebuilt_dict_pos_CRF = defaultdict(list)
for k, v in counter_dict_pos_CRF.items():
    rebuilt_dict_pos_CRF[k] = OrderedDict(sorted(v.items(), key=lambda x: float(x[1]),reverse=True))     
#rebuilt_dict_pos

out = dict(itertools.islice(rebuilt_dict_pos_MEMM['B-I'].items(),40))  #Change no of bars here
plt.title("POS misclassified as 'I' which should actually be 'B'") 
plt.ylabel("Count of misclassifications") 
plt.xlabel("POS misclassified") 
plt.xticks(rotation=90)
plt.bar(out.keys(), out.values(), 0.5, color='b')

out = dict(itertools.islice(rebuilt_dict_pos_MEMM['I-B'].items(),40))  
plt.title("POS misclassified as 'I' which should actually be 'B'") 
plt.ylabel("Count of misclassifications") 
plt.xlabel("POS misclassified") 
plt.xticks(rotation=90)
plt.bar(out.keys(), out.values(), 0.5, color='g')

plt.rcParams.update({'font.size': 18})
# out_memm = dict(itertools.islice(rebuilt_dict_word_MEMM['B-I'].items(),10))  
# #plt.subplot(2, 2, 3)
# plt.title("MEMM") 
# plt.ylabel("Count of misclassifications") 
# plt.xlabel("Words misclassified") 
# plt.xticks(rotation=90)
# plt.tight_layout()
# plt.bar(out_memm.keys(), out_memm.values(), 0.5, color='b')

# out_memm = dict(itertools.islice(rebuilt_dict_word_bi_lstm['B-I'].items(),10))
# #plt.subplot(2, 2, 1)
# plt.title("Bi-LSTM") 
# plt.ylabel("Count of misclassifications") 
# plt.xlabel("Words misclassified") 
# plt.xticks(rotation=90)
# plt.tight_layout()
# plt.bar(out_memm.keys(), out_memm.values(), 0.5, color='b')

out_memm = dict(itertools.islice(rebuilt_dict_pos_MEMM['B-O'].items(),12))
#plt.subplot(2,2,2)
plt.title("MEMM",fontsize=18) 
plt.ylabel("Count of misclassifications",fontsize=18) 
plt.xlabel("POS Tag",fontsize=18) 
plt.xticks(rotation=90,fontsize=18)
plt.tight_layout()
plt.bar(out_memm.keys(), out_memm.values(), 0.5, color='b')

out_lstm = dict(itertools.islice(rebuilt_dict_word_bi_lstm['B-I'].items(),30))  
plt.title("Words misclassified as 'I' which should actually be 'B' for Bi_LSTM") 
plt.ylabel("Count of misclassifications") 
plt.xlabel("Words misclassified") 
plt.xticks(rotation=90)
plt.bar(out_lstm.keys(), out_lstm.values(), 0.5, color='b')

out = dict(itertools.islice(rebuilt_dict_word_MEMM['I-B'].items(),15))
plt.title("Words misclassified as 'B' which should actually be 'I'") 
plt.ylabel("Count of misclassifications") 
plt.xlabel("Words misclassified")   
plt.xticks(rotation=90)
plt.bar(out.keys(), out.values(), 0.5, color='g')

"""**TODOS**

- Draw other histograms of all other combinations for words
- Draw other histograms of all other combinations for POS tags, should know which type of tag was misclassified how many times.
- No of times word occurs vs no of times misclassified
- No of times POS occurs vs no of times misclassified
- Sentences which were classified correctly and incorrectly containing these words (see context) and make a small list .Analyse which phrases, things,word window, pos window are classified incorrectly always, few times, rarely and list them seperately
- The word,POS plot should be compared for all three methods, the plots should be placed in the same graph for better view

- Also find common words /pos tags /sequence of mistakes common to all three models and model-specific mistakes

- Heap map for confusion matrices to be made for all three methods

- See paper for type of errors and classify according to that as well. 
"""


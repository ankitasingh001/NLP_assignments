The process of marking up the words in text(corpus) corresponding to a particular Part of Speech on the basis of its definition and context.
Example: Everything is all about Money.
Tagged Sentence: Everything_NN is_VBZ all_DT about_IN money_NN ._.

Here, we have done POS tagging via three models namely HMM, SVM and Bi-LSTM. 
HMM has been implemented from scratch. For more details refer to pdf uploaded along with the other contents.
The corpus used in the "Brown Corpus" available in nltk library.
The tagset used is the "Universal Tag-set"

All the 3 Models have been implemented on Python-3 Jupyter-Notebook .

Pre-requisites (packages) required to run all 3 :

(i)   nltk
(ii)  genism (for word2vec)
(iii) sklearn 
(iv)  Keras
(v)   pandas

The SVM and bi-LSTM classifiers take a long time to train, but the outputs we obtained are visible in the end section of the jupyter-notebook 

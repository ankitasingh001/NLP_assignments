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

POS Tagging via SVM,HMM and Bi-LSTM

Corpus Insights
# Sentences = 57340
# Tagged words = 1161192
# Average length of sentences = 20

General Comments
NOUN tags -> most significant
Some sentence lengths as long as 180
Mistakes in the corpus itself
Pre-defined universal tags used for classification

HMM-Analysis
Pre-processing
Conversion of all words except NOUNS to lower case
Addition of ^ and EOS tags for ease
Smoothing factor added

Observations
Selective lower casing gives a better accuracy than all other cases
A lot of misclassification related to noun-verb pair.
Also particles, adpositions
Mostly due to bigram modelling

HMM-Analysis
Per-POS Accuracy

Overall Accuracy = 94.94%

HMM-Analysis
Confusion Matrix

SVM-Analysis
Morphological features used:


SVM-Analysis
Processing and observations:
Word2vec dimension set to 50
Using stochastic gradient descent SVM gave lesser accuracy but faster results
Using rbf kernel on a subset gave better accuracies
Word similarity measures and window sizes played an important role for improving accuracies further
Adjectives and adverbs misclassified more often but particle classification accuracy significantly improved 



SVM-Analysis
Per-POS Accuracy

Overall Accuracy = 93.71%

SVM-Analysis
Confusion Matrix

Bi-LSTM Analysis
Processing and observations:
All words converted to lowercase- better accuracy
Embeddings of size 128 used, words padded to handle different lengths
Except for X, all accuracies significantly improved.
Takes longer to train
NOUN-VERB and PRT-ADP misclassification decreases significantly



Bi-LSTM Analysis
Per-POS Accuracy

Overall Accuracy = 97.07%

Bi-LSTM Analysis
Confusion Matrix
Overall tag comparison

General Comments
It took a few seconds to train HMM, but several hours for Bi-LSTM and SVM .
Few tags like pronouns, determiners and conjunctions are very well classified by all the models owing to less ambiguity in occurances.
X(other) tag precision and recall is less in all the models because of uncertain nature of the words.
Some common misclassifications are NOUN-VERB ,PRT-ADP,ADV-ADJ and NOUN-ADJ

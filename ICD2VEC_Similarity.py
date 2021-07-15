#!/usr/bin/env python
# coding: utf-8

# In[ ]:


#Loading the FastText model

from gensim.models import FastText as fText
from gensim.models.keyedvectors import KeyedVectors

model = KeyedVectors.load_word2vec_format('./wiki.en.vec')
model_words = list(model.wv.vocab)     #Loading the model words
model_bin = fText.load_fasttext_format("./wiki.en.bin")


# In[ ]:


#Converting query to vec

import numpy as np
from nltk import SnowballStemmer,word_tokenize
from nltk.corpus import stopwords

stop_words = stopwords.words('english')      #loading the stopwords
stemmer = SnowballStemmer("english")         #loading the stemmer

delimiter = [',', ':','!', '@','&','$','.','/',']','[']     #defining a set of delimeters

def query_to_vec(query):          #For converting query to one single vector
    tmp_vec = np.array([0]*300)   #Creating empty array of zeroes of 300 dimensions
    count = 0
    for word in word_tokenize(query):   #tokenizing the query
        word = word.lower()             #Converting word to its lower-case
        if word in delimiter:
            continue
        if(stemmer.stem(word) in model_words and stemmer.stem(word) not in delimiter):
            tmp_vec = tmp_vec + model.wv[stemmer.stem(word)]  #adding vector of the word by checking appropriate conditions
            count+=1
        elif(word in model_words and word not in delimiter):
            tmp_vec = tmp_vec + model.wv[word]
            count+=1
        elif(word not in delimiter):
            tmp_vec = tmp_vec + model_bin.wv[word]
            count+=1
            continue
        else:
            continue
    return tmp_vec/count       #returning average of the vector 


# In[ ]:


#For computing cosine similarity score

from scipy import spatial

def cos(v1, v2):
	result = 1 - spatial.distance.cosine(v1, v2)
	return result


# In[ ]:


import pickle
def load_obj(name ):                            #for loading the pickle file
    try:
        f = open(name + '.pkl', 'rb')
    except IOError:
        return None
    else:
        return pickle.load(f)
    
icd_vec = load_obj("parent_based_crawled_encoding_dup")


# In[ ]:


#For finding ICD codes related to the symptoms

query_vec = query_to_vec("Skin Itching")
ans_dict = dict()

for key, value in icd_vec.items():
    if(len(key)!=3):
        continue
    ans_dict[key] = cos(value, query_vec)


print(sorted(ans_dict, key=ans_dict.get, reverse=True)[:3])
    


# In[ ]:


#For finding ICD code as a combination of other ICD codes

query_icd_codes = ['I10','I25']
query_vec = np.array([0]*300)
for codes in query_icd_codes:
    query_vec = query_vec + icd_vec[codes]

query_vec = query_vec/len(query_icd_codes)
ans_dict = dict()

for key, value in icd_vec.items():
    if(len(key)!=3 or key in query_icd_codes):
        continue
    ans_dict[key] = cos(value, query_vec)


print(sorted(ans_dict, key=ans_dict.get, reverse=True)[:3])


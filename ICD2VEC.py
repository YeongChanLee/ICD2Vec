#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from gensim.models import FastText as fText
from gensim.models.keyedvectors import KeyedVectors

model = KeyedVectors.load_word2vec_format('./wiki.en.vec')   #Loading FastText model
model_words = list(model.wv.vocab)     #Loading the model words
model_bin = fText.load_fasttext_format("./wiki.en.bin")


# We loaded the model using gensim. 'model_words' contains the word which are there in the dict of pre-trained model.

# In[ ]:


from nltk import SnowballStemmer
from nltk.corpus import stopwords

stop_words = stopwords.words('english')      #loading the stopwords
stemmer = SnowballStemmer("english")         #loading the stemmer

delimiter = [',', ':','!', '@','&','$','.','/',']','[']     #defining a set of delimeters


# In[ ]:


import csv

data_encoding = dict()                          #For storing ICD codes and its short description
flag = 0

with open("./ukb_coding19.tsv") as fd:           #Loading the Csv file containing ICD codes and its short description
    rd = csv.reader(fd, delimiter="\t", quotechar='"')
    for row in rd:                            #iterating through each row
    	if (flag==0):                         #Ignoring first row
    		flag = 1
    		continue
    	a = row[1].split(' ',1)[1]
    	data_encoding[row[0]]=a              #Storing description in a dict


# We loaded the ICD codes and their short description in a dict named "data_encoding"

# In[ ]:


app_syn = dict()                     #For storing approximate synonyms corresponding to each ICD code
cli_info = dict()                    #For storing clinical information corresponding to each ICD code

with open("./icd_info4.csv") as fd:  #"icd_info4.csv" files contains clinical information and aprroximate synonyms of ICD codes
    rd = csv.reader(fd, delimiter=",", quotechar='"')
    for row in rd:
    	row[0] = row[0].split('-')[0]
    	try:
    		row[0] = row[0].split('.')[0] + row[0].split('.')[1]
    	except:
    		row[0] = row[0].split('.')[0]
    	cli_info[row[0]] = row[3]
    	app_syn[row[0]] = row[4]


# In[ ]:


import pickle         #For saving the vectors as object file

def save_obj(obj, name ):
	with open(name + '.pkl', 'wb') as f:
		pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)


# We loaded the approximate synonyms, clincal information and ICD code description in three different dict file.

# In[ ]:


# from nltk import word_tokenize, sent_tokenize
# import numpy as np

# def process(value):       #This method gives a single vector corresponding to the value passed.
# 	word_count = 0
# 	value_vec = np.array([0] * 300)
# 	for word in word_tokenize(value):
# 		word = word.lower()
# 		if(word in model_words and word not in stop_words and word not in delimiter):
# 			value_vec = value_vec + model.wv[word]
# 			word_count = word_count + 1
# 		elif(stemmer.stem(word) in model_words and stemmer.stem(word) not in stop_words and stemmer.stem(word) not in delimiter):
# 			value_vec = value_vec + model.wv[stemmer.stem(word)]
# 			word_count = word_count + 1
# 		elif(word not in stop_words and word not in delimiter):
# 			value_vec = value_vec + model_bin.wv[word]
# 			word_count = word_count + 1

# 	if(word_count>0):
# 		value_vec = value_vec/word_count

# 	return value_vec


# In[ ]:


def word_encoding(word):      #return vector representation of each words using FastText encoding
    if stemmer.stem(word) in model_words:
        return model.wv[stemmer.stem(word)]
    elif word in model_words:
        return model.wv[word]
    else:
        return model_bin.wv[word]


# In[ ]:


data_encoding_comp = dict()    #for storing complete representation of ICD Codes

for key, value in data_encoding.items():
    data_encoding_comp[key] = value
    if key in cli_info.keys():
        if(len(cli_info[key])>0):  #Adding clinical information to ICD code description if present
            data_encoding_comp[key] = data_encoding_comp[key] + " " + cli_info[key]
    if key in app_syn.keys():
        if(len(app_syn[key])>0):   #Adding approximate synonyms to ICD codes description if present
            data_encoding_comp[key] = data_encoding_comp[key] + " " + app_syn[key]


# In[ ]:


from nltk import word_tokenize, sent_tokenize
import numpy as np

data_encoding_vec = dict()     #temporary dict file for storing vector of ICD codes

for key, value in data_encoding_comp.items():
    word_count = 0
    temp_vec = np.array([0]*300)    #Creating an empty array of zeroes of 300 dimensions
    for word in word_tokenize(value):
        word  = word.lower()
        if word in stop_words or word in delimiter:
            continue
        temp_vec = temp_vec + word_encoding(word)  #Adding vector of each word in description of ICD codes
        word_count = word_count + 1
    if(word_count>0):
        temp_vec = temp_vec/word_count        #Averaging out the vector
    data_encoding_vec[key] = temp_vec


# In[ ]:


icd_code_vec = dict()   #For storing final representation of ICD codes

for key, value in data_encoding_vec.items():
	icd_code_vec[key] = value


for key, value in icd_code_vec.items():     #For maintaining hierarchy in ICD codes
	flag = 1
	temp_key = key
	for key1, value1 in data_encoding_vec.items():
		if(temp_key==key1 or key1.split()[0]=='Block' or key1.split()[0]=='Chapter'):
			continue
		else:
			if(temp_key in key1):
				icd_code_vec[key] = icd_code_vec[key] + value1
				flag = flag + 1
	if(flag>1):
		icd_code_vec[key] =icd_code_vec[key]/flag
        
save_obj(icd_code_vec, "icd_code_vec")


import numpy as np
import pandas as pd
from transformers import BertModel, BertTokenizer, FeatureExtractionPipeline
from transformers import AutoTokenizer, AutoModel, AutoConfig, pipeline

from sklearn.metrics.pairwise import cosine_similarity
import csv
import pickle  # For saving the vectors as object file

config = AutoConfig.from_pretrained("model/GatorTron-OG_icd2vec_finetuning/")
tokenizer = AutoTokenizer.from_pretrained("model/GatorTron-OG")
model = AutoModel.from_pretrained("model/GatorTron-OG_icd2vec_finetuning/")
"""
config = AutoConfig.from_pretrained("model/GatorTron-OG/")
tokenizer = AutoTokenizer.from_pretrained("model/GatorTron-OG")
model = AutoModel.from_pretrained("model/GatorTron-OG/")
fep = pipeline('feature-extraction', model=model, tokenizer=tokenizer, config=config)
"""
data_encoding = dict()  # For storing ICD codes and its short description
flag = 0

with open("data/ukb_coding19.tsv") as fd:  # Loading the Csv file containing ICD codes and its short description
    rd = csv.reader(fd, delimiter="\t", quotechar='"')
    for row in rd:  # iterating through each row
        if (flag == 0):  # Ignoring first row
            flag = 1
            continue
        a = row[1].split(' ', 1)[1]
        data_encoding[row[0]] = a  # Storing description in a dict

app_syn = dict()  # For storing approximate synonyms corresponding to each ICD code
cli_info = dict()  # For storing clinical information corresponding to each ICD code

with open("data/icd_info4.csv", 'r',
          encoding='utf-8') as fd:  # "icd_info4.csv" files contains clinical information and aprroximate synonyms of ICD codes
    rd = csv.reader(fd, delimiter=",", quotechar='"')
    for row in rd:
        row[0] = row[0].split('-')[0]
        try:
            row[0] = row[0].split('.')[0] + row[0].split('.')[1]
        except:
            row[0] = row[0].split('.')[0]
        cli_info[row[0]] = row[3]
        app_syn[row[0]] = row[4]


def save_obj(obj, name):
    with open(name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)


def word_encoding(word):      #return vector representation of each words
    encoded_input = tokenizer(word, max_length=500, truncation=True)
    new_word = tokenizer.decode(encoded_input["input_ids"])
    new_word = new_word.replace('[CLS] ', '')
    new_word = new_word.replace(' [SEP]', '')
    encoded_word = np.array(fep(new_word)).squeeze()
    encoded_word = np.average(encoded_word, axis=0)
    encoded_word = np.expand_dims(encoded_word, axis=0)
    return encoded_word 

data_encoding_comp = dict()    #for storing complete representation of ICD Codes

for key, value in data_encoding.items():
    data_encoding_comp[key] = value
    if key in cli_info.keys():
        if len(cli_info[key]) > 0:  #Adding clinical information to ICD code description if present
            data_encoding_comp[key] = data_encoding_comp[key] + " " + cli_info[key]
    if key in app_syn.keys():
        if len(app_syn[key]) > 0:   #Adding approximate synonyms to ICD codes description if present
            data_encoding_comp[key] = data_encoding_comp[key] + " " + app_syn[key]

data_encoding_vec = dict()     #temporary dict file for storing vector of ICD codes
for key, value in data_encoding_comp.items():
    data_encoding_vec[key] = word_encoding(value)

"""
for key, value in data_encoding_comp.items():
    word_count = 0
    temp_vec = np.array([0]*768)    #Creating an empty array of zeroes of 768 dimensions
    for word in word_tokenize(value):
        word = word.lower()
        if word in stop_words or word in delimiter:
            continue
        temp_vec = temp_vec + word_encoding(word)  #Adding vector of each word in description of ICD codes
        word_count = word_count + 1
    if word_count > 0:
        temp_vec = temp_vec/word_count        #Averaging out the vector
    data_encoding_vec[key] = temp_vec
"""

icd_code_vec = dict()  # For storing final representation of ICD codes

for key, value in data_encoding_vec.items():
    icd_code_vec[key] = value

for key, value in icd_code_vec.items():  # For maintaining hierarchy in ICD codes
    flag = 1
    temp_key = key
    for key1, value1 in data_encoding_vec.items():
        if (temp_key == key1 or key1.split()[0] == 'Block' or key1.split()[0] == 'Chapter'):
            continue
        else:
            if temp_key in key1:
                icd_code_vec[key] = icd_code_vec[key] + value1
                flag = flag + 1
    if flag > 1:
        icd_code_vec[key] = icd_code_vec[key] / flag

save_obj(icd_code_vec, "model/GatorTron-OG_icd2vec_finetuning/icd_code_vec_GatorTron-OG_finetuning")

cosine_similarity(icd_code_vec['A00'], icd_code_vec['A001'])




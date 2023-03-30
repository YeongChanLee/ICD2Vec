#%%

import numpy as np
import pandas as pd
from transformers import BertModel, BertTokenizer, FeatureExtractionPipeline
from transformers import AutoTokenizer, AutoModel, AutoConfig, pipeline

from sklearn.metrics.pairwise import cosine_similarity
import csv
import pickle  # For saving the vectors as object file
import pandas as pd


config = AutoConfig.from_pretrained("model/GatorTron-OG_icd2vec_finetuning/")
tokenizer = AutoTokenizer.from_pretrained("model/GatorTron-OG")
model = AutoModel.from_pretrained("model/GatorTron-OG_icd2vec_finetuning/")
fep = pipeline('feature-extraction', model=model, tokenizer=tokenizer, config=config)

"""
config = AutoConfig.from_pretrained("model/GatorTron-OG/")
tokenizer = AutoTokenizer.from_pretrained("model/GatorTron-OG")
model = AutoModel.from_pretrained("model/GatorTron-OG/")
fep = pipeline('feature-extraction', model=model, tokenizer=tokenizer, config=config)
"""

icd_info = pd.read_csv("data/icd_info_5chr.csv")
icd_info = icd_info.fillna("")
icd_info['COMP'] = icd_info['DIS_NAME'] + " " + icd_info["CLI_INFO"] + " " + icd_info["APP_SYN"]

data_encoding_comp = dict(zip(icd_info['DIS_CODE'], icd_info['COMP']))  # For storing ICD codes and its short description

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

data_encoding_vec = dict()     #temporary dict file for storing vector of ICD codes
for key, value in data_encoding_comp.items():
    data_encoding_vec[key] = word_encoding(value)

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
            if key1.startswith(temp_key):
                icd_code_vec[key] = icd_code_vec[key] + value1
                flag = flag + 1
    if flag > 1:
        icd_code_vec[key] = icd_code_vec[key] / flag

save_obj(icd_code_vec, "model/GatorTron-OG_icd2vec_finetuning/icd_code_vec_GatorTron-OG_finetuning")

cosine_similarity(icd_code_vec['A00'], icd_code_vec['A001'])

import numpy as np
from transformers import AutoTokenizer, AutoModel, AutoConfig, pipeline

from sklearn.metrics.pairwise import cosine_similarity
import pickle  # For saving the vectors as object file
from utils import get_dataset

config = AutoConfig.from_pretrained("emilyalsentzer/Bio_ClinicalBERT")
tokenizer = AutoTokenizer.from_pretrained("emilyalsentzer/Bio_ClinicalBERT")
model = AutoModel.from_pretrained("../model/bio-clinicalBERT_icd2vec_finetuning", config=config)
fep = pipeline('feature-extraction', model=model, tokenizer=tokenizer, config=config)


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


data_encoding_comp = get_dataset()

data_encoding_vec = dict()     #temporary dict file for storing vector of ICD codes
for key, value in data_encoding_comp.items():
    data_encoding_vec[key] = word_encoding(value)

icd_code_vec = dict()  # For storing final representation of ICD codes
for key, value in data_encoding_vec.items():
    icd_code_vec[key] = value

#post-processing
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

save_obj(icd_code_vec, "../model/bio-clinicalBERT_icd2vec_finetuning/icd_code_vec_bio-clinicalBERT_finetuning") # ICD2Vec

cosine_similarity(icd_code_vec['A00'], icd_code_vec['A001'])




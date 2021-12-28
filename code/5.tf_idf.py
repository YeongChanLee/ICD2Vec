from sklearn.feature_extraction.text import TfidfVectorizer

import csv
import numpy as np
import pickle
from utils import get_dataset

def save_obj(obj, name):
    with open(name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

data_encoding_comp = get_dataset()

text = list(data_encoding_comp.values())


tf_idf = TfidfVectorizer(stop_words='english')
x = tf_idf.fit_transform(text)
x_arr = x.toarray()
x_dict = dict()
for arr in range(len(x_arr)):
    x_dict[list(data_encoding_comp.keys())[arr]] = np.expand_dims(x_arr[arr], axis=0)


icd_code_vec = dict()  # For storing final representation of ICD codes

for key, value in x_dict.items():
    icd_code_vec[key] = value

for key, value in icd_code_vec.items():  # For maintaining hierarchy in ICD codes
    flag = 1
    temp_key = key
    for key1, value1 in x_dict.items():
        if (temp_key == key1 or key1.split()[0] == 'Block' or key1.split()[0] == 'Chapter'):
            continue
        else:
            if temp_key in key1:
                icd_code_vec[key] = icd_code_vec[key] + value1
                flag = flag + 1
    if flag > 1:
        icd_code_vec[key] = icd_code_vec[key] / flag


save_obj(icd_code_vec, "../model/tf_idf/icd_vec_tf_idf")

from icdcodex import icd2vec, hierarchy
import csv
import pickle

# workers=-1 parallelizes the node2vec algorithm across all available CPUs
embedder = icd2vec.Icd2Vec(num_embedding_dimensions=128, workers=-1)
embedder.fit(*hierarchy.icd10cm())

data_encoding = dict()  # For storing ICD codes and its short description
flag = 0
with open("../data/ukb_coding19.tsv") as fd:  # Loading the Csv file containing ICD codes and its short description
    rd = csv.reader(fd, delimiter="\t", quotechar='"')
    for row in rd:  # iterating through each row
        if (flag == 0):  # Ignoring first row
            flag = 1
            continue
        a = row[1].split(' ', 1)[1]
        data_encoding[row[0]] = a  # Storing description in a dict

codes_of_interest = list(data_encoding.keys())
for i in range(len(codes_of_interest)):
    tmp = codes_of_interest[i]
    if(len(tmp) > 3):
        tmp = tmp[:3] + '.' + tmp[3:]
    codes_of_interest[i] = tmp

codes_of_interest_continuous = dict()
for i in range(len(codes_of_interest)):
    if i % 1000 == 0: print(str(i)+'th start!!')
    try:
        code_vec = embedder.to_vec(codes_of_interest[i:i+1])
        codes_of_interest_continuous[codes_of_interest[i]] = code_vec
    except:
        continue


def save_obj(obj, name):
    with open(name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

save_obj(codes_of_interest_continuous, '../model/icd_codex/icd_codex')

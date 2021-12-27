import pickle
import numpy as np
from transformers import AutoTokenizer, AutoModel,pipeline, AutoConfig
from sklearn.metrics.pairwise import cosine_similarity


def load_obj(name):  # for loading the pickle file
    try:
        f = open(name + '.pkl', 'rb')
    except IOError:
        return None
    else:
        return pickle.load(f)

# Bio_ClinicalBERT
icd_vec = load_obj("../model/bio-clinicalBERT_icd2vec_finetuning/icd_code_vec_bio-clinicalBERT_finetuning")
config = AutoConfig.from_pretrained("emilyalsentzer/Bio_ClinicalBERT")
tokenizer = AutoTokenizer.from_pretrained("emilyalsentzer/Bio_ClinicalBERT")
model = AutoModel.from_pretrained("../model/bio-clinicalBERT_icd2vec_finetuning", config=config)
fep = pipeline('feature-extraction', model=model, tokenizer=tokenizer)


def word_encoding(word):      #return vector representation of each words
    encoded_word = np.array(fep(word)).squeeze()
    encoded_word = np.average(encoded_word, axis=0)
    encoded_word = np.expand_dims(encoded_word, axis=0)
    return encoded_word

#For finding ICD codes related to the symptoms
query_vec = word_encoding("Nearsightedness is a common vision condition in which you can see objects near to you clearly, but objects farther away are blurry.")
ans_dict = dict()
for key, value in icd_vec.items():
    if(len(key)!=3):
        continue
    ans_dict[key] = cosine_similarity(value, query_vec)
my_ans = sorted(ans_dict, key=ans_dict.get, reverse=True)[:5]
print(my_ans)
print(ans_dict[my_ans[0]],
      ans_dict[my_ans[1]],
      ans_dict[my_ans[2]],
      ans_dict[my_ans[3]],
      ans_dict[my_ans[4]])

#For finding ICD codes related to the symptoms
query_vec = word_encoding("Itchy skin is an uncomfortable, irritating sensation that makes you want to scratch.")
ans_dict = dict()
for key, value in icd_vec.items():
    if(len(key)!=3):
        continue
    ans_dict[key] = cosine_similarity(value, query_vec)
my_ans = sorted(ans_dict, key=ans_dict.get, reverse=True)[:5]
print(my_ans)
print(ans_dict[my_ans[0]],
      ans_dict[my_ans[1]],
      ans_dict[my_ans[2]],
      ans_dict[my_ans[3]],
      ans_dict[my_ans[4]])

#For finding ICD codes related to the symptoms
query_vec = word_encoding("Coma is a state of prolonged unconsciousness that can be caused by a variety of problems.")
ans_dict = dict()
for key, value in icd_vec.items():
    if(len(key)!=3):
        continue
    ans_dict[key] = cosine_similarity(value, query_vec)
my_ans = sorted(ans_dict, key=ans_dict.get, reverse=True)[:5]
print(my_ans)
print(ans_dict[my_ans[0]],
      ans_dict[my_ans[1]],
      ans_dict[my_ans[2]],
      ans_dict[my_ans[3]],
      ans_dict[my_ans[4]])

#For finding ICD codes related to the symptoms
query_vec = word_encoding("Asthma is a condition in which your airways narrow and swell and may produce extra mucus. ")
ans_dict = dict()
for key, value in icd_vec.items():
    if(len(key)!=3):
        continue
    ans_dict[key] = cosine_similarity(value, query_vec)
my_ans = sorted(ans_dict, key=ans_dict.get, reverse=True)[:5]
print(my_ans)
print(ans_dict[my_ans[0]],
      ans_dict[my_ans[1]],
      ans_dict[my_ans[2]],
      ans_dict[my_ans[3]],
      ans_dict[my_ans[4]])


query_vec = (icd_vec['I25'] + icd_vec['I10'])/2
ans_dict = dict()
for key, value in icd_vec.items():
    if(len(key)!=3 or key == 'I10' or key == 'I25'):
        continue
    ans_dict[key] = cosine_similarity(value, query_vec)
my_ans = sorted(ans_dict, key=ans_dict.get, reverse=True)[:5]
print(my_ans)
print(ans_dict[my_ans[0]],
      ans_dict[my_ans[1]],
      ans_dict[my_ans[2]],
      ans_dict[my_ans[3]],
      ans_dict[my_ans[4]])

query_vec = (icd_vec['H34'] + icd_vec['E11'])/2
ans_dict = dict()
for key, value in icd_vec.items():
    if(len(key)!=3 or key == 'H34' or key == 'E11'):
        continue
    ans_dict[key] = cosine_similarity(value, query_vec)
my_ans = sorted(ans_dict, key=ans_dict.get, reverse=True)[:5]
print(my_ans)
print(ans_dict[my_ans[0]],
      ans_dict[my_ans[1]],
      ans_dict[my_ans[2]],
      ans_dict[my_ans[3]],
      ans_dict[my_ans[4]])

query_vec = word_encoding("Coronaviruses are a family of viruses that can cause illnesses such as the common cold, severe acute respiratory syndrome (SARS) and Middle East respiratory syndrome (MERS). In 2019, a new coronavirus was identified as the cause of a disease outbreak that originated in China. \
The virus is now known as the severe acute respiratory syndrome coronavirus 2 (SARS-CoV-2). The disease it causes is called coronavirus disease 2019 (COVID-19). In March 2020, the World Health Organization (WHO) declared the COVID-19 outbreak a pandemic. \
Public health groups, including the U.S. Centers for Disease Control and Prevention (CDC) and WHO, are monitoring the pandemic and posting updates on their websites. These groups have also issued recommendations for preventing and treating the illness. \
Signs and symptoms of coronavirus disease 2019 (COVID-19) may appear two to 14 days after exposure. \
This time after exposure and before having symptoms is called the incubation period. Common signs and symptoms can include: Fever, Cough, Tiredness. Early symptoms of COVID-19 may include a loss of taste or smell. Other symptoms can include: Shortness of breath or difficulty breathing, Muscle aches, Chills, Sore throat, Runny nose, Headache, Chest pain, Pink eye (conjunctivitis).")

ans_dict = dict()
for key, value in icd_vec.items():
    if(len(key)!=3):
        continue
    ans_dict[key] = cosine_similarity(value, query_vec)
my_ans = sorted(ans_dict, key=ans_dict.get, reverse=True)[:5]
print(my_ans)
print(ans_dict[my_ans[0]],
      ans_dict[my_ans[1]],
      ans_dict[my_ans[2]],
      ans_dict[my_ans[3]],
      ans_dict[my_ans[4]])
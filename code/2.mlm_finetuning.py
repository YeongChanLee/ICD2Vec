from transformers import BertTokenizer, BertForMaskedLM, TrainingArguments, Trainer, FeatureExtractionPipeline
from transformers import AutoTokenizer, AutoModelForMaskedLM, AutoConfig, pipeline

import torch
import csv
import numpy as np

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

app_syn = dict()  # For storing approximate synonyms corresponding to each ICD code
cli_info = dict()  # For storing clinical information corresponding to each ICD code

with open("../data/icd_info4.csv", 'r',
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

data_encoding_comp = dict()    #for storing complete representation of ICD Codes
for key, value in data_encoding.items():
    data_encoding_comp[key] = value
    if key in cli_info.keys():
        if len(cli_info[key]) > 0:  #Adding clinical information to ICD code description if present
            data_encoding_comp[key] = data_encoding_comp[key] + " " + cli_info[key]
    if key in app_syn.keys():
        if len(app_syn[key]) > 0:   #Adding approximate synonyms to ICD codes description if present
            data_encoding_comp[key] = data_encoding_comp[key] + " " + app_syn[key]

text = list(data_encoding_comp.values())
text = np.repeat(text, 5)
np.random.shuffle(text)
text = text.tolist()

config = AutoConfig.from_pretrained("emilyalsentzer/Bio_ClinicalBERT")
tokenizer = AutoTokenizer.from_pretrained("emilyalsentzer/Bio_ClinicalBERT")
model = AutoModelForMaskedLM.from_pretrained("emilyalsentzer/Bio_ClinicalBERT", config=config)

inputs = tokenizer(text, return_tensors='pt', max_length=512, truncation=True, padding='max_length')
inputs['labels'] = inputs.input_ids.detach().clone()

# create random array of floats in equal dimension to input_ids
rand = torch.rand(inputs.input_ids.shape)
# where the random array is less than 0.3, we set true
mask_arr = (rand < 0.3) * (inputs.input_ids != 101) * (inputs.input_ids != 102) * (inputs.input_ids != 0)

# create selection from mask_arr
selection = []
for i in range(inputs.input_ids.shape[0]):
    selection.append(
        torch.flatten(mask_arr[i].nonzero()).tolist()
    )

# apply selection index to inputs.input_ids, adding MASK tokens
for i in range(inputs.input_ids.shape[0]):
    inputs.input_ids[i, selection[i]] = 103


class MeditationsDataset(torch.utils.data.Dataset):
    def __init__(self, encodings):
        self.encodings = encodings

    def __getitem__(self, idx):
        return {key: torch.tensor(val[idx]) for key, val in self.encodings.items()}

    def __len__(self):
        return len(self.encodings.input_ids)

dataset = MeditationsDataset(inputs)

args = TrainingArguments(
    output_dir='out',
    save_steps=5000,
    per_device_train_batch_size=6,
    num_train_epochs=2
)

trainer = Trainer(
    model=model,
    args=args,
    train_dataset=dataset
)

trainer.train()
trainer.save_model("model/biobert-large_icd2vec_finetuning")


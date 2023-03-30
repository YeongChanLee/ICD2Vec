#%%
from transformers import BertTokenizer, BertForMaskedLM, TrainingArguments, Trainer, FeatureExtractionPipeline
from transformers import AutoTokenizer, AutoModelForMaskedLM, AutoConfig, pipeline

import torch
import csv
import numpy as np

import pandas as pd

icd_info = pd.read_csv("data/icd_info_5chr.csv")
icd_info = icd_info.fillna("")
icd_info['COMP'] = icd_info['DIS_NAME'] + " " + icd_info["CLI_INFO"] + " " + icd_info["APP_SYN"]

data_encoding_comp = dict(zip(icd_info['DIS_CODE'], icd_info['COMP']))  # For storing ICD codes and its short description

text = list(data_encoding_comp.values())
text = np.repeat(text, 5)
np.random.shuffle(text)
text = text.tolist()

config = AutoConfig.from_pretrained("model/GatorTron-OG")
tokenizer = AutoTokenizer.from_pretrained("model/GatorTron-OG")
model = AutoModelForMaskedLM.from_pretrained("model/GatorTron-OG", config=config)


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
trainer.save_model("model/GatorTron-OG_icd2vec_finetuning")


# %%

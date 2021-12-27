from transformers import TrainingArguments, Trainer, AutoTokenizer, AutoModelForMaskedLM, AutoConfig

import torch
import numpy as np
from utils import get_dataset

data_encoding_comp = get_dataset()

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


class CreateDataset(torch.utils.data.Dataset):
    def __init__(self, encodings):
        self.encodings = encodings

    def __getitem__(self, idx):
        return {key: torch.tensor(val[idx]) for key, val in self.encodings.items()}

    def __len__(self):
        return len(self.encodings.input_ids)

dataset = CreateDataset(inputs)

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
trainer.save_model("../model/biobert-large_icd2vec_finetuning")


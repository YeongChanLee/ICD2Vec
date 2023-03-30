#%%
from transformers import AutoTokenizer, AutoModel, FeatureExtractionPipeline, pipeline, AutoConfig

config = AutoConfig.from_pretrained("model/GatorTron-OG/")
tokenizer = AutoTokenizer.from_pretrained("model/GatorTron-OG")
h_model = AutoModel.from_pretrained("model/GatorTron-OG/")
fep = pipeline('feature-extraction', model=h_model, tokenizer=tokenizer, config=config)

weight = h_model.encoder.state_dict()
weight['layer.0.attention.ln.weight']
weight['layer.23.attention.ln.weight']
w = weight['layer.23.output.dense.weight']
weight['ln.weight']
weight['ln.bias']
#%%
import torch

# Load the model and its state dictionary from the checkpoint file
checkpoint = torch.load('model/GatorTron-OG/MegatronBERT.pt')
model = checkpoint['model']

model['language_model']['transformer']['layers.0.input_layernorm.weight']
model['language_model']['transformer']['layers.23.input_layernorm.weight']
model['language_model']['transformer']['layers.23.mlp.dense_4h_to_h.weight']
model['language_model']['transformer']['final_layernorm.weight']
model['language_model']['transformer']['final_layernorm.bias']
# %%

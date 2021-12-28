
## README first,
- We provide csv files including the vectors of ICD codes from ICD2Vec based on Bio+Clinical BERT.
- Using the csv file, You can get the identical results with our paper.


## If you want to directly train the model for ICD2Vec,
- If you run the codes in 'codes',
  ```
  1.mlm_finetuning.py
  2.make_ICD2Vec.py
  3.pkl2csv.py
  ```
  then you can get the identical csv file and a trained model with ICD2Vec.

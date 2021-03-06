import pandas as pd

fname = "../model/bio-clinicalBERT_icd2vec_finetuning/icd_code_vec_bio-clinicalBERT_finetuning"
tmp_df = pd.read_pickle(fname+".pkl")

tmp0 = pd.DataFrame()
for key, values in tmp_df.items():
    print(key)
    #print(values)
    tmp1 = pd.DataFrame({'DIS_CODE': [key]})
    tmp2 = pd.DataFrame(values)
    tmp3 = pd.concat([tmp1.reset_index(drop=True), tmp2], axis=1)
    #print(tmp3)
    tmp0 = tmp0.append(tmp3)


tmp0.to_csv(fname+".csv")



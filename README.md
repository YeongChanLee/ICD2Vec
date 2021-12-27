# ICD2Vec: Mathematical representation of diseases
<img src="https://img.shields.io/badge/Python-3766AB?style=flat-square&logo=Python&logoColor=white"/></a>
<img src="https://img.shields.io/badge/R-276DC3?style=flat-square&logo=R&logoColor=white"/></a>

The International Classification of Diseases (ICD) codes represent the global standard for reporting disease conditions. The current ICD codes are hierarchically structured and only connote partial relationships among diseases. Therefore, it is important to represent the ICD codes as mathematical vectors to indicate the complex relationships across diseases. Here, we proposed a framework denoted **_ICD2Vec_** for providing mathematical representations of diseases by encoding corresponding information. First, we presented the arithmetic and semantic relationships between diseases by mapping composite vectors for symptoms or diseases to the most similar ICD codes. Second, we confirmed the validity of ICD2Vec by comparing the biological relationships and cosine similarities among the vectorized ICD codes. Third, we proposed a new risk score derived from ICD2Vec, and demonstrated its potential clinical utility for coronary artery disease, type 2 diabetes, dementia, and liver cancer, based on a large prospective cohort from the UK and large electronic medical records from a medical center in South Korea. In summary, ICD2Vec is applicable for diverse quantitative analyses using ICD codes in biomedical research.


Source code and data can be downloaded at [https://github.com/YeongChanLee/ICD2Vec/](https://github.com/YeongChanLee/ICD2Vec/).<br/>
Contact: [honghee.won@gmail.com](mailto:honghee.won@gmail.com).<br />
## Overview

![Overview](https://github.com/YeongChanLee/ICD2Vec/blob/v0.2/ICD2Vec/ICD2Vec_abstract.PNG)

## Setting
- We recommend to install recent version of Pytorch and Tensorflow
- My setting:

    ```markdown
    PyTorch: 1.9.0+cu111
    Tensorflow: 2.4.1
    ```

## ICD2Vec development
## **1. Crawling ICD-10-CM information**
- Crawling the clinical information of the ICD-10-CM codes :<br />
Reference url: [icd10data.com](https://www.icd10data.com/). 

    `Rscript code/1.crawling_icd10data.R`

- Outcomes: <br />
(1) [icd_info4.csv](https://github.com/YeongChanLee/ICD2Vec/tree/v0.2/code/icd_info4.csv)

    ```markdown
    wget https://github.com/YeongChanLee/ICD2Vec/blob/main/crawling/icd_info4.csv

    ```

## **2. Fine-tuning Bio+Clinical BERT using clinical information of diseases**
We introduce to develop ICD2Vec based on [Bio+Clinical BERT](https://arxiv.org/abs/1904.03323). <br/>
We can build ICD2Vec with simple codes and a pretrained model. You can use another model. <br/>
You can also easily apply ICD2Vec based on other models in our paper.<br/>

### Bio+Clinical BERT
- Download the pre-trained [Bio+Clinical BERT model](https://huggingface.co/emilyalsentzer/Bio_ClinicalBERT) using [HuggingFace](https://huggingface.co/).<br/>

    `import transformers`
    ```markdown
    from transformers import TrainingArguments, Trainer, AutoTokenizer, AutoModelForMaskedLM, AutoConfig
    
    config = AutoConfig.from_pretrained("emilyalsentzer/Bio_ClinicalBERT")
    tokenizer = AutoTokenizer.from_pretrained("emilyalsentzer/Bio_ClinicalBERT")
    model = AutoModelForMaskedLM.from_pretrained("emilyalsentzer/Bio_ClinicalBERT", config=config)
    ```
- Full script is for masked language modeling for fine-tuning in the code 'code/2.mlm_finetuning.py'


## **3. ICD2Vec development**
- Generate ICD2Vec with this code:<br />

    `code/3.develop_ICD2Vec.py`

- Outcomes (for example): <br />

    `model/bio-clinicalBERT_icd2vec_finetuning/icd_code_vec_bio-clinicalBERT_finetuning.pkl`

    We provide split ICD2Vec pkl or csv. <br/>
    The pkl file is identical with the csv file. <br/>
    For example, ICD2Vec.csv contains ICD code (column name of 'DIS_CODE') and 768 dimensional vectors. <br/>
    Please download: <br/>
    (1) 

    ```markdown
    wget 
    
    ```
    
## **4. Analogical reasoning with ICD2Vec**
- Analogical reasoning with ICD2Vec (Table 1)<br />
- See 'code/4.similarity_ICD2Vec.py'
- For example,

    ```markdown
    input: "Nearsightedness is a common vision condition in which you can see objects near to you clearly, but objects farther away are blurry."
    output(top-5 ICD codes): ['H53', 'H52', 'H44', 'F40', 'R11']
    ```

## Additional experiments
- EDA for the vectorized ICD-10-CM codes
- See 'examples' directory

    `EDA.Rmd`


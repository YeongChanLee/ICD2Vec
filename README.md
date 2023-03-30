# ICD2Vec: Mathematical representation of diseases
<img src="https://img.shields.io/badge/Python-3766AB?style=flat-square&logo=Python&logoColor=white"/></a>
<img src="https://img.shields.io/badge/R-276DC3?style=flat-square&logo=R&logoColor=white"/></a>

# Newly updated! - Mar. 26th, 2023
We updated ICD2Vec using [GatorTron](https://www.nature.com/articles/s41746-022-00742-2)

## Background 
The International Classification of Diseases (ICD) codes represent the global standard for reporting disease conditions. The current ICD codes connote direct human-defined relationships among diseases in a hierarchical tree structure. Representing the ICD codes as mathematical vectors helps to capture nonlinear relationships in medical ontologies across diseases.
## Methods 
We propose a universally applicable framework called “ICD2Vec” designed to provide mathematical representations of diseases by encoding corresponding information. First, we present the arithmetical and semantic relationships between diseases by mapping composite vectors for symptoms or diseases to the most similar ICD codes. Second, we investigated the validity of ICD2Vec by comparing the biological relationships and cosine similarities among the vectorized ICD codes. Third, we propose a new risk score called IRIS, derived from ICD2Vec, and demonstrate its clinical utility with large cohorts from the UK and South Korea.
## Results 
Semantic compositionality was qualitatively confirmed between descriptions of symptoms and ICD2Vec. For example, the most diseases most similar to COVID-19 were found to be the common cold (ICD-10: J00), unspecified viral hemorrhagic fever (ICD-10: A99), and smallpox (ICD-10: B03). We show the significant associations between the cosine similarities derived from ICD2Vec and the biological relationships using disease-to-disease pairs. Furthermore, we observed significant adjusted hazard ratios (HR) and area under the receiver operating characteristics (AUROC) between IRIS and risks for eight diseases. For instance, the higher IRIS for coronary artery disease (CAD) can be the higher probability for the incidence of CAD (HR: 2.15 [95% CI 2.02–2.28] and AUROC: 0.587 [95% CI 0.583–0.591]). We identified individuals at substantially increased risk of CAD using IRIS and 10-year atherosclerotic cardiovascular disease risk (adjusted HR, 4.26, 95% CI, 3.59–5.05).
## Conclusions 
ICD2Vec, a proposed universal framework for converting qualitatively measured ICD codes into quantitative vectors containing semantic relationships between diseases, exhibited a significant correlation with actual biological significance. In addition, the IRIS was a significant predictor of major diseases in a prospective study using two large-scale Biobank EHR datasets. Based on this clinical validity and utility evidence, we suggest that publicly available ICD2Vec can be used in diverse research and clinical practices and has important clinical implications.


Source code and data can be downloaded at [https://github.com/YeongChanLee/ICD2Vec/](https://github.com/YeongChanLee/ICD2Vec/).<br/>
Contact: [conan_8th@naver.com](mailto:conan_8th@naver.com).<br />
## Overview

<img src="https://github.com/YeongChanLee/ICD2Vec/blob/v0.2/ICD2Vec/ICD2Vec_abstract.PNG" width="379" height="540"/>

## Setting
- We recommend to install recent version of Pytorch and Tensorflow.
- My setting (main packages):

    ```markdown
    PyTorch: 1.13.1+cu117
    Tensorflow: 2.11.0
    ```

## ICD2Vec development
## **1. Crawling ICD-10-CM information**
- Crawling the clinical information of the ICD-10-CM codes :<br />
Reference url: [icd10data.com](https://www.icd10data.com/). 

    `Rscript code/1.crawling_icd10data.R`

- Outcomes: <br />
(1) [icd_info4.csv](https://github.com/YeongChanLee/ICD2Vec/tree/v1.0/code/icd_info4.csv)

    ```markdown
    wget https://github.com/YeongChanLee/ICD2Vec/blob/main/crawling/icd_info4.csv

    ```
- Specially, we used 24,354 ICD codes consisting of categories and subcategories with up to 5 characters.
(1) [icd_info_5chr.csv](https://github.com/YeongChanLee/ICD2Vec/tree/v1.0/code/icd_info_5chr.csv)

    ```markdown
    wget https://github.com/YeongChanLee/ICD2Vec/blob/main/crawling/icd_info_5chr.csv

    ```
    
## **2. Fine-tuning GatorTron-OG using clinical information of diseases**
We introduce to develop ICD2Vec based on [GatorTron](https://www.nature.com/articles/s41746-022-00742-2). <br/>
We can build ICD2Vec with simple codes and a pretrained model. You can use another model. <br/>
You can also easily apply ICD2Vec based on other models in our paper.<br/>

### GatorTron-OG compiled to HuggingFace
- Download the pre-trained [GatorTron model](https://catalog.ngc.nvidia.com/orgs/nvidia/teams/clara/models/gatortron_og) developed by [Nvidia NeMo](https://developer.nvidia.com/nemo).<br/>
- We compiled GatorTron-OG to Huggingface framework.

    `import transformers`
    ```markdown
    python NeMo_to_huggingface.py model/GatorTron-OG/MegatronBERT.pt --config_file model/GatorTron-OG/config.json

    ```


    `import transformers`
    ```markdown
    from transformers import TrainingArguments, Trainer, AutoTokenizer, AutoModelForMaskedLM, AutoConfig
    
    config = AutoConfig.from_pretrained("model/GatorTron-OG")
    tokenizer = AutoTokenizer.from_pretrained("model/GatorTron-OG")
    model = AutoModelForMaskedLM.from_pretrained("model/GatorTron-OG", config=config)
    ```
- Full script is for masked language modeling for fine-tuning in the code 'code/2.mlm_finetuning.py'


## **3. ICD2Vec development**
- Generate ICD2Vec with this code:<br />

    `code/2.develop_ICD2Vec.py`

- Outcomes (for example): <br />

    `model/GatorTron-OG_icd2vec_finetuning/icd_code_vec_GatorTron-OG_finetuning.pkl`

    We provide split ICD2Vec pkl or csv. <br/>
    The pkl file is identical with the csv file. <br/>
    For example, ICD2Vec.csv contains ICD code (column name of 'DIS_CODE') and 1024 dimensional vectors. <br/>
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
    input: "Coronaviruses are a family of viruses that can cause illnesses such as the common cold, severe acute respiratory syndrome (SARS) and Middle East respiratory syndrome (MERS). In 2019, a new coronavirus was identified as the cause of a disease outbreak that originated in China. The virus is now known as the severe acute respiratory syndrome coronavirus 2 (SARS-CoV-2). The disease it causes is called coronavirus disease 2019 (COVID-19). In March 2020, the World Health Organization (WHO) declared the COVID-19 outbreak a pandemic. Public health groups, including the U.S. Centers for Disease Control and Prevention (CDC) and WHO, are monitoring the pandemic and posting updates on their websites. These groups have also issued recommendations for preventing and treating the illness. Signs and symptoms of coronavirus disease 2019 (COVID-19) may appear two to 14 days after exposure. This time after exposure and before having symptoms is called the incubation period. Common signs and symptoms can include: Fever, Cough, Tiredness. Early symptoms of COVID-19 may include a loss of taste or smell. Other symptoms can include: Shortness of breath or difficulty breathing, Muscle aches, Chills, Sore throat, Runny nose, Headache, Chest pain, Pink eye (conjunctivitis)."
    output(top-5 ICD codes): ['J00', 'A99', 'B03', 'A90', 'B20']
    ```

## Additional experiments
- <del>http://www.icd2vec.kro.kr/</del>
- EDA for the vectorized ICD-10-CM codes
- See 'examples' directory

    `EDA.Rmd`

## Citation
- We will notice soon.


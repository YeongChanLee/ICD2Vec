# ICD2Vec: Mathematical representation of diseases
<img src="https://img.shields.io/badge/Python-3766AB?style=flat-square&logo=Python&logoColor=white"/></a>
<img src="https://img.shields.io/badge/R-276DC3?style=flat-square&logo=R&logoColor=white"/></a>

The International Classification of Diseases (ICD) codes represent the global standard for reporting disease conditions. The current ICD codes are hierarchically structured and only connote partial relationships among diseases. Therefore, it is important to represent the ICD codes as mathematical vectors to indicate the complex relationships across diseases. Here, we proposed a framework denoted **_ICD2Vec_** for providing mathematical representations of diseases by encoding corresponding information. First, we presented the arithmetic and semantic relationships between diseases by mapping composite vectors for symptoms or diseases to the most similar ICD codes. Second, we confirmed the validity of ICD2Vec by comparing the biological relationships and cosine similarities among the vectorized ICD codes. Third, we proposed a new risk score derived from ICD2Vec, and demonstrated its potential clinical utility for coronary artery disease, type 2 diabetes, dementia, and liver cancer, based on a large prospective cohort from the UK and large electronic medical records from a medical center in South Korea. In summary, ICD2Vec is applicable for diverse quantitative analyses using ICD codes in biomedical research.


Source code and data can be downloaded at [https://github.com/YeongChanLee/ICD2Vec/](https://github.com/YeongChanLee/ICD2Vec/).<br />
Contact: [honghee.won@gmail.com](mailto:honghee.won@gmail.com).<br />
## Main experiments

![Overview](https://github.com/YeongChanLee/ICD2Vec/blob/main/ICD2Vec/ICD2Vec_overview_abb.PNG)

## **#1 Preparing data**
### Fasttext model (wiki)
- Download the pre-trained Fasttext model (Eng. version):<br />
[Download link (~15GB)](https://dl.fbaipublicfiles.com/fasttext/vectors-wiki/wiki.en.zip). 

    `unzip wiki.en.zip`
    ```markdown
    1. wiki.en.vec (~6.2GB)
    2. wiki.en.bin (~8.0GB)
    ```

## **2. Crawling the ICD-10-CM data**
- Crawling the clinical information of the ICD-10-CM codes :<br />
Reference url: [icd10data.com](https://www.icd10data.com/). 

    `Rscript crawling_icd10data.R`

- Outcomes: <br />
(1) [parent_based_crawled_encoding_dup.zip](https://github.com/YeongChanLee/ICD2Vec/blob/main/crawling/parent_based_crawled_encoding_dup.zip), (2) [parent_based_crawled_encoding_dup.z01](https://github.com/YeongChanLee/ICD2Vec/blob/main/crawling/parent_based_crawled_encoding_dup.z01)

    ```markdown
    wget https://github.com/YeongChanLee/ICD2Vec/blob/main/crawling/parent_based_crawled_encoding_dup.zip
    wget https://github.com/YeongChanLee/ICD2Vec/blob/main/crawling/parent_based_crawled_encoding_dup.z01

    unzip parent_based_crawled_encoding_dup.7z
    ※ Please place it in the same directory and decompress it through the .zip format file.
    ```
    


## **3. ICD2Vec development**
- Generating ICD2Vec using the following command:<br />

    `python ICD2VEC.ipynb (Do we need to transfer *ipynb to py?)`

- Outcomes: <br />
(1) [ICD_Code_Vectors.zip](https://github.com/YeongChanLee/ICD2Vec/blob/main/ICD2Vec/ICD_Code_Vectors.zip), (2) [ICD_Code_Vectors.z01](https://github.com/YeongChanLee/ICD2Vec/blob/main/ICD2Vec/ICD_Code_Vectors.z01)

    ```markdown
    wget https://github.com/YeongChanLee/ICD2Vec/blob/main/ICD2Vec/ICD_Code_Vectors.zip
    wget https://github.com/YeongChanLee/ICD2Vec/blob/main/ICD2Vec/ICD_Code_Vectors.z01
    
    unzip ICD_Code_Vectors.zip
    ※ Please place it in the same directory and decompress it through the .zip format file.
    ```
    
## **4. Arthmetic operation with ICD2Vec**
- Generating ICD2Vec using the following command:<br />

    `python ICD2VEC_Similarity.ipynb (Do we need to transfer *ipynb to py?)`

    ```markdown
    outcomes: ...
    examples: ...
    ```

## Additional experiments
#### EDA for the vectorized ICD-10-CM codes
    https://github.com/YeongChanLee/ICD2Vec/blob/main/EDA.html

#### 22222222
    https://github.com/YeongChanLee/ICD2Vec/blob/main/EDA.html


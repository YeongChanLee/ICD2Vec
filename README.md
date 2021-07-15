# ICD2Vec: Mathematical representation of diseases

The International Classification of Diseases (ICD) codes represent the global standard for reporting disease conditions. The current ICD codes are hierarchically structured and only connote partial relationships among diseases. Therefore, it is important to represent the ICD codes as mathematical vectors to indicate the complex relationships across diseases. Here, we proposed a framework denoted **_ICD2Vec_** for providing mathematical representations of diseases by encoding corresponding information. First, we presented the arithmetic and semantic relationships between diseases by mapping composite vectors for symptoms or diseases to the most similar ICD codes. Second, we confirmed the validity of ICD2Vec by comparing the biological relationships and cosine similarities among the vectorized ICD codes. Third, we proposed a new risk score derived from ICD2Vec, and demonstrated its potential clinical utility for coronary artery disease, type 2 diabetes, dementia, and liver cancer, based on a large prospective cohort from the UK and large electronic medical records from a medical center in South Korea. In summary, ICD2Vec is applicable for diverse quantitative analyses using ICD codes in biomedical research.


Source code and data can be downloaded at [https://github.com/YeongChanLee/ICD2Vec/](https://github.com/YeongChanLee/ICD2Vec/).<br />
Contact: [honghee.won@gmail.com](mailto:honghee.won@gmail.com).<br />

## Getting Started
<img src="https://img.shields.io/badge/Python-3766AB?style=flat-square&logo=Python&logoColor=white"/></a>
<img src="https://img.shields.io/badge/R-276DC3?style=flat-square&logo=R&logoColor=white"/></a>


- Clone this repository using the following git command:

    `git clone https://github.com/YeongChanLee/ICD2Vec.git`


## **Step#1 Preparing data**
### Fasttext model (wiki)
- Download the pre-trained Fasttext model (Eng.):<br />
[Download link (~15GB)](https://dl.fbaipublicfiles.com/fasttext/vectors-wiki/wiki.en.zip). 

    `unzip wiki.en.zip`
```markdown
1. wiki.en.vec (~6.2GB)
2. wiki.en.bin (~8.0GB)
```

### 22222222222
- Download the pre-trained Fasttext model (Eng.):<br />
[Download link (~15GB)](https://dl.fbaipublicfiles.com/fasttext/vectors-wiki/wiki.en.zip). 

    `unzip wiki.en.zip`
```markdown
1. wiki.en.vec (~6.2GB)
2. wiki.en.bin (~8.0GB)
```

## **Step#2 ICD-10-CM diagnosis code data**
- Crawling the clinical information of the ICD-10-CM codes :<br />
[Reference url: icd10data.com](https://www.icd10data.com/). 

    `Rscript crawling_icd10data.R`

```markdown
outcomes
1. ..
2. ...
```

### EDA
[PCA plotting](https://github.com/YeongChanLee/ICD2Vec/blob/main/EDA.html)

```markdown
1. ?
2. !?

```

Markdown is a lightweight and easy-to-use syntax for styling your writing. It includes conventions for

```markdown
Syntax highlighted code block

# Header 1



## Header 2
### Header 3
#### just test by shj

- Bulleted
- List

1. Numbered
2. List

**Bold** and _Italic_ and `Code` text

[Link](url) and ![Image](src)
```


[editor on GitHub](https://github.com/normalhyuk/normalhyuk.github.io/edit/master/README.md)

# ICD2Vec: Mathematical representation of diseases

The International Classification of Diseases (ICD) codes represent the global standard for reporting disease conditions. The current ICD codes are hierarchically structured and only connote partial relationships among diseases. Therefore, it is important to represent the ICD codes as mathematical vectors to indicate the complex relationships across diseases. Here, we proposed a framework denoted _ICD2Vec_ for providing mathematical representations of diseases by encoding corresponding information. First, we presented the arithmetic and semantic relationships between diseases by mapping composite vectors for symptoms or diseases to the most similar ICD codes. Second, we confirmed the validity of ICD2Vec by comparing the biological relationships and cosine similarities among the vectorized ICD codes. Third, we proposed a new risk score derived from ICD2Vec, and demonstrated its potential clinical utility for coronary artery disease, type 2 diabetes, dementia, and liver cancer, based on a large prospective cohort from the UK and large electronic medical records from a medical center in South Korea. In summary, ICD2Vec is applicable for diverse quantitative analyses using ICD codes in biomedical research.


Source code and data can be downloaded at [https://github.com/YeongChanLee/ICD2Vec/](https://github.com/YeongChanLee/ICD2Vec/).<br />
Contact: [honghee.won@gmail.com](honghee.won@gmail.com).<br />

## Fasttext
### Download pre-trained Fasttext model .. (+ wiki.)
[download link](https://dl.fbaipublicfiles.com/fasttext/vectors-wiki/wiki.en.zip).
```markdown
1. wiki.en.vec
2. wiki.en.bin

```
### EDA
[PCA plotting](https://github.com/YeongChanLee/ICD2Vec/blob/main/EDA.html)

```markdown
1. ?
2. !?

```

## ICD2Vec (1)

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

For more details see [GitHub Flavored Markdown](https://guides.github.com/features/mastering-markdown/).

### Jekyll Themes

Your Pages site will use the layout and styles from the Jekyll theme you have selected in your [repository settings](https://github.com/normalhyuk/normalhyuk.github.io/settings). The name of this theme is saved in the Jekyll `_config.yml` configuration file.

### Support or Contact

Having trouble with Pages? Check out our [documentation](https://help.github.com/categories/github-pages-basics/) or [contact support](https://github.com/contact) and we’ll help you sort it out.

[editor on GitHub](https://github.com/normalhyuk/normalhyuk.github.io/edit/master/README.md)

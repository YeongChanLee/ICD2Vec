import csv

def get_dataset():
    data_encoding = dict()  # For storing ICD codes and its short description
    flag = 0

    with open("../data/ukb_coding19.tsv") as fd:  # Loading the Csv file containing ICD codes and its short description
        rd = csv.reader(fd, delimiter="\t", quotechar='"')
        for row in rd:  # iterating through each row
            if (flag == 0):  # Ignoring first row
                flag = 1
                continue
            a = row[1].split(' ', 1)[1]
            data_encoding[row[0]] = a  # Storing description in a dict

    app_syn = dict()  # For storing approximate synonyms corresponding to each ICD code
    cli_info = dict()  # For storing clinical information corresponding to each ICD code

    with open("../data/icd_info4.csv", 'r',
              encoding='utf-8') as fd:  # "icd_info4.csv" files contains clinical information and aprroximate synonyms of ICD codes
        rd = csv.reader(fd, delimiter=",", quotechar='"')
        for row in rd:
            row[0] = row[0].split('-')[0]
            try:
                row[0] = row[0].split('.')[0] + row[0].split('.')[1]
            except:
                row[0] = row[0].split('.')[0]
            cli_info[row[0]] = row[3]
            app_syn[row[0]] = row[4]

    data_encoding_comp = dict()  # for storing complete representation of ICD Codes
    for key, value in data_encoding.items():
        data_encoding_comp[key] = value
        if key in cli_info.keys():
            if len(cli_info[key]) > 0:  # Adding clinical information to ICD code description if present
                data_encoding_comp[key] = data_encoding_comp[key] + " " + cli_info[key]
        if key in app_syn.keys():
            if len(app_syn[key]) > 0:  # Adding approximate synonyms to ICD codes description if present
                data_encoding_comp[key] = data_encoding_comp[key] + " " + app_syn[key]

    return data_encoding_comp
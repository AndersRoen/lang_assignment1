# importing the different packages we need to use + setting up nlp
import argparse
import math
import os
import spacy
import re
import string
import numpy as np
import pandas as pd
from collections import Counter
from spacy.matcher import Matcher
nlp = spacy.load("en_core_web_sm")
matcher = Matcher(nlp.vocab)

#loading in the filename
def read_df(filename):
    filepath = os.path.join("in", filename)
    with open(filepath, "r") as file:
        text = file.read()
    return text

# running it through the nlp pipeline
def create_doc(text):
    text = text.lower()
    text = re.sub("\W+", " ", text)
    doc = nlp(text)
    n_tokens = len(doc)
    return doc, n_tokens
    
# defines a key-word, and makes a list of collocates with a window size of 5
def find_collocates(key, doc):
    key = key
    span = 10
    key_counter = 0
    for token in doc:
        if token.text == key:
            key_counter = key_counter + 1
    collocate_list = []
    for token in doc:
        if token.text == key:
            before = token.i - 5 #window size
            after = token.i +5
            for i in range(before, after):
                if str(doc[i]) != key:
                    collocate_list.append(str(doc[i]))
    return collocate_list, key_counter, span

# this extracts what is needed to calculate MI scores
def MI_prep(collocate_list, key_counter, span, n_tokens, doc):
    A = key_counter
    B = []
    # counts how many times each collocate occurs
    for i in range(0, len(collocate_list)-1):
        B_collocates = str(collocate_list[i])
        counter2 = 0
        for token in doc:
            if token.text == B_collocates:
                counter2 += 1
        B.append(counter2)
    
    AB = []
    for i in range(0, len(collocate_list)-1):
        B_collocate = str(collocate_list[i])
        counter3 = 0
        for token in collocate_list:
            if token == B_collocate:
                counter3+= 1
        AB.append(counter3)
    sizeCorpus = n_tokens
    return A, B, AB, sizeCorpus
# calculates the mutual information score
def MI_calc(collocate_list, A, B, AB, sizeCorpus, span):
    MI = []
    for i in range(0, len(collocate_list)-1):
        MI1 = math.log((AB[i] * sizeCorpus/(A * B[i] * span)))/math.log(2)
        MI.append(MI1)
    return(MI)

# makes a pandas dataframe and saves to csv
def collocate_df(collocate_list, B, AB, MI, out_name):
    MI_scores = list(zip(collocate_list, B, AB, MI))
    df = pd.DataFrame(MI_scores, columns = ['words', 'B', 'AB', 'MI'])
    outpath = ("out")
    df.to_csv(os.path.join(outpath, out_name), encoding='utf-8')
    return df

def parse_args():
    # Initialise argparse
    ap = argparse.ArgumentParser()
    # command line parameters
    ap.add_argument("-f", "--filename", required = True, help = "The filename we want to work with")
    ap.add_argument("-o", "--out_name", required = True, help = "The filename we want to work with")
    ap.add_argument("-k", "--key", required = True, help = "The keyword we focus on")
    args = vars(ap.parse_args())
    return args
                    
def main():
    args = parse_args()
    text = read_df(args["filename"])
    doc, n_tokens = create_doc(text)
    coll_list, key_counter, span = find_collocates(args["key"], doc)
    A, B, AB, sizeCorpus = MI_prep(coll_list, key_counter, span, n_tokens, doc)
    MI = MI_calc(coll_list, A, B, AB, sizeCorpus, span)
    df = collocate_df(coll_list, B, AB, MI, args["out_name"])
    print(df) 

if __name__ == "__main__":
    main()


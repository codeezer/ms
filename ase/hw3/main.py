#! /usr/bin/python

from os import read
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer

def read_file(file_path):
    with open(file_path, 'r') as f:
        lines = f.readlines()
    return lines


def sim(a, b):
    return (a*b).sum(axis=1)/(np.linalg.norm(a) * np.linalg.norm(b))

def main():
    # reading the file
    # file1 = './additional_files/jEdit4.3/CorpusMethods-jEdit4.3-AfterSplitStopStem.txt'
    # qfile = './additional_files/jEdit4.3/CorpusQueries-jEdit4.3-AfterSplitStopStem.txt'
    
    file1 = './sample_file.txt'
    qfile = 'query.txt'

    docs = read_file(file1)
    # generate term document matrix
    v = CountVectorizer()
    X = v.fit_transform(docs)
    tdm_df = pd.DataFrame(X.toarray(), columns=v.get_feature_names())
    # print("tdm")
    # print(tdm_df)
    terms_df = pd.DataFrame(columns=tdm_df.columns.values)
    
    # normalize the term document matrix
    tf_df = tdm_df.div(tdm_df.max(axis=1), axis=0)
    # print("norm tdmn")
    # print(tf_df)
    
    # compute document frequencies
    df_df = (tdm_df != 0).sum()
    # print("df")
    # print(df_df)

    # compute inverse document frequencies
    idf_df = np.log(tdm_df.shape[0]/df_df)
    # print("idf")
    # print(idf_df)

    # compute tf-idf weighted matrix
    w_tf_idf_df = tf_df * idf_df
    # print("weighted tf-idf matrix")
    # print(w_tf_idf_df)

    # query handling
    q = read_file(qfile)
    X = v.fit_transform(q)
    q_df = pd.DataFrame(X.toarray(), columns=v.get_feature_names())
    
    qv_df = pd.concat([terms_df, q_df], axis=0, ignore_index=True).fillna(0)

    # cosine similarity
    sim_df = w_tf_idf_df.apply(sim, args=(qv_df, ), axis=1)

    # ranked list
    ranked_list = sim_df.sort_values(0, ascending=False)
    ranked_list.index += 1
    ranked_list.columns = ['Similarity']
    print(ranked_list)


if __name__ == "__main__":
    main()
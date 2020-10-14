#! /usr/bin/python

import os
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer

def read_file(file_path):
    with open(file_path, 'r') as f:
        lines = f.read().splitlines()
    return lines


def sim(a, b):
    return (a*b).sum(axis=1)/(np.linalg.norm(a) * np.linalg.norm(b))

def main():
    # reading the file
    # file1 = './additional_files/jEdit4.3/CorpusMethods-jEdit4.3-AfterSplitStopStem.txt'
    # qfile = './additional_files/jEdit4.3/CorpusQueries-jEdit4.3-AfterSplitStopStem.txt'
    # lfile = './additional_files/jEdit4.3/jEdit4.3ListOfFeatureIDs.txt'
    sets_path = './additional_files/jEdit4.3/jEdit4.3GoldSets/'
    map_file = './additional_files/jEdit4.3/CorpusMethods-jEdit4.3.mapping'
    
    file1 = './sample_file.txt'
    qfile = './query.txt'
    lfile = './list_features.txt'

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
    # print(sim_df)

    # list of features
    lf_df = pd.DataFrame(read_file(lfile), columns=['feature_id'])

    gsmid_map = pd.DataFrame(read_file(map_file), columns=['method_name'])
    

    for i, fid in enumerate(lf_df['feature_id'].values):
        gset_file = "GoldSet{}.txt".format(fid)
        
        ranked_list = sim_df[i].sort_values(0, ascending=False).reset_index()
        
        if fid in lf_df.values:
            temp_rank_list = []
            for gs_mid in read_file(os.path.join(sets_path, gset_file)):
                matches = gsmid_map[gsmid_map['method_name']==gs_mid].index

                gs_mid_p = matches[0] if len(matches)>0 else -1
                
                vsm_all_rank = ranked_list[ranked_list['index']==gs_mid_p].index if gs_mid_p != -1 else "-1"
                if len(vsm_all_rank) < 1:
                    vsm_all_rank = "-1"
                
                temp_rank_list.append(vsm_all_rank)
                
                print(str(fid) + "| " + str(gs_mid_p) + "| " + str(gs_mid) + "| " + str(vsm_all_rank))
            print(max(temp_rank_list))


    # ranked list
    # ranked_list = sim_df.sort_values(0, ascending=False)
    # ranked_list.index += 1
    # ranked_list.columns = ['Similarity']
    # print(ranked_list)


if __name__ == "__main__":
    main()
#! /usr/bin/python

import os
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer

file1 = './additional_files/jEdit4.3/CorpusMethods-jEdit4.3-AfterSplitStopStem.txt'
qfile = './additional_files/jEdit4.3/CorpusQueries-jEdit4.3-AfterSplitStopStem.txt'
lfile = './additional_files/jEdit4.3/jEdit4.3ListOfFeatureIDs.txt'
sets_path = './additional_files/jEdit4.3/jEdit4.3GoldSets/'
map_file = './additional_files/jEdit4.3/CorpusMethods-jEdit4.3.mapping'

def read_file(file_path):
    with open(file_path, 'r') as f:
        lines = f.read().splitlines()
    return lines


def sim(a, b):
    return (a*b).sum(axis=1)/(np.linalg.norm(a) * np.linalg.norm(b))


def compute_sim_mat():
    # reading the file
    
    #file1 = './sample_file.txt'
    #qfile = './query.txt'
    #lfile = './list_features.txt'

    docs = read_file(file1)
    v = CountVectorizer()
    X = v.fit_transform(docs)
    tdm_df = pd.DataFrame(X.toarray(), columns=v.get_feature_names())
    terms_df = pd.DataFrame(columns=tdm_df.columns.values)

    # normalize the term document matrix
    tf_df = tdm_df.div(tdm_df.max(axis=1), axis=0)

    # compute document frequencies
    df_df = (tdm_df != 0).sum()

    # compute inverse document frequencies
    idf_df = np.log(tdm_df.shape[0]/df_df)

    # compute tf-idf weighted matrix
    w_tf_idf_df = tf_df * idf_df

    # query handling
    q = read_file(qfile)
    X = v.fit_transform(q)
    q_df = pd.DataFrame(X.toarray(), columns=v.get_feature_names())
    
    qv_df = pd.concat([terms_df, q_df], axis=0, ignore_index=True).fillna(0)
    
    sim_df = w_tf_idf_df.apply(sim, args=(qv_df, ), axis=1)

    return sim_df


def main():
    # cosine similarity
    naming = [str(i) for i in range(1,151)]
    # sim_df = compute_sim()
    sim_df = pd.read_csv("similarity_matrix.csv", index_col=[0])
    sim_df.columns = naming

    # list of features
    lf_df = pd.DataFrame(read_file(lfile), columns=['feature_id'])

    gsmid_map = pd.DataFrame(read_file(map_file), columns=['method_name'])

    mins = []
    min_position = []
    csv_len = 0
    temp_fid = -1

    # CSV header
    with open("all.csv", "w") as f:
        f.write("featureID" + "\t" + "GoldSet MethodID Position" + "\t" + "GoldSetMethodID" + "\t" + "VSM GoldSetMethodID Rank - All Ranks" + "\n")
    
    with open("min.csv", "w") as f:
        f.write("VSM GoldSetMethodID Rank - Best Rank" + "\n")
    

    featureID = ""
    GoldSetMIDP = ""
    GoldSetMID = ""
    VSMGoldSetMIDR = ""
    VSMGoldSetMIDBR = ""
    # the ranking implementation
    for i, fid in enumerate(lf_df['feature_id'].values, start=1):
        gset_file = "GoldSet{}.txt".format(fid)
        
        ranked_list = sim_df['{}'.format(i)].sort_values(0, ascending=False).reset_index()
        
        if fid in lf_df.values:
            temp_rank_list = []
            for gs_mid in read_file(os.path.join(sets_path, gset_file)):
                matches = gsmid_map[gsmid_map['method_name']==gs_mid].index

                gs_mid_p = matches[0]+1 if len(matches)>0 else -1
                
                vsm_all_rank = ranked_list[ranked_list['index']==gs_mid_p].index if gs_mid_p != -1 else []
                if len(vsm_all_rank) < 1:
                    vsm_all_rank = float('inf')
                else:
                    vsm_all_rank = vsm_all_rank[0]+1
                temp_rank_list.append(vsm_all_rank)
                
                GoldSetMIDP = str(gs_mid_p)
                GoldSetMID = str(gs_mid)
                with open("all.csv", "a") as f:
                    if fid != temp_fid:
                        min_position.append(csv_len)
                        temp_fid = fid
                        featureID = str(fid)
                    else:
                        featureID = ""

                    if vsm_all_rank != float('inf'):
                        VSMGoldSetMIDR = str(vsm_all_rank)
                    else:
                        VSMGoldSetMIDR = ""
                    
                    f.write(featureID + "\t" + GoldSetMIDP + "\t" + GoldSetMID + "\t" + VSMGoldSetMIDR + "\n")
                csv_len += 1
            mins.append(min(temp_rank_list))
        

    with open("min.csv", "a") as f:
        for i in range(csv_len):
            if i in min_position:
                f.write(str(mins[min_position.index(i)]) + "\n")
            else:
                f.write("" +"\n")

    f = pd.read_csv("all.csv", sep="\t") 
    l = pd.read_csv("min.csv", sep="\t", skip_blank_lines=False)
    
    final = pd.concat([f, l], axis=1, join='outer')
    
    final.to_csv("VSM_Effictiveness.csv", float_format="%.f", sep="\t", index=False)
    os.remove("all.csv")
    os.remove("min.csv")

if __name__ == "__main__":
    main()

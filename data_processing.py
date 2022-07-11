import pandas as pd
import numpy as np


def manual_input(file, IS, Sample_metadata, Feature_metadata):
    df = pd.read_excel(file)
    headers = list(df.columns)
    Feature_name = headers[0]
    df = df.set_index(Feature_name)
    #IS = 685
    IS = df.loc[IS]
    df_norm=df/IS
    df_norm.to_json("C:/Users/mavikr/Documents/Python/data_site/static/files/df_norm.json")
    df_norm.to_excel("C:/Users/mavikr/Documents/Python/data_site/static/files/df_norm.xlsx")
    Sample_metadata = Sample_metadata
    Sample_metadata = pd.read_excel(Sample_metadata)
    QC_names = []
    for i in range(len(Sample_metadata)):                 #Change this at some point
        if Sample_metadata.iloc[i,1]== 'QC':
            QC_names.append(Sample_metadata.iloc[i,0])
    QCs = df_norm[QC_names].copy()
    QCs = QCs.loc[(QCs != 0).any(1)]
    RSD = []
    for i in range(len(QCs)):       #Change this at some point
        st_dev = np.std(QCs.iloc[i])
        average = np.average(QCs.iloc[i])
        #print(i, QCs.iloc[i], st_dev)
        #print(st_dev/average)
        RSD.append(np.divide(st_dev, average))
    QCs['RSD'] = RSD
    Pass_RSD = QCs.loc[QCs['RSD'] < 0.3]
    QCs.to_excel("C:/Users/mavikr/Documents/Python/data_site/static/files/QCs.xlsx")
    Pass_RSD.to_excel("C:/Users/mavikr/Documents/Python/data_site/static/files/Pass_RSD.xlsx")
    cor= Pass_RSD.T.astype(float)
    cor_matrix = cor.corr().abs()
    upper_tri = cor_matrix.where(np.triu(np.ones(cor_matrix.shape),k=1).astype(bool))
    s = upper_tri.stack()
    highly_correlating_features = (list(s[s.gt(0.95)].index))
    tup = pd.DataFrame(highly_correlating_features, columns = ['dummy', 'comment'])
    tup.sort_values
    feature_metadata = pd.read_excel(Feature_metadata)
    feature_metadata2 = feature_metadata.set_index(feature_metadata.iloc[:,0])
    masses = feature_metadata2.iloc[:,2]
    RTs = feature_metadata2.iloc[:,1]
    new_tup_dummy = []
    new_tup_comment = []
    for i in range(len(tup)):
        feature1 = tup.iloc[i,0]
        feature2 = tup.iloc[i,1]
        mass_diff = abs(masses.loc[feature1]-masses.loc[feature2])  
        RT_diff = abs(RTs.loc[feature1]-RTs.loc[feature2])
        if mass_diff <0.3 and RT_diff < 10:
            new_tup_dummy.append(feature1)
            new_tup_comment.append(feature2)
    new_tup = pd.DataFrame()
    new_tup['dummy'] = new_tup_dummy
    new_tup['comment'] =new_tup_comment
    dummy = []
    duplicates_list = []
    to_drop = []
    new_tup2 = pd.DataFrame()
    first = True
    for i in range(len(new_tup)):
        if first == True:
            dummy = new_tup.iloc[i][0]
            duplicates_list.append(new_tup.iloc[i][1])
            to_drop.append(new_tup.iloc[i-1][1])
            first = False
        else:    
            if new_tup.iloc[i][0] == new_tup.iloc[i-1][0]:
                duplicates_list.append(new_tup.iloc[i-1][1])
                to_drop.append(new_tup.iloc[i-1][1])
            else:
                new_tup2[dummy] = [duplicates_list]
                dummy = []
                duplicates_list= []
                dummy = new_tup.iloc[i][0]
                duplicates_list.append(new_tup.iloc[i][1])   
                to_drop.append(new_tup.iloc[i-1][1])
    if duplicates_list:
        new_tup2[dummy] = [duplicates_list]
        new_tup2 = new_tup2.T
        new_tup2.reset_index(inplace=True)
        new_tup2.columns=[Feature_name,'duplicates']
        Passed_features1 = Pass_RSD.drop(index = to_drop, axis = 0)
        new_Passed_features = pd.merge(Passed_features1, new_tup2, how = 'outer', on = Feature_name)
    else:
        new_Passed_features = Pass_RSD
    new_Passed_features.to_excel("C:/Users/mavikr/Documents/Python/data_site/static/files/Final_results.xlsx")

        
import pandas as pd
def data_info(dataset):
    try:
        col_name = [] #save col name
        Count    = []
        Missing  = []
        N_unique = []
        Unique   = []
        Dtype    = []
        for col in dataset.columns:
            col_name.append(col)
            Count.append(dataset[col].count())
            Missing.append(dataset[col].isna().sum())
            N_unique.append(dataset[col].nunique())
            Unique.append(dataset[col].unique())
            Dtype.append(dataset[col].dtype)
        return pd.DataFrame({"Col_Name" : col_name , "Dtype" : Dtype ,
                             "N_unique" : N_unique , "Count" : Count ,
                             "Missing"  : Missing  , "Unique": Unique  })
    except Exception  as e :
        print("Error: ",e)
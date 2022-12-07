import os
import sys

import logging

import pandas as pd
import numpy as np

from e_commerce.config import get_conf

def load_parquet_files() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    
    try:
        train = pd.read_parquet(os.path.join(get_conf().DATA, "train.parquet"))
        test = pd.read_parquet(os.path.join(get_conf().DATA, "test.parquet"))
        val = pd.read_parquet(os.path.join(get_conf().DATA, "val.parquet"))
    except FileNotFoundError as fe:
        logging.error(fe.strerror)
        sys.exit(1)

    return train, test, val

def filter_data(data: pd.DataFrame, file_name: str) -> pd.DataFrame:
    data_filtered = data[get_conf().SUBSET_FIELDS]
    data_filtered = data_filtered.drop_duplicates(['user_id', 'product_id'])
    data_filtered.to_csv(os.path.join(get_conf().DATA, file_name), index=False)

    return data_filtered

def select_client_subset(data: pd.DataFrame) -> list[str]:
    data.replace('NA', np.nan, inplace=True)
    
    data.dropna(axis=0, subset='cat_0', inplace=True)
    data = data.drop_duplicates(['user_id', 'product_id'])

    user_ids = data.groupby('user_id')['user_id'].filter(lambda x: len(x) >= get_conf().N_SAMPLES).unique().tolist()
    
    return  user_ids

def get_purchase_data() -> pd.DataFrame:
    train =  pd.read_csv(os.path.join(get_conf().DATA, "train.csv"))
    test =  pd.read_csv(os.path.join(get_conf().DATA, "test.csv"))

    return train, test

def preprocess_data() -> list[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    train, test, val = load_parquet_files()
    user_ids = select_client_subset(train)
    
    train = train[train['user_id'].isin(user_ids)]
    test = test[test['user_id'].isin(user_ids)]
    val = val[val['user_id'].isin(user_ids)]

    test.replace('NA', np.nan, inplace=True)
    val.replace('NA', np.nan, inplace=True)

    test = pd.concat([val, test])

    train = filter_data(train, "train.csv")
    test = filter_data(test, "test.csv")
   
    logging.info(f"Files 'train.csv', 'test.csv' generated in {get_conf().DATA} folder")

def get_categories(train: pd.DataFrame, test: pd.DataFrame) -> list[str]:
    data = pd.concat([train, test], ignore_index=True)

    categories = []
    for category in get_conf().CAT_FIELDS:
        categories.extend(data[category].dropna().unique().tolist())
    
    del(data)

    return categories


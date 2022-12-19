import os
import sys

import logging

import pandas as pd
import numpy as np

from e_commerce.config import get_conf


def load_parquet_files() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Reads the original datasets that will be filtered

    :return: One tuple with the loaded dataframes
    :rtype: tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]
    """

    try:
        train = pd.read_parquet(os.path.join(get_conf().DATA, "train.parquet"))
        test = pd.read_parquet(os.path.join(get_conf().DATA, "test.parquet"))
        val = pd.read_parquet(os.path.join(get_conf().DATA, "val.parquet"))
    except FileNotFoundError as fe:
        logging.error(fe.strerror)
        sys.exit(1)

    return train, test, val


def filter_data(data: pd.DataFrame, file_name: str) -> pd.DataFrame:
    """Filters the fields of the datasets to be used and saves a copy in csv format in the disc

    :param data: Dataframe to be filtered
    :type data: pd.DataFrame
    :param file_name: Name of the file that will be saved in the data folder
    :type file_name: str
    :return: The filtered dataframe
    :rtype: pd.DataFrame
    """
    data_filtered = data[get_conf().SUBSET_FIELDS]
    data_filtered = data_filtered.drop_duplicates(["user_id", "product_id"])
    data_filtered.to_csv(os.path.join(get_conf().DATA, file_name), index=False)

    return data_filtered


def select_client_subset(data: pd.DataFrame) -> list[str]:
    """Selects the client ids with at least n sales registered and deletes the rows with no main category

    :param data: Dataframe with the sales
    :type data: pd.DataFrame
    :return: Filtered client ids
    :rtype: List[str]
    """
    data.replace("NA", np.nan, inplace=True)

    data.dropna(axis=0, subset="cat_0", inplace=True)
    data = data.drop_duplicates(["user_id", "product_id"])

    user_ids = (
        data.groupby("user_id")["user_id"]
        .filter(lambda x: len(x) >= get_conf().N_ITEMS)
        .unique()
        .tolist()
    )

    return user_ids


def get_purchase_data(unit_test=False) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Returns the purchase filtered data ready to be used

    :param unit_test: Flag for activating test mode
    :type unit_test: Boolean
    :return: train and test dataframes
    :rtype: pd.DataFrame
    """
    opt = 0 if not unit_test else 1

    train = pd.read_csv(os.path.join(get_conf().DATA, get_conf().DB_TRAIN[opt]))
    test = pd.read_csv(os.path.join(get_conf().DATA, get_conf().DB_TEST[opt]))

    return train, test


def preprocess_data():
    """Reads the original dataframes and processes them to generate the csv files that will be used in the process"""
    train, test, val = load_parquet_files()
    user_ids = select_client_subset(train)

    train = train[train["user_id"].isin(user_ids)]
    test = test[test["user_id"].isin(user_ids)]
    val = val[val["user_id"].isin(user_ids)]

    test.replace("NA", np.nan, inplace=True)
    val.replace("NA", np.nan, inplace=True)

    test = pd.concat([val, test])

    train = filter_data(train, "train.csv")
    test = filter_data(test, "test.csv")

    logging.info(f"Files 'train.csv', 'test.csv' generated in {get_conf().DATA} folder")


def get_categories(train: pd.DataFrame, test: pd.DataFrame) -> list[str]:
    """Generate a list of unique categories of the items in the filtered data

    :param train: Training dataframe to be processed
    :type train: pd.DataFrame
    :param test: Testing dataframe to be processed
    :type test: pd.DataFrame
    :return: List of categories gotten in the process
    :rtype: List[str]
    """
    data = pd.concat([train, test], ignore_index=True)

    categories = []
    for category in get_conf().CAT_FIELDS:
        categories.extend(data[category].dropna().unique().tolist())

    del data

    return categories

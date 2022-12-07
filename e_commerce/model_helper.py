import os

import numpy as np
import pandas as pd

import pickle
import logging

from sklearn.neighbors import NearestNeighbors
from e_commerce.config import get_conf


def fill_matrix(
    matrix: pd.DataFrame, reference_sales: pd.DataFrame, inplace: bool = False
) -> pd.DataFrame:
    """Fills the matrix with the frequencies of the purchases of each category for each client

    :param matrix: Matrix to be filled
    :type matrix: pd.DataFrame
    :param reference_sales: Matrix of sales
    :type reference_sales: pd.DataFrame
    :param inplace: If the process is inplace, defaults to False
    :type inplace: bool, optional
    :return: The matrix filled
    :rtype: pd.DataFrame
    """

    if inplace:
        m_filled = matrix
    else:
        m_filled = matrix.copy()

    for _, row in reference_sales.iterrows():
        for cat in get_conf().CAT_FIELDS:
            if not pd.isna(row[cat]):
                m_filled.loc[row["user_id"], row[cat]] += 1

    if inplace:
        return

    return m_filled


def generate_empty_matrix(
    reference_client_ids: np.ndarray, categories: pd.Series
) -> pd.DataFrame:
    """Generates the matrix that will be filled with the preferencies of the each client

    :param reference_client_ids: List of the clients
    :type reference_client_ids: np.ndarray
    :param categories: List of the categories
    :type categories: pd.Series
    :return: Empty matrix to be filled
    :rtype: pd.DataFrame
    """
    return pd.DataFrame(
        data=np.zeros((len(reference_client_ids), len(categories)), dtype=np.int16),
        index=reference_client_ids,
        columns=categories,
        dtype=np.int16,
    )


def filter_train_data(train: pd.DataFrame) -> pd.DataFrame:
    """Last filtering of the data that will be used in the process

    :param train: Dataframe with the sales information
    :type train: pd.DataFrame
    :return: Filtered dataframe with the las n items sold for each client
    :rtype: pd.DataFrame
    """

    train = train.groupby("user_id").tail(get_conf().N_ITEMS)
    train.to_parquet(os.path.join(get_conf().DATA, get_conf().FILTERED_TRAIN_DATA))

    logging.info(f"Filtered train dataset shape: {train.shape}")

    return train


def generate_frequent_matrix(
    train: pd.DataFrame, categories: list[str]
) -> pd.DataFrame:

    user_ids = train["user_id"].unique()
    if not train.empty:

        matrix = generate_empty_matrix(
            reference_client_ids=user_ids, categories=categories
        )
        fill_matrix(matrix, train, inplace=True)

    matrix.to_pickle(os.path.join(get_conf().MODEL, get_conf().FREQUENT_MATRIX))

    logging.info("Frequent matrix generated")

    return matrix


def fit_model(freq_matrix: pd.DataFrame, n_neighbors: int = 3):

    model = NearestNeighbors(
        n_neighbors=n_neighbors, metric="cosine", algorithm="brute", n_jobs=-1
    )

    model.fit(freq_matrix)

    with open(os.path.join(get_conf().MODEL, get_conf().MODEL_FILE_NAME), "wb") as f:
        pickle.dump(model, f)

    logging.info(f"Model fitted and saved in {get_conf().MODEL} folder")

    return model

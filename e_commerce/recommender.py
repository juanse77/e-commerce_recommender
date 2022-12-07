"""Helper module for the manage of the recommendation generation"""

import os

import pandas as pd
import pickle

from sklearn.neighbors import NearestNeighbors
from e_commerce.config import get_conf


def get_neighbors(model: NearestNeighbors, freq_matrix: pd.DataFrame) -> pd.DataFrame:
    """Figures out the best n neighbors for each client

    :param model: Fitted NearestNeighbors object
    :type model: NearestNeighbors
    :param freq_matrix: Matrix with the frequence of categories of products consume for the clients
    :type freq_matrix: pd.DataFrame
    :return: Matrix with one row for the most similar buyers of each client
    :rtype: pd.DataFrame
    """

    neighbors = model.kneighbors(freq_matrix, return_distance=False)

    neighbors_of_users = []
    for neigh_list in neighbors:
        neighbors_of_users.append(pd.DataFrame([freq_matrix.iloc[neigh_list].index]))

    neighbor_ids = pd.concat(neighbors_of_users, ignore_index=True)

    return neighbor_ids


def get_users_recommendations(
    data: pd.DataFrame, neighbors: pd.DataFrame, freq_matrix: pd.DataFrame
) -> list[tuple[str, list[list[str]]]]:
    """Returns a tuple with a list of code items recommendated for each client

    :param data: Dataframe with purchase information
    :type data: pd.DataFrame
    :param neighbors: Dataframe with information of the similar clientes for each client
    :type neighbors: pd.DataFrame
    :param freq_matrix: Dataframe with the frequecies of categories of items consumed by each client
    :type freq_matrix: pd.DataFrame
    :return: A tuple with the recommendations for each client
    :rtype: Tuple[str, List[List[str]]]
    """

    users_recommendation_matrix = []

    neighbors.reset_index()
    for i, user_neighbors in neighbors.iterrows():

        user_recommendation_list = (
            data[data["user_id"].isin(user_neighbors.values)]["product_id"]
            .unique()
            .tolist()
        )

        users_recommendation_matrix.append(
            (freq_matrix.index[i], user_recommendation_list)
        )

    return users_recommendation_matrix


def get_score(recommendation_path: str, test_path: str):
    """Figures out the estimated score reached by the method

    :param recommendation_path: Name of the recommendations file. It must be placed in the data folder
    :type recommendation_path: str
    :param test_path: Name of the test file. It must be placed in the data folder
    :type test_path: str
    :return: The estimated score reached
    :rtype: float
    """

    with open(os.path.join(get_conf().DATA, recommendation_path), "rb") as f:
        recommendations = pickle.load(f)

    validations = pd.read_csv(os.path.join(get_conf().DATA, test_path))

    cont_success = 0
    for user_id, recommendation_list in recommendations:
        future_user_purchase = (
            validations[validations["user_id"] == user_id]["product_id"]
            .unique()
            .tolist()
        )

        for user_purchase in future_user_purchase:
            if user_purchase in recommendation_list:
                cont_success += 1
                break

    return cont_success / len(recommendations)
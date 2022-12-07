import os

import pandas as pd
import pickle

from sklearn.neighbors import NearestNeighbors
from e_commerce.config import get_conf

def get_neighbors(model: NearestNeighbors, freq_matrix: pd.DataFrame, frac: float = 0.1) -> tuple[pd.DataFrame, pd.DataFrame]:    

    neighbors = model.kneighbors(freq_matrix, return_distance=False)

    neighbors_of_users = []
    for neigh_list in neighbors:
        neighbors_of_users.append(pd.DataFrame([freq_matrix.iloc[neigh_list].index]))
    
    neighbor_ids = pd.concat(neighbors_of_users, ignore_index=True)

    return neighbor_ids

def get_user_items(data: pd.DataFrame, freq_matrix: pd.DataFrame) -> tuple[list[pd.DataFrame], list[pd.DataFrame]]:
    
    users_historic_purchase_matrix = []
    
    for u_ids, _ in freq_matrix.iterrows():
        users_historic_purchase_matrix.append(data[data['user_id'] == u_ids])

    return users_historic_purchase_matrix

def get_users_recommendations(data: pd.DataFrame, neighbors: pd.DataFrame, freq_matrix: pd.DataFrame) -> tuple[ str, list[list[str]] ]:
    
    users_recommendation_matrix = []
    
    neighbors.reset_index()
    for i, user_neighbors in neighbors.iterrows():
        
        user_recommendation_list = data[
            data['user_id'].isin(user_neighbors.values)]['product_id'].unique().tolist()

        users_recommendation_matrix.append((freq_matrix.index[i], user_recommendation_list))

    return users_recommendation_matrix

def load_model(model_path: str):
    with open(os.path.join("model", model_path), "rb") as f:
        model = pickle.load(f)

    return model

def load_user_purchase_matrix(matrix_path: str) -> pd.DataFrame:
    return pd.read_pickle(os.path.join("model", matrix_path))

def get_score(recommendation_path: str, test_path: str):

    with open(os.path.join(get_conf().DATA, recommendation_path), "rb") as f:
        recommendations = pickle.load(f)

    validations = pd.read_csv(os.path.join(get_conf().DATA, test_path))
    
    cont_success = 0
    for user_id, recommendation_list in recommendations:
        future_user_purchase = validations[validations['user_id'] == user_id]['product_id'].unique().tolist()

        for user_purchase in future_user_purchase:
            if user_purchase in recommendation_list:
                cont_success += 1
                break
    
    return cont_success / len(recommendations)

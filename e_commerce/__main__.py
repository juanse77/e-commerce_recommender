import os
import sys

import pickle
import logging 

import e_commerce.load_data_helper as ldh
import e_commerce.model_helper as mh
import e_commerce.recommender as rec
from e_commerce.config import get_conf

logging.getLogger().setLevel(logging.INFO)
logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))

def build_dirs():
    if not os.path.exists(get_conf().DATA):
        os.mkdir(get_conf().DATA)

    if not os.path.exists(get_conf().MODEL):
        os.mkdir(get_conf().MODEL)

def generate_purchase_subset():
    ldh.preprocess_data()

def main(score=False):
    build_dirs()

    train, test = ldh.get_purchase_data()
    categories = ldh.get_categories(train, test)

    del(test)

    train = mh.filter_train_data(train)
    freq_matrix = mh.generate_frequent_matrix(train, categories)
    model = mh.fit_model(freq_matrix)

    neighbors = rec.get_neighbors(model, freq_matrix)
    users_recomentation_matrix = rec.get_users_recommendations(train, neighbors, freq_matrix)

    with open(os.path.join(get_conf().DATA, get_conf().RECOMMENDATION_FILE_NAME), "wb") as f:
        pickle.dump(users_recomentation_matrix, f)

    logging.info("File {Configuration.RECOMMENDATION_FILE_NAME} with all user recommendations generated in {Configuration.DATA} folder")

    if score:
        get_score(get_conf().RECOMMENDATION_FILE_NAME, "test.csv")

def get_score(recommendation_path: str, test_path: str):

    try:
        score = rec.get_score(recommendation_path, test_path)
    except FileNotFoundError as fe:
        logging.error(fe.strerror)
        sys.exit(1)

    logging.info(f"Score reached: {round(score * 100, 2)}%")

if __name__ == "__main__":
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "init":
            generate_purchase_subset()
        elif sys.argv[1] == "score":
            main(score=True)
        else:
            logging.error("Subcommand not recognised")
            sys.exit(1)
    else:
        main()

"""Main module for generation of the recommentations"""

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
    """Creates the folder structure"""

    if not os.path.exists(get_conf().DATA):
        os.mkdir(get_conf().DATA)

    if not os.path.exists(get_conf().MODEL):
        os.mkdir(get_conf().MODEL)


def generate_purchase_subset():
    """Reads the original data files for generating a new filtered files"""
    ldh.preprocess_data()


def main(score=False, unit_test=False):
    """Manages all the process to generate the recommendation

    :param score: Sets if executes the calculate of the score or not
    :type score: bool, optional
    """
    build_dirs()

    train, test = ldh.get_purchase_data(unit_test)
    categories = ldh.get_categories(train, test)

    del test

    train = mh.filter_train_data(train)
    freq_matrix = mh.generate_frequent_matrix(train, categories)
    model = mh.fit_model(freq_matrix)

    neighbors = rec.get_neighbors(model, freq_matrix)
    purchases_matrix = rec.get_purchases_matrix(train)

    del train

    users_recomentation_matrix = rec.get_users_recommendations(
        purchases_matrix, neighbors, freq_matrix
    )

    opt = 0 if not unit_test else 1

    with open(
        os.path.join(get_conf().DATA, get_conf().RECOMMENDATION_FILE_NAME[opt]), "wb"
    ) as f:
        pickle.dump(users_recomentation_matrix, f)

    logging.info(
        "File %s with all user recommendations generated in %s folder",
        get_conf().RECOMMENDATION_FILE_NAME[opt],
        get_conf().DATA,
    )

    if score:
        get_score(get_conf().RECOMMENDATION_FILE_NAME[0], "test.csv")


def get_score(recommendation_path: str, test_path: str):
    """Calculates the efficiency of the recommendations

    :param recommendation_path: Name of the recommendation file. It must be placed in data folder
    :type recommendation_path: str
    :param test_path:  Name of the test file. It must be placed in data folder
    :type test_path: str
    """

    try:
        score = rec.get_score(recommendation_path, test_path)
    except FileNotFoundError as fe:
        logging.error(fe.strerror)
        sys.exit(1)

    logging.info("Score reached: %.2f%%", round(score * 100, 2))


if __name__ == "__main__":

    if len(sys.argv) > 1:

        if sys.argv[1] == "init":
            generate_purchase_subset()
        elif sys.argv[1] == "score":
            # get_score("recommendations.pkl", "test.csv")
            main(score=True)
        elif sys.argv[1] == "test":
            main(unit_test=True)
        else:
            logging.error("Subcommand not recognised")
            sys.exit(1)

    else:
        main()

"""Module for generating recommendations"""
import os
import pickle

import numpy as np

from e_commerce.config import get_conf
from e_commerce.__main__ import main


def test_main():
    """Tests the global process"""
    main(unit_test=True)

    with open(
        os.path.join(get_conf().DATA, get_conf().RECOMMENDATION_FILE_NAME[1]), "rb"
    ) as f:
        rec1 = pickle.load(f)

    with open(
        os.path.join(get_conf().DATA, get_conf().RECOMMENDATION_FILE_NAME[2]), "rb"
    ) as f:
        rec2 = pickle.load(f)

    for user1, user2 in zip(rec1, rec2):
        assert user1[0] == user2[0]
        assert np.array_equal(user1[1], user2[1])

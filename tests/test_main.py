import os
import pickle

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

    assert rec1 == rec2

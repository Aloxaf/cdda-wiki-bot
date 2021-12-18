import os
import pytest


@pytest.fixture()
def cdda_data_path():
    return os.environ["CDDA_DATA_PATH"]

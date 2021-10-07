import pytest
from volttron.utils import load_config


def test_load_config_json():
    load_config()


def test_raise_exception_no_file():

    with pytest.raises(FileNotFoundError):
        load_config("")
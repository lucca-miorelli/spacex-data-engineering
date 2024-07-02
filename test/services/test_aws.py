import pandas as pd
import pytest

from app.services.aws import AWS


@pytest.fixture
def aws():
    return AWS()


def test_save_to_json(aws):
    data = {"key": "value"}
    path = "test_path"
    file_name = "test_file"
    aws.save_to_json(data, path, file_name)
    assert aws.read_from_json(f"{path}/{file_name}.json") == data


def test_save_to_parquet(aws):
    df = pd.DataFrame({"key": ["value"]})
    path = "test_path"
    file_name = "test_file"
    aws.save_to_parquet(df, path, file_name)
    assert aws.file_exists(f"{path}/{file_name}.parquet")

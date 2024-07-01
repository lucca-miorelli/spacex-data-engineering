from typing import List, Optional

import pandas as pd

from app.models import Launch
from app.services.aws import AWS
from app.services.db import Database
from app.services.requester import SpaceXRequester


# Get data
def extract_launches() -> Optional[List[Launch]]:
    spacex_requester = SpaceXRequester()
    response = spacex_requester.request_launches()

    try:
        launches: List[Launch] = [Launch(**launch) for launch in response]
        return launches
    except Exception as e:
        print(e)


# Save raw data to S3 as JSON
def save_raw_data(launches: List[Launch]) -> None:
    aws = AWS()
    aws.save_to_json(
        data=[launch.model_dump() for launch in launches],
        path="01_raw",
        file_name="launches",
    )
    return


# Process data
def process_launches(launches: List[Launch]) -> pd.DataFrame:
    df = pd.json_normalize([launch.model_dump() for launch in launches])

    # Explode 'cores' column
    df = df.explode("cores")

    if df["cores"].apply(lambda x: isinstance(x, dict)).any():
        cores_df = pd.json_normalize(df["cores"])
        cores_df.columns = [f"cores.{sub_col}" for sub_col in cores_df.columns]
        df = df.drop(columns=["cores"]).join(cores_df)

    # Explode 'failures' column
    df = df.explode("failures")

    if df["failures"].apply(lambda x: isinstance(x, dict)).any():
        failures_df = pd.json_normalize(df["failures"])
        failures_df.columns = [f"failures.{sub_col}" for sub_col in failures_df.columns]
        df = df.drop(columns=["failures"]).join(failures_df)

    return df.drop(columns=["fairings"])


# Save processed data to S3 as parquet
def save_processed_data(launches_df: pd.DataFrame) -> None:
    aws = AWS()
    aws.save_to_parquet(
        df=launches_df,
        path="02_processed",
        file_name="launches",
    )
    return


# Save processed data to database table
def save_to_database(launches_df: pd.DataFrame) -> None:
    db = Database()
    db.load_dataframe(
        df=launches_df,
        table="launches",
        schema="public",
    )
    return


def main():
    launches = extract_launches()
    save_raw_data(launches)
    processed_df = process_launches(launches)
    save_processed_data(processed_df)
    save_to_database(processed_df)


if __name__ == "__main__":
    main()

from typing import List, Optional

import pandas as pd
from loguru import logger

from app.models import Launch
from app.services.aws import AWS
from app.services.db import Database
from app.services.requester import SpaceXRequester


def extract_launches() -> Optional[List[Launch]]:
    """
    Extracts launches from SpaceX API.

    Returns:
        List[Launch]: List of Launch objects.
    """
    spacex_requester = SpaceXRequester()
    response = spacex_requester.request_launches()

    logger.info(f"Extracted {len(response)} launches from `launches` endpoint.")

    try:
        launches: List[Launch] = [Launch(**launch) for launch in response]
        return launches
    except Exception as e:
        print(e)


def save_raw_data(launches: List[Launch]) -> None:
    """
    Saves raw data to S3 as JSON.
    
    Args:
        launches (List[Launch]): List of Launch objects.
        
    Returns:
        None
    """
    aws = AWS()
    logger.info(f"Saving {len(launches)} launches to S3 as raw data.")
    aws.save_to_json(
        data=[launch.model_dump() for launch in launches],
        path="01_raw",
        file_name="launches",
    )
    return


def type_casting(df: pd.DataFrame) -> pd.DataFrame:
    """
    Type casts DataFrame columns to appropriate types.
    
    Args:
        df (pd.DataFrame): DataFrame to be type casted.
        
    Returns:
        pd.DataFrame: Type casted DataFrame
    """
    # Force `date_utc` to datetime
    df["date_utc"] = pd.to_datetime(df["date_utc"])
    return df


def process_launches(launches: List[Launch]) -> pd.DataFrame:
    """
    Processes the extracted launches data.
    
    Args:
        launches (List[Launch]): List of Launch objects.
        
    Returns:
        pd.DataFrame: Processed DataFrame
    """
    df = pd.json_normalize([launch.model_dump() for launch in launches])
    logger.info(f"Normalized JSON data. DataFrame shape: {df.shape}")

    # Explode 'cores' column
    df = df.explode("cores")

    if df["cores"].apply(lambda x: isinstance(x, dict)).any():
        cores_df = pd.json_normalize(df["cores"])
        cores_df.columns = [f"cores.{sub_col}" for sub_col in cores_df.columns]
        df = df.drop(columns=["cores"]).join(cores_df)

    logger.info(f"Exploded 'cores' column. DataFrame shape: {df.shape}")

    # Explode 'failures' column
    df = df.explode("failures")

    if df["failures"].apply(lambda x: isinstance(x, dict)).any():
        failures_df = pd.json_normalize(df["failures"])
        failures_df.columns = [f"failures.{sub_col}" for sub_col in failures_df.columns]
        df = df.drop(columns=["failures"]).join(failures_df)
    df = df.drop(columns=["fairings"])

    logger.info(f"Exploded 'failures' column. DataFrame shape: {df.shape}")

    df = type_casting(df)
    logger.info(f"Type casted DataFrame. DataFrame shape: {df.shape}")

    return df


def save_processed_data(launches_df: pd.DataFrame) -> None:
    """
    Saves processed data to S3 as parquet.
    
    Args:
        launches_df (pd.DataFrame): Processed DataFrame.
        
    Returns:
        None
    """
    aws = AWS()
    logger.info(f"Saving processed data to S3 as parquet.")
    aws.save_to_parquet(
        df=launches_df,
        path="02_processed",
        file_name="launches",
    )
    return


def save_to_database(launches_df: pd.DataFrame) -> None:
    """
    Saves processed data to database table.
    
    Args:
        launches_df (pd.DataFrame): Processed DataFrame.
        
    Returns:
        None
    """
    db = Database()
    logger.info(f"Saving processed data to database.")
    db.load_dataframe(
        df=launches_df,
        table="launches",
        schema="public",
    )
    return


def main():
    """Main function to orchestrate the data processing pipeline."""
    launches = extract_launches()
    save_raw_data(launches)
    processed_df = process_launches(launches)
    save_processed_data(processed_df)
    save_to_database(processed_df)


if __name__ == "__main__":
    main()

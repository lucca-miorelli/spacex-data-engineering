from dataclasses import dataclass, field
from typing import Literal, Type

import pandas as pd
from loguru import logger
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker

from app.models import Base
from app.settings import settings


@dataclass
class Database:
    engine: Engine = field(init=False)
    session: sessionmaker = field(init=False)

    def __post_init__(self):
        self.engine = create_engine(settings.SQLALCHEMY_DATABASE_URI)
        self.session = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)

    def get_dataframe(self, model: Type[Base]) -> pd.DataFrame:
        """Download the model data from the database as a DataFrame."""
        return pd.read_sql(self.session().query(model.__table__).statement, self.engine)

    def load_dataframe(
        self,
        df: pd.DataFrame,
        table: str,
        schema: str = "public",
        if_exists: Literal["fail", "replace", "append"] = "replace",
    ):
        """Load the data from a DataFrame to the database."""
        df.to_sql(
            table,
            con=self.engine,
            if_exists=if_exists,
            index=False,
            schema=schema,
        )
        logger.info(f"Loaded {len(df)} records to {schema}.{table} (mode: {if_exists})")

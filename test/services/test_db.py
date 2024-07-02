import pandas as pd
import pytest
from sqlalchemy.exc import ProgrammingError

from app.services.db import Database


# Fixture to create a database instance
@pytest.fixture
def db():
    return Database()


@pytest.mark.parametrize(
    "df, table, schema, if_exists",
    [
        (pd.DataFrame(), "test_table", "public", "will_fail"),
        (pd.DataFrame(), "test_table", "public", "append"),
        (pd.DataFrame(), "test_table", "public", "replace"),
    ],
)
def test_load_dataframe(db, df, table, schema, if_exists):
    # Check that the method raises an error if 'if_exists' is not 'append' or 'replace'
    if schema != "public":
        with pytest.raises(ProgrammingError):
            db.load_dataframe(df, table, schema, if_exists)

    if if_exists not in ["append", "replace"]:
        with pytest.raises(ValueError):
            db.load_dataframe(df, table, schema, if_exists)
    else:
        db.load_dataframe(df, table, schema, if_exists)
        # Check that the method returns None
        assert db.load_dataframe(df, table, schema, if_exists) is None

"""Unit tests for the data module"""

import pytest
from src.data import load_data


class TestData:
    """Test the data module"""

    @pytest.fixture(scope="class")
    def df(self):
        yield load_data("tests/data")

    def test_no_consent_column(self, df):
        """Check that the consent column has been removed"""
        consent_col = "Do you agree to take part in this survey?"
        assert consent_col not in df.columns

    def test_column_names(self, df):
        """Check that the column names are correct"""
        col_names = [
            "timestamp",
            "salary",
            "bonus",
            "received_equity",
            "job_title",
            "num_employees",
            "num_subordinates",
            "sector",
            "region",
            "educational_background",
            "highest_education",
            "years_experience",
            "gender",
            "danish_national",
            "tool_usage",
        ]
        for col in col_names:
            assert col in df.columns

    def test_column_types(self, df):
        """Check that the column types are correct"""
        col_types = dict(
            timestamp="datetime64[ns, UTC]",
            salary="int",
            bonus="int",
            received_equity="category",
            job_title="category",
            num_employees="category",
            num_subordinates="category",
            sector="category",
            region="category",
            educational_background="category",
            highest_education="category",
            years_experience="int",
            gender="category",
            danish_national="category",
            tool_usage="object",
        )
        for col_name, dtype in df.dtypes.iteritems():
            assert col_types[col_name] == dtype

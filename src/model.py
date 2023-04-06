import pandas as pd
from functools import partial

from data import load_data
from utils import MANUAL_SORT_COLS
from utils import FILTER_VALS

from sklearn.pipeline import make_pipeline
from sklearn.compose import make_column_transformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.preprocessing import OrdinalEncoder
from sklearn.preprocessing import FunctionTransformer
from sklearn.linear_model import QuantileRegressor
from sklearn.model_selection import cross_val_score


class QuantileModel:
    QUANTILES = [0.05, 0.25, 0.50, 0.75, 0.95]

    def __init__(self):
        self.data = self._filter_irrelevant_samples(load_data())
        # self.feature_transformer = make_column_transformer(
        #     (OneHotEncoder(categories=[df.job_title.unique().to_list()]), ["job_title"]),
        #     (OneHotEncoder(categories=[list(range(16))]), ["years_experience"]),
        #     (OneHotEncoder(categories=[MANUAL_SORT_COLS["num_subordinates"]]), ['num_subordinates']),
        # )
        self.feature_extractor = make_pipeline(
            FunctionTransformer(self._extract_columns),
            make_column_transformer(
                # TODO: This will error on unseen categories, which is nice,
                #       but remember to gray out options that are not in the data
                (OneHotEncoder(), ["job_title_no_senior"]),
                (OrdinalEncoder(categories=[list(range(16))]), ["years_experience"]),
                ("passthrough", ["is_senior"]),
                (OrdinalEncoder(categories=[MANUAL_SORT_COLS["num_subordinates"]]), ["num_subordinates"]),
            ),
        )
        self.model_class = partial(QuantileRegressor, solver="highs", alpha=0.0)
        self._fit()

    @staticmethod
    def _filter_irrelevant_samples(df):
        # Remove irrelevant values i.e. "Other", "Prefer not to say"
        for col in ["job_title", "years_experience", "num_subordinates"]:
            df = df[~df[col].isin(FILTER_VALS)]
        return df

    @staticmethod
    def _extract_columns(df: pd.DataFrame) -> pd.DataFrame:
        df = df.copy()  # avoid unexpected side-effects

        # Use a boolean variable to model whether the title has "senior" in it
        df["is_senior"] = df["job_title"].str.contains("Senior")
        df["job_title_no_senior"] = df["job_title"].str.replace("Senior ", "")

        # Select columns of interest
        selected_cols = df[["is_senior", "job_title_no_senior", "years_experience", "num_subordinates"]]
        return selected_cols

    def _fit(self):
        df = self.data
        self.quantile_models = [self.model_class(quantile=q) for q in self.QUANTILES]

        # Fit model to all data
        x, y = df, df["salary"]
        x = self.feature_extractor.fit_transform(x)
        for m in self.quantile_models:
            m.fit(x, y)

    def predict(self, x: pd.DataFrame) -> pd.Series:
        x = self.feature_extractor.transform(x)
        pred = [model.predict(x) for model in self.quantile_models]
        pred_series = pd.Series({q: p for q, p in zip(self.QUANTILES, pred)}, name="Estimated Salary")
        pred_series.index.name = "Quantiles"
        return pred_series

    def score(self) -> None:
        df = self.data
        x, y = df, df["salary"]
        x = self.feature_extractor.fit_transform(x)
        mae_score = cross_val_score(self.model_class(quantile=0.5), x, y, cv=5, scoring="neg_mean_absolute_error")
        print(f"MAE score: {mae_score.mean():.2f} (mean), +/- {mae_score.std():.2f} (std)")

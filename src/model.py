from data import load_data
from utils import MANUAL_SORT_COLS
from utils import FILTER_VALS

from sklearn.pipeline import make_pipeline
from sklearn.compose import make_column_transformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.preprocessing import OrdinalEncoder
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import train_test_split


def feature_extraction(df):
    df = df.copy()  # avoid unexpected side-effects

    # Use a boolean variable to model whether the title has "senior" in it
    df["is_senior"] = df["job_title"].str.contains("Senior")
    df["job_title_no_senior"] = df["job_title"].str.replace("Senior ", "")

    # Select columns of interest
    selected_cols = df[["is_senior", "job_title_no_senior", "years_experience", "num_subordinates"]]
    return selected_cols


def get_model():

    # Data loading & preprocessing
    df = load_data()

    # Remove irrelevant values i.e. "Other", "Prefer not to say"
    for col in ["job_title", "years_experience", "num_subordinates"]:
        df = df[~df[col].isin(FILTER_VALS)]

    pipeline = make_pipeline(
        # make_column_transformer(
        #     (OneHotEncoder(categories=[df.job_title.unique().to_list()]), ["job_title"]),
        #     (OneHotEncoder(categories=[list(range(16))]), ["years_experience"]),
        #     (OneHotEncoder(categories=[MANUAL_SORT_COLS["num_subordinates"]]), ['num_subordinates']),
        # )
        make_column_transformer(
            (OneHotEncoder(categories=[df.job_title.unique().to_list()]), ["job_title_no_senior"]),
            (OrdinalEncoder(categories=[list(range(16))]), ["years_experience"]),
            ("passthrough", ["is_senior"]),
            (OrdinalEncoder(categories=[MANUAL_SORT_COLS["num_subordinates"]]), ["num_subordinates"]),
        ),
        LinearRegression(),
    )

    # TODO
    # *** FOR MODELLING - LETS MOVE THIS TO A NOTEBOOK!? ***
    x, y = feature_extraction(df), df["salary"]
    r2_score = cross_val_score(pipeline, x, y, cv=5, scoring="r2")
    mse_score = cross_val_score(pipeline, x, y, cv=5, scoring="neg_root_mean_squared_error")
    print(f"R² score: {r2_score.mean():.2f} (mean), +/- {r2_score.std():.2f} (std)")
    print(f"MSE score: {r2_score.mean():.2f} (mean), +/- {mse_score.std():.2f} (std)")
    # *** END ***


    # Fit model to all data
    x, y = feature_extraction(df), df["salary"]
    pipeline.fit(x, y)

    return pipeline

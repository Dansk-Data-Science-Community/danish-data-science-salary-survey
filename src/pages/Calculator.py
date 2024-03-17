import time

from data import load_data
from data import convert_experience_to_int
from model import QuantileModel
from utils import MANUAL_SORT_COLS

import pandas as pd
import streamlit as st


def main():

    # Data loading & preprocessing
    df = load_data()

    select_names = {
        "job_title": "Job title",
        "years_experience": "Years experience",
        "num_subordinates": "Number of subordinates",
    }

    # Input: Job title
    title_opt = df[
        "job_title"
    ].unique()  # NB: We only allow the option that we have collected data for
    title_opt_sorted = [t for t in title_opt if "Senior" not in t] + [
        t for t in title_opt if "Senior" in t
    ]
    title = st.selectbox("Job title", title_opt_sorted)

    # Input: Years experience
    experience_opt = ["Less than a year"] + [str(i) for i in range(1, 16)] + ["15+"]
    experience = st.selectbox("Years experience", experience_opt)

    # Input: No. of subordinates
    subordinaries_opt = MANUAL_SORT_COLS["num_subordinates"]
    subordinaries = st.selectbox("Number of subordinates", subordinaries_opt)

    # Input as valid DataFrame
    input_data = pd.DataFrame(
        [[title, convert_experience_to_int(experience), subordinaries]],
        columns=["job_title", "years_experience", "num_subordinates"],
    )

    # # Input: Comparison variable
    # selected = st.selectbox("Comparison variable", select_names.values())
    # comparison = {v: k for k, v in select_names.items()}[selected]

    with st.spinner("Fetching data"):
        model = QuantileModel()
        pred = model.predict(input_data)
        st.text(f"*** Pred: ***")
        st.dataframe(pred)

        import seaborn as sns
        import matplotlib.pyplot as plt
        fig = plt.figure(figsize=(13, 6))
        preds = {}
        for exp_opt in experience_opt:
            # Input as valid DataFrame
            input_data = pd.DataFrame(
                [[title, convert_experience_to_int(exp_opt), subordinaries]],
                columns=list(select_names),  # dict key order is preserved from python 3.7 and up
            )
            model = QuantileModel()
            preds[exp_opt] = model.predict(input_data)

        preds_df = pd.DataFrame(preds)
        plt.plot(preds_df.T)
        # st.dataframe(preds_df)
        st.pyplot(fig)

        # TODO
        # *** FOR DEBUGGING ***
        filt_df = df[
            (title == df["job_title"])
            & (convert_experience_to_int(experience) == df["years_experience"])
            & (subordinaries == df["num_subordinates"])
        ]
        st.text("For debugging")
        st.dataframe(filt_df)
        # *** END ***


if __name__ == "__main__":
    main()

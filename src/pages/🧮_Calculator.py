import streamlit as st
import numpy as np
from data import load_data
from utils import MANUAL_SORT_COLS

def main():
    """Set up and display the dashboard"""

     # Set the title of the dashboard
    st.set_page_config(page_title="DDSC Salary Survey Dashboard", layout="wide")

    # Allows for adjusting page width
    _, col, _ = st.columns([1, 3, 1])

    with col:

        # Data loading & preprocessing
        df = load_data()

        job_title = st.selectbox("Job title", df.job_title.unique())
        sector = st.selectbox("Sector", df.sector.unique())
        region = st.selectbox("Region", df.region.unique())
        highest_education = st.selectbox("Highest education", df.highest_education.unique())

        filt_df = df[
            (df.job_title == job_title) &
            (df.sector == sector) &
            (df.region == region) &
            (df.highest_education == highest_education)
        ]

        if len(filt_df) < 5:
            st.markdown("Not enough data")
        
        else:
            st.dataframe(filt_df.salary.describe())

        # st.dataframe(filt_df)

if __name__ == "__main__":
    main()
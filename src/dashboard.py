from pydoc import render_doc
import streamlit as st
import pandas as pd
from data import load_data
import numpy as np

import plotly.figure_factory as ff
import plotly.express as px

if __name__ == "__main__":
    df = load_data()

    # Only allow categorical columns
    columns = df.select_dtypes(include=["category"]).columns.values

    option = st.selectbox("Comparison variable", columns)
    render_df = df.copy()

    # Remove unnecessary values for clearner plots
    if option == "received_equity":
        render_df = render_df[
            ~render_df.received_equity.isin(["I do not know", "Prefer not to say"])
        ]
    # TODO: Implement for other columns

    fig = px.box(render_df, x=option, y="salary")

    st.plotly_chart(fig, use_container_width=True)

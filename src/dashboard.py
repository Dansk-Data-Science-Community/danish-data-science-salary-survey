from pydoc import render_doc
import streamlit as st
from data import load_data
from utils import RELEVANT_VALS, INTRO_PARAGRAPH

import plotly.figure_factory as ff
import plotly.express as px

if __name__ == "__main__":
    # Load intro HTML
    st.markdown(INTRO_PARAGRAPH, unsafe_allow_html=True)

    df = load_data()

    # Only allow categorical columns
    columns = df.select_dtypes(include=["category"]).columns.values

    option = st.selectbox("Comparison variable", columns)
    render_df = df.copy()

    # TODO: Display more information on selected category. Maybe also the wording of the question from the survey?

    # Remove unnecessary values for clearner plots
    if option in RELEVANT_VALS:
        render_df = render_df[render_df[option].isin(RELEVANT_VALS[option])]
        fig = px.box(render_df, x=option, y="salary", category_orders=RELEVANT_VALS)

    else:
        fig = px.box(render_df, x=option, y="salary")

    st.plotly_chart(fig, use_container_width=True)

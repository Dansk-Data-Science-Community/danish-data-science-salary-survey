from pydoc import render_doc
import streamlit as st
from data import load_data
from utils import MANUAL_SORT_COLS, MEDIAN_SORT_COLS, INTRO_PARAGRAPH, FILTER_VALS

import plotly.figure_factory as ff
import plotly.express as px

if __name__ == "__main__":
    st.set_page_config(page_title="DDSC Salary Survey Dashboard", layout="wide")

    # Allows for adjusting page width
    _, col, _ = st.columns([1, 3, 1])

    with col:

        # Load intro HTML
        st.markdown(INTRO_PARAGRAPH, unsafe_allow_html=True)

        # Data loading & preprocessing
        df = load_data()

        # Only allow categorical columns
        columns = df.select_dtypes(include=["category"]).columns.values

        # Dropdown for selecting comparison variable
        option = st.selectbox("Comparison variable", columns)

        # Remove irrelevant values i.e. "Other", "Prefer not to say"
        render_df = df[~df[option].isin(FILTER_VALS)]

    # TODO: Display more information on selected category. Maybe also the wording of the question from the survey?

    # Sort values based on median salary
    sort_order = None
    if option in MEDIAN_SORT_COLS:
        sort_order = {
            option: render_df.groupby(option)
            .agg({"salary": "median"})
            .sort_values("salary")
            .index.tolist()
        }

    # Sort values manually and remove clutter
    if option in MANUAL_SORT_COLS:
        render_df = render_df[render_df[option].isin(MANUAL_SORT_COLS[option])]
        sort_order = MANUAL_SORT_COLS

    # Allows for adjusting page width
    _, col, _ = st.columns([1, 10, 1])

    with col:

        # Plot
        fig = px.box(
            render_df,
            x=option,
            y="salary",
            color=option,
            color_discrete_sequence=px.colors.qualitative.Light24,
            category_orders=sort_order,
        )
        fig.update_layout(showlegend=False)

        st.plotly_chart(fig, use_container_width=True)

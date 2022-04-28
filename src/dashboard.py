"""Source code for the dashboard"""

import streamlit as st
#import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
from data import load_data
from utils import (
    MANUAL_SORT_COLS,
    MEDIAN_SORT_COLS,
    INTRO_PARAGRAPH,
    FILTER_VALS,
    COL_NAMES,
)


def main():
    """Set up and display the dashboard"""

    # Set the title of the dashboard
    st.set_page_config(page_title="DDSC Salary Survey Dashboard", layout="wide")

    # Allows for adjusting page width
    _, col, _ = st.columns([1, 3, 1])

    with col:

        # Load intro HTML
        st.markdown(INTRO_PARAGRAPH, unsafe_allow_html=True)

        # Data loading & preprocessing
        df = load_data()

        # Dropdown for selecting comparison variable
        selected = st.selectbox("Comparison variable", COL_NAMES.keys())
        option = COL_NAMES[selected]

        # Remove irrelevant values i.e. "Other", "Prefer not to say"
        render_df = df[~df[option].isin(FILTER_VALS)]

        # Remove values with <5 entries
        grouped_df = render_df.groupby(option).agg({"salary": "count"})
        allowed_vals = grouped_df.query("salary > 5").index.tolist()
        render_df = render_df[render_df[option].isin(allowed_vals)]

    # TODO: Display more information on selected category. Maybe also the
    # wording of the question from the survey?

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

    # More readable plot labels
    labels = {**{"salary": "Salary"}, **{v: k for k, v in COL_NAMES.items()}}

    # Allows for adjusting page width
    _, col, _ = st.columns([1, 5, 1])

    with col:

        # Set up the figure for the plot
        # fig = px.box(
        #     render_df,
        #     x=option,
        #     y='salary',
        #     points=False,
        #     color=option,
        #     color_discrete_sequence=px.colors.diverging.Tealrose,
        #     category_orders=sort_order,
        #     labels=labels,
        # )
        # fig.update_layout(showlegend=False)

        # Display the plot
        # st.plotly_chart(fig, use_container_width=True)

        plt.style.use('seaborn-whitegrid')

        # Remove unused categorical values
        for col, dtype in render_df.dtypes.items():
            if dtype == 'category':
                render_df[col] = render_df[col].cat.remove_unused_categories()

        # Set up the figure for the plot
        fig = plt.figure(figsize=(13, 6))

        # Set up sort order for seaborn
        if sort_order is not None:
            print(sort_order)
            sort_order = [
                col_name for col_name in sort_order[option]
                if col_name in allowed_vals
            ]

        # Set up the seaborn box plot
        sns.boxplot(
            data=render_df,
            x=option,
            y='salary',
            showfliers=False,
            order=sort_order,
            whis=0.0
        )

        # Rotate the x-axis labels
        plt.xticks(rotation=45, ha='right')

        # Set the label for the x-axis and y-axis
        plt.xlabel(labels[option])
        plt.ylabel("Salary")

        # Display the plot
        st.pyplot(fig)


if __name__ == "__main__":
    main()

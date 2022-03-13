from cmath import isnan
import streamlit as st
import pandas as pd
import numpy as np
import time
from collections import Counter
from data import load_data

import plotly.figure_factory as ff
import plotly.graph_objects as go
import plotly.express as px

if __name__ == '__main__':
    df = load_data()

    x1 = df[df.gender == 'male'].salary
    x2 = df[df.gender == 'female'].salary
    x3 = df[df.gender == 'no answer'].salary

    hist_data = [x1, x2]

    group_labels = ['Male', 'Female']
    colors = ['#A56CC1', '#A6ACEC']

    fig = ff.create_distplot(hist_data, group_labels, colors=colors, bin_size=5000, show_rug=False)
    fig.update_xaxes(range=[0, 150000])

    fig.update_layout(title_text='Hist and Curve Plot')

    st.plotly_chart(fig, use_container_width=True)

    # Streamlit widgets automatically run the script from top to bottom. Since
    # this button is not connected to any other logic, it just causes a plain
    # rerun.
    st.button("Re-run")
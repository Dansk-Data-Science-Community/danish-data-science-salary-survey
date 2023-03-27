"""Source code for the dashboard"""

import streamlit as st
from utils import INTRO_PARAGRAPH


def main():
    """Set up and display the dashboard"""

    # Set the title of the dashboard
    st.set_page_config(page_title="DDSC Salary Survey Dashboard", layout="wide")

    # Allows for adjusting page width
    col, _ = st.columns([3, 2])

    with col:

        # Load intro HTML
        st.markdown(INTRO_PARAGRAPH, unsafe_allow_html=True)


if __name__ == "__main__":
    main()

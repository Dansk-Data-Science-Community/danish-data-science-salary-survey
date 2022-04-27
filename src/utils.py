"""Utility variables and functions used in the project."""

from pathlib import Path
import base64


# Column names used on dashboard for readability
COL_NAMES = {
    "Received equity": "received_equity",
    "Job title": "job_title",
    "Number of employees": "num_employees",
    "Number of subordinates": "num_subordinates",
    "Job sector": "sector",
    "Region": "region",
    "Educational background": "educational_background",
    "Highest education": "highest_education",
    "Years experience": "years_experience",
    "Uses high-level languages": "uses_high_level_language",
    "Uses mid-level languages": "uses_mid_level_language",
    "Uses query languages": "uses_query_languages",
    "Uses visualisation tools": "uses_visualisation_tools",
    "Uses deployment tools": "uses_deployment_tools",
    "Uses version control tools": "uses_version_control",
    "Uses spreadsheets": "uses_spreadsheets",
    "Uses distributed computing tools": "uses_distributed_computing_tools",
    "Uses monitoring tools": "uses_monitoring_tools",
    "Uses AutoML tools": "uses_automl_tools",
}


# Columns with an intuitive order - manually set below
MANUAL_SORT_COLS = {
    "received_equity": ["Yes", "No"],
    "num_employees": [
        "0 (e.g., self-employed)",
        "1-9",
        "10-24",
        "25-99",
        "100-249",
        "250+",
    ],
    "num_subordinates": ["0", "1-9", "10-24", "25-99", "100-249", "250+"],
    "region": ["Hovedstaden", "Sjælland", "Syddanmark", "Midtjylland", "Nordjylland"],
    "highest_education": [
        "Secondary school (e.g., gymnasium, high school)",
        "Academy profession degree (kort videregående uddannelse)",
        "Undergraduate (e.g., bachelor, professionsbachelor)",
        "Master's (kandidat)",
        "PhD",
    ],
    "gender": ["male", "female"],
}


# Sort boolean columns in order True, False
MANUAL_SORT_COLS = {
    **MANUAL_SORT_COLS,
    **{COL_NAMES[k]: [True, False] for k in COL_NAMES.keys() if "[Tools]" in k},
}


# Columns that don't have an intuitive order to sort by median salary
MEDIAN_SORT_COLS = ["job_title", "sector", "region", "educational_background"]


# Values to remove for appearance
FILTER_VALS = ["Other", "Prefer not to say"]


# URLs
WEBSITE_URL = "https://ddsc.io/"
GITHUB_URL = "https://github.com/Dansk-Data-Science-Community/danish-data-science-salary-survey"


def get_image(filename: str) -> str:
    '''Helper function to add images to the HTML.

    Args:
        filename (str):
            The name of the image file to add.

    Returns:
        str:
            The bytestring of the b64 encoded image.
    '''
    assets_path = Path(__file__).parent.parent / "assets"
    img_path = assets_path / filename
    b64_encoded = base64.b64encode(img_path.read_bytes())
    return b64_encoded.decode()


INTRO_HTML = f"""
    <div id="header">
        <img src=data:image/png;base64,{encode_img(assets_path + '/ddsc-logo-base.png')} id="logo" />
        <h2>DDSC Salary Survey</h2>
    </div>
    <div id="description">
        This dashboard is generated from results gathered by the <a href="https://ddsc.io/">DDSC</a> salary survey, an anonymous questionnaire concerning data science salaries in Denmark.
        Code can be found on <a href="https://github.com/Dansk-Data-Science-Community/danish-data-science-salary-survey">Github</a>!
    </div>

    <div id="footer">
        <div id="developed-by">Developed by:</div>
        <div id="developers">
            <a href="https://www.linkedin.com/in/torben-albert-lindqvist/" class="dev">
                <img class="dev-img" src="data:image/png;base64,{encode_img(assets_path + '/torben.jpeg')}" />
                <div class="dev-name">Torben Albert-Lindqvist</div>
            </a>
            <a href="https://www.linkedin.com/in/saattrupdan/" class="dev">
                <img class="dev-img" src="data:image/png;base64,{encode_img(assets_path + '/dan.jpeg')}" />
                <div class="dev-name">Dan Saattrup Nielsen</div>
            </a>
            <a href="https://www.linkedin.com/in/kaspergroesludvigsen/" class="dev">
                <img class="dev-img" src="data:image/png;base64,{encode_img(assets_path + '/kasper.jpeg')}" />
                <div class="dev-name">Kasper Groes Albin Ludvigsen</div>
            </a>
        </div>
    </div>
"""


INTRO_CSS = """
    <style>

        a {
            text-decoration: none;
            font-weight: bold;
        }

        .dev {
            margin-top: 10px;
            display: flex;
        }

        .dev-name {
             margin: auto 0 auto 5px;
        }

        .dev-img {
            width: 35px;
            border-radius: 100%;
            margin-right: 5px;
        }

        #header {
            display: flex;
        }

        #logo {
            width: 40px;
            height: 40px;
            margin: auto 10px auto 0;
        }

        #description, #footer {
            margin-bottom: 25px;
        }

        #developers {
            display: flex;
            flex-direction: column;
        }

    </style>
"""


INTRO_PARAGRAPH = INTRO_HTML + INTRO_CSS

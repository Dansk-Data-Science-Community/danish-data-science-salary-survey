from pathlib import Path
import base64

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
    "danish_national": ["Yes", "No"],
}

# Columns that don't have an intuitive order to sort by median salary
MEDIAN_SORT_COLS = ["job_title", "sector", "region", "educational_background"]

# Values to remove for appearance
FILTER_VALS = ["Other", "Prefer not to say"]

assets_path = str(Path(__file__).parent.parent) + '/assets'
encode_img = lambda path: base64.b64encode(Path(path).read_bytes()).decode()

INTRO_HTML = f'''
    <div id="header">
        <img src="https://ddsc.io/static/ddsc-logo-base.png" id="logo" />  
        <h2>DDSC Salary Survey</h2>
    </div>
    <div id="description">This dashboard is generated from results gathered by the <a href="https://ddsc.io/">DDSC</a> salary survey, an anonymous questionnaire concerning data science salaries in Denmark.</div> 

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
'''

INTRO_CSS = '''
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
'''

INTRO_PARAGRAPH = INTRO_HTML + INTRO_CSS

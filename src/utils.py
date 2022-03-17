RELEVANT_VALS = {
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

INTRO_PARAGRAPH = """
    <div id="header">
        <img src="https://ddsc.io/static/ddsc-logo-base.png" id="logo" />  
        <h2>DDSC Salary Survey</h2>
    </div>
    <div id="description">This dashboard is generated from results gathered by the <a href="https://ddsc.io/">DDSC</a> salary survey, an anonymous questionnaire concerning data science salaries in Denmark.</div> 

    <div id="footer">
        <div>Developed by:</div>
        <div id="developers">
            <a href="https://www.linkedin.com/in/torben-albert-lindqvist/">Torben Albert-Lindqvist</a>
            <a href="https://www.linkedin.com/in/saattrupdan/">Dan Saattrup Nielsen</a>
            <a href="https://www.linkedin.com/in/kaspergroesludvigsen/">Kasper Groes Albin Ludvigsen</a>
        </div>
    </div>

    <style>

        a {
            text-decoration: none;
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

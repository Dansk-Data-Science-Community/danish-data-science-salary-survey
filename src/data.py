"""Script containing data loading scripts"""

import pandas as pd
from pathlib import Path


def load_data() -> pd.DataFrame:
    """Loads the survey data as a dataframe.

    Returns:
        Pandas Dataframe:
            The survey data.
    """

    # Locate the path to the data, which takes the first CSV file
    # in the 'data' directory
    data_path = next(Path("data").glob("*.csv"))

    # Load the data
    df = pd.read_csv(data_path)

    # Discard those who did not want to partake and remove the question
    consent = df["Do you agree to take part in this survey?"]
    df = df.query('@consent == "I am happy to take part in this survey"').drop(
        columns=["Do you agree to take part in this survey?"]
    )

    # Rename cols
    df = df.rename(
        columns={
            "Timestamp": "timestamp",
            "What is your monthly salary in DKK, before tax and including pension?": "salary",
            "How much bonus did you receive last year, in DKK?": "bonus",
            "Have you received any equity in your company?": "received_equity",
            "What job title best reflects your daily work?": "job_title",
            "What tools do you use in your daily work?": "tools",
            "How many people are employed at your work?": "num_employees",
            "How many people are you managing at your work?": "num_subordinates",
            "In which sector do you work?": "sector",
            "In which Danish region is your office located?": "region",
            "What educational background do you have?": "educational_background",
            "What is your highest level of education?": "highest_education",
            "How many years of relevant full-time work experience do you have?": "years_experience",
            "What is your gender?": "gender",
            "Are you a Danish national/citizen?": "danish_national",
        }
    )

    # Split the `tools` column into a separate Boolean column for each tool.
    # Note that this effectively removes the 'custom' tool options that people
    # have inserted, as none of those got more than two answers anyway.
    tools = dict(
        uses_high_level_language="High-level programming languages (e.g., Python, R, MATLAB, SAS, Julia, JavaScript)",
        uses_mid_level_language="Mid-level programming languages (e.g., C, C++, C#, Java, Go)",
        uses_visualisation_tools="Advanced visualisation tools (e.g., PowerBI, D3.js, Tableau, Qlik)",
        uses_deployment_tools="Deployment tools (e.g., Docker, AWS SageMaker, Tensorflow Serving, MLflow)",
        uses_version_control="Version control systems (e.g., GitHub, GitLab, BitBucket, Beanstalk)",
        uses_spreadsheets="Spreadsheets (e.g., Excel, Google Sheets)",
        uses_query_languages="Query languages (e.g., SQL, BigQuery)",
        uses_distributed_computing_tools="Distributed computing tools (e.g., Kubernetes, Apache Hadoop, Apache Spark, Ray)",
        uses_monitoring_tools="Monitoring tools (e.g., Arize AI, WhyLabs, Grafana, Evidently, Fiddler)",
        uses_automl_tools="AutoML / Low-code / No-code tools (e.g., PyCaret, TPOT, Google AutoML, Azure ML)",
        uses_rpa_tools="RPA tools (e.g., Zaptest, Eggplant, HelpSystems)",
    )
    for name, desc in tools.items():
        df[name] = df.tools.str.split(";").map(lambda lst: desc in lst)
    df.drop(columns="tools", inplace=True)

    # Convert the 'timestamp' column to a datetime format, rather than simply a
    # datetime string
    df["timestamp"] = pd.to_datetime(df["timestamp"])

    # Duplicate years_experience col and convert to numeric. NB! 15+ years will
    # simply be 15
    df["years_experience"] = df.years_experience.str.replace(r"\D", "", regex=True)
    df["years_experience"] = pd.to_numeric(df.years_experience)

    # "Less than a year" is converted to nan. Convert nan to 0
    df["years_experience"] = df.years_experience.fillna(0)

    # Set up datatypes
    dtypes = dict(
        salary="int",
        bonus="int",
        received_equity="category",
        job_title="category",
        num_employees="category",
        num_subordinates="category",
        sector="category",
        region="category",
        educational_background="category",
        highest_education="category",
        years_experience="int",
        gender="category",
        danish_national="category",
    )
    df = df.astype(dtypes)

    return df

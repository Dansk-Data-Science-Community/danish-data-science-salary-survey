'''Utility functions to be used within the project'''

import pandas as pd
from pathlib import Path

def load_data() -> pd.DataFrame:
    '''Loads the survey data as a dataframe.
    
    Returns:
        Pandas Dataframe:
            The survey data.
    '''

    df = pd.read_csv("data/Danish-Data-Science-Salary-Survey.csv")

    # Discard those who did not want to partake and remove the question
    df = df[df["Do you agree to take part in this survey?"] == "I am happy to take part in this survey"]
    df.drop(["Do you agree to take part in this survey?"], axis=1, inplace=True)

    # Rename cols
    df = df.rename(columns={
        "Timestamp" : "timestamp",
        "What is your monthly salary in DKK, before tax and including pension?": "salary", 
        "How much bonus did you receive last year, in DKK?" : "bonus",
        "Have you received any equity in your company?" : "received_equity",
        "What job title best reflects your daily work?" : "job_title",
        "What tools do you use in your daily work?" : "tools",
        "How many people are employed at your work?" : "num_employees",
        "How many people are you managing at your work?" : "num_subordinates",
        "In which sector do you work?" : "sector", 
        "In which Danish region is your office located?" : "region",
        "What educational background do you have?" : "educational_background",
        "What is your highest level of education?" : "highest_education", 
        "How many years of relevant full-time work experience do you have?" : "years_experience_str",
        "What is your gender?" : "gender", 
        "Are you a Danish national/citizen?" : "danish_national"
        })
    
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    
    # Duplicate years_experience col and convert to numeric. NB! 15+ years will simply be 15
    df["years_experience_float"] = df["years_experience_str"].str.replace(r'\D', '')
    df["years_experience_float"] = pd.to_numeric(df["years_experience_float"])
    # "Less than a year" is converted to nan. Convert nan to 0
    df['years_experience_float'] = df['years_experience_float'].fillna(0)

    return df





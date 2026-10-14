import pandas as pd
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent

CENSORSHIP_DF = pd.read_csv(DATA_DIR/"lgbt_rights"/"censorship-of-lgbt-issues.csv")
SAME_SEX_MARRIAGE_DF = pd.read_csv(DATA_DIR/"lgbt_rights"/"marriage-same-sex-partners-equaldex.csv")
SAME_SEX_LEGAL_DF = pd.read_csv(DATA_DIR/"lgbt_rights"/"same-sex-sexual-acts-legal-mignot.csv")
GENDER_AFFIRMING_CARE_DF = pd.read_csv(DATA_DIR/"lgbt_rights"/"gender-affirming-care.csv")
CHANGE_LEGAL_GENDER_DF = pd.read_csv(DATA_DIR/"lgbt_rights"/"right-to-change-legal-gender-equaldex.csv")
EQUALITY_INDEX_DF = pd.read_csv(DATA_DIR/"lgbt_rights"/"equaldex_equality_index.csv")
COLONIZATION_DF = pd.read_csv(DATA_DIR/"european-overseas-colonies-and-their-colonizers.csv")

MERGE_VARIABLES = ["Entity", "Code", "Year"]

def create_lgbt_rights_df():
    same_sex_df = pd.merge(
        SAME_SEX_LEGAL_DF, 
        SAME_SEX_MARRIAGE_DF,
        on=MERGE_VARIABLES,
        how="left"
        )

    gender_df = pd.merge(
        GENDER_AFFIRMING_CARE_DF,
        CHANGE_LEGAL_GENDER_DF,
        on=MERGE_VARIABLES,
        how="right"
    )

    same_sex_with_censorship_df = pd.merge(
        same_sex_df,
        CENSORSHIP_DF,
        on=MERGE_VARIABLES,
        how="left"
    )

    lgbt_rights_df = pd.merge(
        same_sex_with_censorship_df,
        gender_df,
        on=MERGE_VARIABLES,
        how="left"
    )

    return lgbt_rights_df

def create_lgbt_rights_and_colonial_history_df():
    lgbt_rigths_df = create_lgbt_rights_df()

    combined_df = pd.merge(
        lgbt_rigths_df,
        COLONIZATION_DF,
        on=MERGE_VARIABLES,
        how="right"
    )

    return combined_df


if __name__ == "__main__":
    lgbt_rights_df = create_lgbt_rights_df()
    lgbt_rights_df.to_csv("project/data/lgbt_rights/lgbt_rights_combined.csv")

    combined_df = create_lgbt_rights_and_colonial_history_df()
    combined_df.to_csv("project/data/all_data_combined.csv")
import pandas as pd
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent
LGBT_RIGHTS = "lgbt_rights"

CENSORSHIP_DF = pd.read_csv(DATA_DIR/LGBT_RIGHTS/"censorship-of-lgbt-issues.csv")
SAME_SEX_MARRIAGE_DF = pd.read_csv(DATA_DIR/LGBT_RIGHTS/"marriage-same-sex-partners-equaldex.csv")
SAME_SEX_LEGAL_DF = pd.read_csv(DATA_DIR/LGBT_RIGHTS/"same-sex-sexual-acts-legal-mignot.csv")
GENDER_AFFIRMING_CARE_DF = pd.read_csv(DATA_DIR/LGBT_RIGHTS/"gender-affirming-care.csv")
CHANGE_LEGAL_GENDER_DF = pd.read_csv(DATA_DIR/LGBT_RIGHTS/"right-to-change-legal-gender-equaldex.csv")
EQUALITY_INDEX_DF = pd.read_csv(DATA_DIR/LGBT_RIGHTS/"cleaned_equaldex_equality_index.csv")
COLONIZATION_DF = pd.read_csv(DATA_DIR/"european-overseas-colonies-and-their-colonizers.csv")

MERGE_VARIABLES = ["Entity", "Code", "Year"]


def create_lgbt_rights_df():
    """Merge all of the one-issue Equaldex CSVs"""
    same_sex_df = pd.merge(
        SAME_SEX_LEGAL_DF, 
        SAME_SEX_MARRIAGE_DF,
        on=MERGE_VARIABLES,
        how="outer"
        )

    gender_df = pd.merge(
        GENDER_AFFIRMING_CARE_DF,
        CHANGE_LEGAL_GENDER_DF,
        on=MERGE_VARIABLES,
        how="outer"
    )

    same_sex_with_censorship_df = pd.merge(
        same_sex_df,
        CENSORSHIP_DF,
        on=MERGE_VARIABLES,
        how="outer"
    )

    lgbt_rights_df = pd.merge(
        same_sex_with_censorship_df,
        gender_df,
        on=MERGE_VARIABLES,
        how="outer"
    )

    return lgbt_rights_df

def create_lgbt_rights_and_colonial_history_df():
    """Combine the LGBT rights dataset with the colonial history one."""
    lgbt_rigths_df = create_lgbt_rights_df()

    # Add columns for length of colonization and time since colonization
    # Maybe length of colonization is the current year (2026) minus the first year where Colonizer == "No longer colonized"
    # COLONIZATION_DF["time_since_colonization"]

    combined_df = pd.merge(
        lgbt_rigths_df,
        COLONIZATION_DF,
        on=MERGE_VARIABLES,
        how="outer"
    )

    return combined_df


if __name__ == "__main__":
    lgbt_rights_df = create_lgbt_rights_df()
    lgbt_rights_df.to_csv("project/data/lgbt_rights/lgbt_rights_combined.csv")

    combined_df = create_lgbt_rights_and_colonial_history_df()
    combined_df.to_csv("project/data/all_data_combined.csv")
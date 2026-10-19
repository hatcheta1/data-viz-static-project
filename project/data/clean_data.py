import csv
import pandas as pd
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent
LGBT_RIGHTS = "lgbt_rights"
NOT_COLONIZED = ["Not colonized", "No longer colonized", "Colonizer"]


def clean_equality_index_data():
    """Remove the quotation marks from multi-word values in the Name column"""

    df = pd.read_csv(DATA_DIR/LGBT_RIGHTS/"equaldex_equality_index.csv")
    df["Name"] = df["Name"].astype(str).str.replace('"', '')
    df.to_csv(DATA_DIR/"cleaned"/"cleaned_equaldex_equality_index.csv", index=False)

def clean_colonizer_data():
    """Remove the leading z's from the non-country values in the Colonizer column"""

    df = pd.read_csv(DATA_DIR/"european-overseas-colonies-and-their-colonizers.csv")
    df["Colonizer"] = df["Colonizer"].str.replace(r"^z+\.\s*", "", regex=True)

    return df

def add_length_of_colonization_column(df):
    """Add a column that counts the number of years that a country was colonized"""

    df["is_colonized"] = ~df["Colonizer"].isin(NOT_COLONIZED)

    # total years per country, repeated on every row
    df["Years colonized"] = df.groupby("Entity")["is_colonized"].transform("sum")

    return df

def add_longest_colonizer_column(df):
    """Add a column that names a country's longest colonizer"""
    country_named = df[~df["Colonizer"].isin(NOT_COLONIZED + ["Multiple colonizers"])]

    counts = (country_named.groupby(["Entity", "Colonizer"]).size()
                .reset_index(name="n")
                .sort_values(["Entity", "n", "Colonizer"], ascending=[True, False, True]))

    longest = counts.drop_duplicates("Entity").set_index("Entity")["Colonizer"]

    df["Longest colonizer"] = df["Entity"].map(longest).fillna("None")

    return df


if __name__ == "__main__":
    clean_equality_index_data()

    clean_colonial_history_df = clean_colonizer_data()
    length_added_df = add_length_of_colonization_column(clean_colonial_history_df)
    longest_colonizer_added_df = add_longest_colonizer_column(length_added_df)

    longest_colonizer_added_df.to_csv(DATA_DIR/"cleaned"/"colonizer_data_cleaned.csv", index=False)
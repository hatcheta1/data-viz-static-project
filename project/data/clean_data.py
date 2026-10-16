import csv
import pandas as pd
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent
LGBT_RIGHTS = "lgbt_rights"


def clean_equality_index_data():
    """Remove the quotation marks from multi-word values in the Name column"""

    df = pd.read_csv(DATA_DIR/LGBT_RIGHTS/"equaldex_equality_index.csv")
    df["Name"] = df["Name"].astype(str).str.replace('"', '')
    df.to_csv(DATA_DIR/LGBT_RIGHTS/"cleaned_equaldex_equality_index.csv")

# TODO: remove preceeding Zs in non-country values in colonizer data


if __name__ == "__main__":
    clean_equality_index_data()

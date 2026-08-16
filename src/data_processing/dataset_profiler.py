import pandas as pd


def profile_dataset(df):

    profile = {
        "rows": int(df.shape[0]),
        "columns": int(df.shape[1]),
        "column_names": df.columns.tolist(),
        "missing_values": int(df.isnull().sum().sum()),
        "duplicate_rows": int(df.duplicated().sum()),
    }

    numerical_df = df.select_dtypes(include=["number"])

    categorical_df = df.select_dtypes(exclude=["number"])

    profile["numerical_columns"] = numerical_df.columns.tolist()

    profile["categorical_columns"] = categorical_df.columns.tolist()

    profile["numerical_summary"] = (
        numerical_df.describe().round(2).to_dict()
        if not numerical_df.empty
        else {}
    )

    profile["unique_values"] = {
        column: int(df[column].nunique())
        for column in df.columns
    }

    return profile
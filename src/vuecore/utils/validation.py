import pandas as pd
from typing import List


def validate_columns_exist(df: pd.DataFrame, required_columns: List[str]) -> None:
    """
    Validates that a list of required columns exists in a pandas DataFrame.

    This is a crucial pre-flight check before attempting to create a plot,
    ensuring that all data mappings specified in the configuration are valid.

    Parameters
    ----------
    df : pd.DataFrame
        The pandas DataFrame to check.
    required_columns : List[str]
        A list of column names that must exist in the DataFrame's columns.

    Returns
    -------
    None

    Raises
    ------
    ValueError
        If one or more columns from `required_columns` are not found in the DataFrame.
    """
    missing_cols = [col for col in required_columns if col not in df.columns]
    if missing_cols:
        raise ValueError(
            f"The following required columns are missing from the data: {missing_cols}"
        )

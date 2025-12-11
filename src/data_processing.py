from __future__ import annotations

"""Data processing helpers for ApiPlaygroundPy.

This module contains small utilities focused on working with data
returned from web APIs. They are intentionally minimal yet explicit,
serving mainly as examples that can be extended for real-world use.
"""

from typing import Any, Callable, Iterable, List, Mapping, Sequence

import pandas as pd


def to_dataframe(records: Any) -> pd.DataFrame:
    """Convert API records to a :class:`pandas.DataFrame`.

    Parameters
    ----------
    records:
        Typically a list (or other iterable) of dicts returned by an API
        call like ``ApiPlayground.get``. If a single mapping is passed,
        it is wrapped into a list.

    Returns
    -------
    pandas.DataFrame
        DataFrame representation of the input records.
    """

    if isinstance(records, Mapping):
        records = [records]
    elif not isinstance(records, Iterable) or isinstance(records, (str, bytes)):
        # Fallback: wrap any non-iterable (or string-like) value in a list
        records = [records]

    return pd.DataFrame.from_records(records)  # type: ignore[arg-type]


def select_columns(df: pd.DataFrame, columns: Sequence[str]) -> pd.DataFrame:
    """Return a new DataFrame containing only the specified columns.

    Missing columns raise a :class:`KeyError` as in normal pandas
    column selection.
    """

    return df.loc[:, list(columns)]


def filter_rows(df: pd.DataFrame, predicate: Callable[[pd.DataFrame], Any]) -> pd.DataFrame:
    """Filter rows in *df* using a boolean mask returned by *predicate*.

    The *predicate* receives the full DataFrame and should return a
    boolean-valued Series or array indexable on *df*.

    Examples
    --------
    >>> filter_rows(df, lambda d: d["userId"] == 1)
    """

    mask = predicate(df)
    return df.loc[mask]


def head_as_dicts(df: pd.DataFrame, n: int = 5) -> List[dict]:
    """Return the first *n* rows of *df* as a list of dicts.

    This can be useful for quickly inspecting a DataFrame in contexts
    where plain Python objects are more convenient than tabular output.
    """

    return df.head(n).to_dict(orient="records")

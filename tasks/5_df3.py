import pandas as pd


def make_df3(df1: pd.DataFrame, df2: pd.DataFrame) -> pd.DataFrame:
    df3 = df1.fillna(df2)
    df3 = df3.astype("int64")
    return df3


if __name__ == "__main__":
    df1 = pd.DataFrame({
        "a": [1, 2, 3],
        "b": [None, 5, 6],
        "c": [7, None, 9],
    })
    df2 = pd.DataFrame({
        "b": [4, 89, 87],
        "c": [54, 8, 35],
        "d": [10, 11, 12],
    })

    df3 = make_df3(df1, df2)
    print(df3)

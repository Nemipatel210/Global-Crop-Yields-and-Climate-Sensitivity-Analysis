import pandas as pd
import numpy as np
import country_converter as coco


def load_and_clean_data(filepath="yield_df.csv"):
    """Loads dataset, removes anomalies, applies log transforms, and maps continents."""
    df = pd.read_csv(filepath)

    # Remove unnamed indices if present
    df = df.loc[:, ~df.columns.str.contains("^Unnamed")]

    # Nonlinear transforms: Threshold removal of near-zero pesticide entries
    df = df[df["pesticides_tonnes"] > 1.0].copy()

    # Nonlinear transforms: Log-scale yield axis to compress wide dynamic range
    df["log_yield"] = np.log1p(df["hg/ha_yield"])

    # Merge with continent lookup
    cc = coco.CountryConverter()
    df["Continent"] = cc.pandas_convert(series=df["Area"], to="continent")

    # Create decade column
    df["Decade"] = (df["Year"] // 10) * 10

    return df

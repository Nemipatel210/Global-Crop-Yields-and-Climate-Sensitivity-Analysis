import numpy as np
import pandas as pd
from sklearn.feature_selection import mutual_info_regression
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans


def _detrend_group(group):
    """Polynomial fitting (Degree-2) to find trends and isolate climate signal."""
    years = group["Year"].values
    yields = group["hg/ha_yield"].values

    if len(years) > 2:
        coefs = np.polyfit(years, yields, 2)
        trend = np.polyval(coefs, years)
        group["detrended_yield"] = yields - trend
    else:
        group["detrended_yield"] = yields - np.mean(yields)
    return group


def compute_sensitivities(df):
    """Computes Mutual Information and prepares matrix for PCA."""
    # Group by apply (vectorized over categories, avoids explicit python for-loops)
    df = df.groupby("Item", group_keys=False).apply(_detrend_group)

    results = []
    # MI computation per crop
    for crop, group in df.groupby("Item"):
        if len(group) > 5:
            # sk-learn continuous MI estimator
            mi_temp = mutual_info_regression(
                group[["avg_temp"]], group["detrended_yield"]
            )[0]
            mi_rain = mutual_info_regression(
                group[["average_rain_fall_mm_per_year"]], group["detrended_yield"]
            )[0]
            mi_pest = mutual_info_regression(
                group[["pesticides_tonnes"]], group["detrended_yield"]
            )[0]

            continent = (
                group["Continent"].mode()[0]
                if not group["Continent"].empty
                else "Unknown"
            )
            mean_pest = group["pesticides_tonnes"].mean()

            results.append(
                {
                    "Crop": crop,
                    "Continent": continent,
                    "MI_Temp": mi_temp,
                    "MI_Rain": mi_rain,
                    "MI_Pest": mi_pest,
                    "Mean_Pesticide": mean_pest,
                }
            )

    return pd.DataFrame(results), df


def perform_pca_and_clustering(sens_df, n_components=2, n_clusters=3):
    """PCA & K-means Clustering"""
    features = ["MI_Temp", "MI_Rain", "MI_Pest"]
    X = sens_df[features].values

    # 2. Vectorized NumPy standardization
    X_std = (X - np.mean(X, axis=0)) / np.std(X, axis=0)

    pca = PCA(n_components=n_components)
    components = pca.fit_transform(X_std)

    # K-means clustering to group crop sensitivities
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    clusters = kmeans.fit_predict(X_std)

    res_df = sens_df.copy()
    res_df["PC1"] = components[:, 0]
    res_df["PC2"] = components[:, 1]
    res_df["Cluster"] = clusters

    return res_df, pca


def calculate_climate_sensitivity_index(df):
    """Calculates CSI by country for Geopandas projection."""
    c_index = df.groupby("Area")["detrended_yield"].var().fillna(0).reset_index()
    c_index.columns = ["Area", "Climate_Sensitivity_Index"]

    # Normalize index 0-1 using NumPy
    c_index["Climate_Sensitivity_Index"] = (
        c_index["Climate_Sensitivity_Index"]
        / c_index["Climate_Sensitivity_Index"].max()
    )
    return c_index

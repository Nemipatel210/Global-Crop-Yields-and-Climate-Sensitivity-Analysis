import geopandas as gpd
import geoviews as gv
from geoviews import opts
import pandas as pd

gv.extension("bokeh")


def get_climate_sensitivity_map(csi_df):
    """Plotting EPSG:4326 data on a map using Geopandas and Geoviews."""

    url = "https://naturalearth.s3.amazonaws.com/110m_cultural/ne_110m_admin_0_countries.zip"
    world = gpd.read_file(url)

    world = world.rename(columns={"NAME": "name"})
    # ------------------------------

    # Handle country name variations
    csi_df["Area"] = csi_df["Area"].replace(
        {"United States of America": "United States"}
    )

    # Merge geometries with our CSI calculations
    merged = world.merge(csi_df, left_on="name", right_on="Area", how="left")
    merged["Climate_Sensitivity_Index"] = merged["Climate_Sensitivity_Index"].fillna(0)

    # Render interactive map
    polys = gv.Polygons(merged, vdims=["name", "Climate_Sensitivity_Index"]).opts(
        opts.Polygons(
            color="Climate_Sensitivity_Index",
            cmap="YlOrRd",
            colorbar=True,
            tools=["hover"],
            width=800,
            height=500,
            title="Global Climate Sensitivity Index by Country (EPSG:4326)",
        )
    )
    return polys

import matplotlib.pyplot as plt
import seaborn as sns
import holoviews as hv
import panel as pn
import numpy as np

hv.extension("bokeh")


def plot_detrending_example(df, country="India", crop="Wheat"):
    """Visualizes the methodology of isolating the climate signal from technological growth."""
    # Isolate specific time series
    subset = df[(df["Area"] == country) & (df["Item"] == crop)].sort_values("Year")
    years = subset["Year"].values
    yields = subset["hg/ha_yield"].values

    # Calculate Degree-2 Polynomial trend (Technological growth)
    coefs = np.polyfit(years, yields, 2)
    trend = np.polyval(coefs, years)
    detrended = yields - trend

    # Create a 2-panel Matplotlib figure
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8), sharex=True)

    # Top plot: Raw Yield vs Trend
    ax1.plot(
        years, yields, marker="o", label="Raw Yield", color="steelblue", linewidth=2
    )
    ax1.plot(
        years,
        trend,
        "--",
        color="crimson",
        label="Technological Trend (Degree-2 Fit)",
        linewidth=2,
    )
    ax1.set_ylabel(r"Raw Yield ($\mathrm{hg \cdot ha^{-1}}$)", fontsize=12)
    ax1.set_title(
        f"Methodology: Isolating Climate Signal for {crop} in {country}", fontsize=14
    )
    ax1.legend()
    ax1.grid(True, linestyle=":", alpha=0.6)

    # Bottom plot: The Detrended Residuals (The Climate Anomaly)
    colors = np.where(detrended > 0, "seagreen", "indianred")
    ax2.bar(years, detrended, color=colors, alpha=0.8)
    ax2.axhline(0, color="black", linewidth=1.5)
    ax2.set_ylabel(r"Detrended Anomaly ($\epsilon$)", fontsize=12)
    ax2.set_xlabel("Year", fontsize=12)
    ax2.grid(True, linestyle=":", alpha=0.6)

    plt.tight_layout()
    return fig


def plot_pesticide_paradox(df, crop="Maize"):
    """Visualizes the non-linear relationship requiring Mutual Information."""
    subset = df[df["Item"] == crop]

    fig, ax = plt.subplots(figsize=(9, 6))

    # Seaborn regplot with logx=True forces a logarithmic fit showing diminishing returns
    sns.regplot(
        data=subset,
        x="pesticides_tonnes",
        y="log_yield",
        logx=True,
        scatter_kws={"alpha": 0.3, "color": "gray", "s": 25, "edgecolor": "w"},
        line_kws={"color": "darkorange", "linewidth": 3},
        ax=ax,
    )

    ax.set_title(f"The Pesticide Paradox: Diminishing Returns in {crop}", fontsize=14)
    ax.set_xlabel(r"Pesticide Usage (Tonnes)", fontsize=12)
    ax.set_ylabel(r"$\log(1 + \hat{Y})$ ($\mathrm{hg \cdot ha^{-1}}$)", fontsize=12)
    ax.grid(True, linestyle="--", alpha=0.5)

    plt.tight_layout()
    return fig


def plot_joint_distribution(df, crop_name="Maize"):
    """Joint and marginal distributions using seaborn."""
    crop_data = df[df["Item"] == crop_name]

    g = sns.JointGrid(
        data=crop_data, x="average_rain_fall_mm_per_year", y="log_yield", height=7
    )
    g.plot_joint(sns.scatterplot, s=50, alpha=0.5, edgecolor="w", color="teal")
    g.plot_marginals(sns.histplot, kde=True, color="teal")

    # 4. LaTeX typeset mathematical symbols
    g.set_axis_labels(
        r"Average Rainfall (mm/year)",
        r"$\log(1 + \hat{Y})$ ($\mathrm{hg \cdot ha^{-1}}$)",
        fontsize=12,
    )
    g.figure.suptitle(
        f"Joint Density of Rainfall vs Yield for {crop_name}", y=1.02, fontsize=14
    )
    return g.figure


def plot_pca_biplot(pca_df):
    """PCA Biplot using colors, markers, and sizing for multivariate encoding."""
    plt.figure(figsize=(10, 7))

    sns.scatterplot(
        data=pca_df,
        x="PC1",
        y="PC2",
        hue="Continent",
        size="Mean_Pesticide",
        style="Cluster",  # Uses K-Means results as marker style
        sizes=(50, 500),
        alpha=0.7,
        palette="Set1",
        edgecolor="k",
    )

    plt.title(
        r"PCA Biplot of Crop Sensitivities (Scaled by Pesticide Use)", fontsize=14
    )
    plt.xlabel(r"Principal Component 1 ($I(X_{temp};Y)$ dominant)", fontsize=12)
    plt.ylabel(r"Principal Component 2 ($I(X_{rain};Y)$ dominant)", fontsize=12)
    plt.legend(bbox_to_anchor=(1.05, 1), loc="upper left")
    plt.grid(True, linestyle="--", alpha=0.5)
    plt.tight_layout()
    return plt.gcf()


def interactive_climate_sensitivity(df):
    """Interactive plots using Panel & HoloViews."""

    def create_plot(crop, continent):
        subset = df[(df["Item"] == crop) & (df["Continent"] == continent)]
        if subset.empty:
            return hv.Curve([]).opts(title="No Data Available")

        scatter = hv.Scatter(subset, kdims=["avg_temp"], vdims=["log_yield"]).opts(
            size=8,
            color="crimson",
            alpha=0.6,
            tools=["hover"],
            xlabel="Average Temperature (°C)",
            ylabel="Log Yield",
        )
        return scatter.opts(
            title=f"Climate Sensitivity: {crop} in {continent}", width=650, height=450
        )

    crops = sorted(df["Item"].unique().tolist())
    continents = sorted(df["Continent"].dropna().unique().tolist())

    crop_select = pn.widgets.Select(name="Crop", options=crops, value="Wheat")
    continent_select = pn.widgets.Select(name="Continent", options=continents)

    interactive_plot = pn.bind(
        create_plot, crop=crop_select, continent=continent_select
    )
    return pn.Column(pn.Row(crop_select, continent_select), interactive_plot)

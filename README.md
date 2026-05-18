# Global Crop Yields and Climate Sensitivity Analysis

## Abstract
This project analyzes the growing vulnerability of global agricultural systems to climate change by isolating environmental shocks from human-driven technological advancements. Utilizing the FAO global crop yield dataset (which includes yield, temperature, rainfall, and pesticide usage across decades), this study seeks to identify which crops and regions are most at risk. To achieve this, we applied polynomial detrending to remove technological growth baselines, followed by the calculation of continuous Mutual Information ($I(X;Y)$) to capture the non-linear, diminishing returns of pesticide use. Finally, we utilized Principal Component Analysis (PCA) and K-Means clustering to group crop-continent pairs into specific climate-response profiles, projecting these findings onto an interactive global choropleth map to pinpoint actionable geographic vulnerabilities.

## Overview
This repository contains a comprehensive data science and visualization project that investigates the non-linear relationships between global crop yields, climate variations, and pesticide usage. The primary objective of this analysis is to uncouple human-driven technological growth from natural climate signals to accurately identify which global regions and specific crops are most vulnerable to environmental shocks.

## Methodology
Standard linear correlation fails to accurately capture ecological and chemical dynamics due to inherent non-linearities, such as the diminishing returns of pesticide application (the "Pesticide Paradox"). To address this, the project employs a rigorous statistical pipeline:

1. **Polynomial Detrending:** A Degree-2 Polynomial fit is applied to raw yield time-series data to isolate and remove the baseline of technological progression. The resulting residuals represent pure environmental anomalies.
2. **Mutual Information ($I(X;Y)$):** Continuous Mutual Information estimators are used in place of Pearson correlation to capture both linear and complex non-linear dependencies between climate variables (temperature, rainfall) and detrended crop yields.
3. **Principal Component Analysis (PCA) & Clustering:** High-dimensional sensitivity vectors are reduced to a 2D feature space using PCA. K-Means clustering is then applied to group crop-continent pairs into distinct climate-response profiles.
4. **Geospatial Mapping:** The variance of the detrended yields is aggregated into a global Climate Sensitivity Index (CSI) and projected onto a choropleth map to highlight regional vulnerabilities.

## Repository Structure
To maintain software hygiene and notebook readability, complex logic is abstracted into reusable Python modules.

```text
project_root/
├── README.md                 # Project documentation
├── requirements.txt          # Python dependencies
├── notebook.ipynb            # Main Jupyter Notebook containing the narrative and visualizations
├── yield_df.csv              # Raw dataset
└── modules/                  # Backend logic and processing scripts
    ├── data_loader.py        # Data cleaning, continent mapping, and log transformations
    ├── analysis.py           # Detrending, Mutual Information, and PCA/K-Means logic
    ├── visualization.py      # Matplotlib, Seaborn, and interactive HoloViews/Panel charts
    └── geo_utils.py          # GeoPandas and GeoViews mapping logic

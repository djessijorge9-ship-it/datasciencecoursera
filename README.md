# IBM Applied Data Science Capstone: Falcon 9 Landing Prediction

**Learner:** Djessi Jorge  
**Completed:** 4 August 2026

This repository contains the completed, reproducible analysis for the IBM Applied Data Science Capstone. The project examines historical Falcon 9 launches and builds classification models to estimate whether the first stage will land successfully.

## Key results

- 90 Falcon 9 API records were used for modelling.
- 60 launches landed successfully, giving a historical success rate of 66.67%.
- Logistic Regression, SVM and KNN each achieved 83.33% test accuracy.
- Decision Tree achieved 77.78% test accuracy.
- Logistic Regression was selected as the practical baseline because it ties for the highest accuracy and returns interpretable probabilities.
- Its holdout confusion matrix was `[[3, 3], [0, 12]]`: all 12 successful landings were identified, with three failures over-predicted as successes.

## Reproducible workflow

| Stage | File |
| --- | --- |
| SpaceX API collection | [1_Capstone_Djessi_Jorge_Data_Collection.ipynb](1_Capstone_Djessi_Jorge_Data_Collection.ipynb) |
| Wikipedia web scraping | [2_Capstone_Djessi_Jorge_Webscraping.ipynb](2_Capstone_Djessi_Jorge_Webscraping.ipynb) |
| Data wrangling and feature engineering | [3_Capstone_Djessi_Jorge_Data_Wrangling.ipynb](3_Capstone_Djessi_Jorge_Data_Wrangling.ipynb) |
| SQL exploratory analysis | [4_Capstone_Djessi_Jorge_EDA_SQL.ipynb](4_Capstone_Djessi_Jorge_EDA_SQL.ipynb) |
| Visual exploratory analysis | [5_Capstone_Djessi_Jorge_EDA_Data_Visualization.ipynb](5_Capstone_Djessi_Jorge_EDA_Data_Visualization.ipynb) |
| Folium launch-site analysis | [6_Capstone_Djessi_Jorge_Launch_Site_Location.ipynb](6_Capstone_Djessi_Jorge_Launch_Site_Location.ipynb) |
| Machine-learning comparison | [7_Capstone_Djessi_Jorge_Machine_Learning_Prediction.ipynb](7_Capstone_Djessi_Jorge_Machine_Learning_Prediction.ipynb) |
| Plotly Dash application | [Djessi_Jorge_spacex_dash_app.py](Djessi_Jorge_spacex_dash_app.py) |

## Data files

- `dataset_part_1.csv`: normalised 90-record Falcon 9 API snapshot.
- `dataset_part_2.csv`: cleaned records plus the binary `Class` target.
- `dataset_part_3.csv`: 80-column numeric feature matrix.
- `Spacex.csv` and `spacex_web_scraped.csv`: 101-row historical launch table used for SQL analysis.
- `spacex_launch_geo.csv`: geocoded launch records for Folium.
- `spacex_launch_dash.csv`: dashboard data.

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
jupyter lab
```

To start the dashboard:

```bash
python Djessi_Jorge_spacex_dash_app.py
```

## Data provenance

The analysis uses IBM Skills Network course snapshots of public SpaceX API and Wikipedia launch data. The notebooks keep live-collection code separate from local snapshot execution so the published results remain reproducible if external pages or APIs change.

## Conclusion

Landing success improves strongly with programme experience. Launch site, orbit and booster history add useful context beyond payload mass alone. For a commercial bid, the model probability should support - not replace - expert review, especially because false-positive recovery predictions carry the greatest pricing risk.

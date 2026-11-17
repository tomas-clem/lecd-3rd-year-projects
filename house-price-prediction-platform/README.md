# House Price Prediction Platform ("Prevemos")

A web platform that estimates the market price of a house in Portugal from its location and characteristics. Users can save houses as favourites and follow how their estimated price changes over time, compare the estimate with their own expected price, and explore a choropleth map of the housing market by municipality.

*Group project with Afonso Cordeiro, Daniela Lopes and Óscar Ferrão. Course: Data Science and Engineering Project, University of Coimbra, 2023/24. Developed over a semester with weekly meetings; the requirements and designs are in this folder.*

## How it works

1. **Data collection:** [`Code/Scripts/webscraper.py`](Code/Scripts/webscraper.py) collects house listings from a real estate website and stores them in AWS DynamoDB.
2. **Pre-processing:** [`ScriptPreProcessamento.py`](Code/Scripts/ScriptPreProcessamento.py) and the notebooks in [`Code/F1_Modelos/`](Code/F1_Modelos/) clean the listings, geocode addresses with the Google Maps API, normalise the features and split the data by region.
3. **Models:** one regressor per region where there was enough data (Portalegre, Setúbal, Évora, Beja, Terceira, São Miguel) and a general model for the rest of the country. They are MLP and Gradient Boosting regressors tuned with grid search, saved in [`Code/Scripts/modelos/`](Code/Scripts/modelos/).
4. **Web application:** [`Code/website/`](Code/website/) is a Flask app with user accounts (bcrypt passwords, password recovery by email), price estimation, favourites with price history charts and a choropleth map (Plotly).

| Folder | Contents |
|---|---|
| `Architecture/` | System description and architecture diagram |
| `Requirements/` | Quality attributes (performance, security, testability, usability) |
| `Design/` | Interface mock-ups per use case |
| `Code/` | Scraper, pre-processing, model notebooks, trained models and the web app |

## Running the web app

The app depends on cloud resources that are no longer available, so it cannot run as is. To run it you would need:

- AWS credentials and DynamoDB tables `users`, `recovery`, `favorites` and `houses` in `eu-west-1`.
- A Google Maps API key in place of `{google_maps_api_key}` (in `Code/website/modelo.py` and the templates).
- A Gmail account with an app password for the recovery emails (`Code/website/email_functions.py`).

Then, from `Code/website/`:

```bash
pip install flask boto3 bcrypt googlemaps plotly pandas numpy scipy "scikit-learn==1.3.2" requests
python main.py
```

The trained models load with scikit-learn 1.3.

## Data

The listings were scraped from a real estate website whose terms do not allow redistribution, so the raw and processed datasets are not included. The notebooks keep their outputs.

## Changes from the submitted version

Credentials that were written in the code were replaced by placeholders:

- `{password}`: the Gmail app password in `email_functions.py`.
- `{google_maps_api_key}`: two Google Maps API keys in `modelo.py`, `ScriptPreProcessamento.py`, `Imp_Pre_processamento_d.ipynb`, `favorites.js` and four templates.
- `{gitlab_token}`: a GitLab access token in `Scripts/graficoTempo.py` (used to chart time spent per member from GitLab issues).

Files made smaller:

- `Code/website/static/images/bg.jpg`, the page background, was resized from 5848×3898 to 1920×1280 pixels (13 MB to 0.5 MB).
- `Criar_subdatasets.ipynb` and `Imp_Pre_processamento_d.ipynb` each saved a full copy of the Plotly.js library (3.5 MB) in the output of the cell that first shows a Plotly chart. It was replaced by a link to the same version (2.26.0) on Plotly's CDN, which is what Plotly itself writes in connected mode. The code and all other outputs are unchanged.

## Known limitations

- The Flask secret key is hardcoded in `main.py`, and `email_functions.py` logs in to Gmail when the module is imported.
- `modelo.py` scans the whole `houses` table at start-up.

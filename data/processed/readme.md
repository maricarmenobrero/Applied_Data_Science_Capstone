### `processed/dataset_part_1.csv`

**Description**  
Final dataset for Capstone **Lab 1** (SpaceX Falcon 9). It consolidates past launch records to support EDA and binary classification of first-stage landing outcomes.

**Provenance**  
- SpaceX REST API v4 (e.g., `/launches/past`, with lookups to `/rockets`, `/cores`, `/launchpads`, `/payloads`).  
- Supplemented by web-scraped Wikipedia tables (Falcon 9 launch records) using BeautifulSoup where applicable.

**Wrangling steps (summary)**  
- Filter **Falcon 1** out (keep **Falcon 9** only).  
- Normalize nested JSON → flat table (e.g., `pandas.json_normalize`).  
- Resolve foreign keys (IDs) to human-readable fields (rocket, core, launchpad, payload).  
- Handle missing values:
  - `PayloadMass`: imputed with the **mean**.
  - `LandingPad`: left as `NULL` when no landing pad was used (to be handled later via one-hot encoding).
- Type casting and light renaming for clarity.

**Intended use**  
- EDA (SQL/plots), feature engineering, and as input to classification models (Logistic Regression, SVM, Decision Tree, KNN).  

**Schema (core columns)**

| Column           | Type      | Description                                                             | Example                  |
|------------------|-----------|-------------------------------------------------------------------------|--------------------------|
| `FlightNumber`   | int       | Sequential flight index per program                                     | `96`                     |
| `Date`           | date (parsed from str)  | UTC launch date                                                         | `2019-05-24`            |
| `BoosterVersion` | object       | Falcon 9 block/booster version                                          | `Falcon 9 Block 5`      |
| `PayloadMass`    | float64     | Payload mass in kg (mean-imputed if missing)                            | `13120.0`               |
| `Orbit`          | object       | Target orbit (e.g., `LEO`, `GTO`, `SSO`)                                | `LEO`                    |
| `LaunchSite`     | object       | Launch site short name                                                  | `CCAFS LC-40`           |
| `Outcome`        | object       | Text status for first-stage attempt/result (e.g., `True ASDS`)          | `True ASDS`             |
| `Flights`        | int64       | Number of flights of the same booster                                   | `3`                      |
| `GridFins`       | bool  | Grid fins used (`True`/`False`)                                      | `True`                      |
| `Reused`         | bool  | Booster reused                                                          | `True`                      |
| `Legs`           | bool  | Landing legs deployed                                                   | `True`                      |
| `LandingPad`     | object/NULL  | Landing pad ID or `NULL` if not used                                    | `LZ-1` / `NULL`         |
| `Block`          | float64       | Falcon 9 block number                                                   | `5`                      |
| `ReusedCount`    | int64       | Times the booster has been reused                                       | `2`                      |
| `Serial`         | object       | Booster serial                                                          | `B1056`                 |
| `Longitude`      | float64     | Launch longitude                                                        | `-80.5772`              |
| `Latitude`       | float64     | Launch latitude                                                         | `28.5619`               |

**Attribution & license**  
- SpaceX API data courtesy of SpaceX.  
- Wikipedia tables are available under **CC BY-SA**; cite the specific pages if used.

**Reproducibility**  
- See notebooks under `labs/` (e.g., `01_data_collection.ipynb`, `02_data_wrangling.ipynb`) for code that fetches and builds this dataset.  
- If your environment needs secrets/tokens, copy `.env.example` → `.env` and fill in values (do not commit `.env`).

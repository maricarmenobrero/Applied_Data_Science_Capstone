# `processed/dataset_part_1.csv`

## Description  
Final dataset for Capstone **Lab 1** (SpaceX Falcon 9). A cleaned, analysis-ready dataset with information on Falcon 9 launches.

This file was created during a data lab (**Lab 1**): we started from a broader launch list, filtered out Falcon 1, reindexed flights, and filled a few missing values.

> **Size**: ~90 rows (≈2010–2020) · **File**: dataset_part_1.csv

## What’s inside?

- **Resolve foreign keys** (IDs) to human-readable fields (rocket, core, launchpad, payload).

- **Falcon 9 only**: rows with `BoosterVersion == "Falcon 1"` were removed.

- **Reindexing**: `FlightNumber` was reset to 1…N after filtering.

- **Basic imputation**: `NaN` values in `PayloadMass` were replaced with the **mean** of that column. `LandingPad` was left as `NaN` when no landing pad was used (to be handled later via one-hot encoding).

- **No text normalization**: categorical fields remain as `object` (strings).

## Data dictionary

| Column           | Type                             | Description                                                | Examples / Notes                                    |
| ---------------- | -------------------------------- | ---------------------------------------------------------- | --------------------------------------------------- |
| `FlightNumber`   | `int64`                          | Sequential flight number (reindexed after filtering).      | 1, 2, …, 90                                         |
| `Date`           | `date` (parsed from string) | Launch date (UTC).                                         | `2018-02-06`                                        |
| `BoosterVersion` | `object`                         | Booster model/version.                                     | `Falcon 9 Block 5`, `Falcon 9 Full Thrust`          |
| `PayloadMass`    | `float64`                        | Payload mass in kilograms. `NaN` imputed with column mean. | e.g., 6200.0                                        |
| `Orbit`          | `object`                         | Target orbit.                                              | `LEO`, `ISS`, `GTO`, `SSO`                          |
| `LaunchSite`     | `object`                         | Launch pad/site.                                           | `KSC LC-39A`, `CCAFS LC-40`, `VAFB SLC-4E`          |
| `Outcome`        | `object`                         | Landing outcome (success + method).                        | `True ASDS`, `False ASDS`, `True RTLS`, `None None` |
| `Flights`        | `float64`                        | Cumulative number of flights of the same core.             | 1.0–6.0                                             |
| `GridFins`       | `bool`                           | Whether the booster used grid fins.                        | `True`/`False`                                      |
| `Reused`         | `bool`                           | Whether the core was reused on this flight.                | `True`/`False`                                      |
| `Legs`           | `bool`                           | Whether landing legs were deployed.                        | `True`/`False`                                      |
| `LandingPad`     | `object`                         | Landing zone/drone ship.                                   | `OCISLY`, `JRTI-2`, `LZ-1`, `LZ-4`                  |
| `Block`          | `float64`                        | Core Block version (if applicable).                        | 1.0–5.0                                             |
| `ReusedCount`    | `float64`                        | Total reuse count of the core up to this launch.           | 0.0–5.0                                             |
| `Serial`         | `object`                         | Core serial number.                                        | `B1049`, `B1051`, …                                 |
| `Longitude`      | `float64`                        | Launch site longitude.                                     | −120.61 … −80.58                                    |
| `Latitude`       | `float64`                        | Launch site latitude.                                      | 28.56 … 34.63                                       |


## Attribution & license

- SpaceX API data courtesy of SpaceX.  

Shared **for educational purposes**. If you reuse it in reports/public outputs, please add proper attribution to original sources where applicable. Code in this repo can be released under **MIT** (or your preferred license).

## Contributing

PRs and issues welcome! Ideas:

- Normalize `Outcome` into separate fields

- Add EDA notebooks

- Improve `PayloadMass` imputation strategy

## Reproducibility

- See notebook under `labs/jupyter-labs-spacex-data-collection-api.ipynb` for code that fetches and builds this dataset.  

---

# `processed/spacex_web_scraped.csv`

## Description

A clean CSV with historical SpaceX launch data scraped from Wikipedia as part of a web-scraping lab. It includes flight number, date/time, vehicle/booster, launch site, payload details, orbit, customer, and launch/landing outcomes.

## Schema (columns)

| Column            | Description                                                                          |
| ----------------- | ------------------------------------------------------------------------------------ |
| `Flight No.`      | Sequential flight identifier (as shown on the source page).                          |
| `Date`            | Launch date (string, as displayed on the page; not timezone-normalized).             |
| `Time`            | Launch time (string; may be local/UTC as per source and sometimes empty).            |
| `Version Booster` | Vehicle/booster version (e.g., *Falcon 9 Block 5*, *Falcon Heavy*).                  |
| `Launch site`     | Launch complex (e.g., *CCSFS SLC-40*, *KSC LC-39A*, *VAFB SLC-4E*).                  |
| `Payload`         | Payload name/mission label.                                                          |
| `Payload mass`    | Payload mass in kilograms when available; missing values are left blank/NaN.         |
| `Orbit`           | Target orbit (e.g., *LEO*, *GTO*, *SSO*, *Mars transfer*).                           |
| `Customer`        | Launch customer / operator.                                                          |
| `Launch outcome`  | Outcome of the launch (e.g., *Success*, *Partial failure*, *Failure*).               |
| `Booster landing` | Landing result/status (e.g., *ASDS—Success*, *RTLS—Success*, *Expended*, *Failure*). |


> **Notes**:<br>
> - Dates/times are kept as strings exactly as found.
> - Payload masses are already normalized to kg where provided.
> - Some cells may be empty due to missing or ambiguous source data.
> - This CSV is the direct output of **Lab 2** from the **Applied Data Science Capstone** from IBM (web scraping module).

## How this dataset was built

- **Source**: Public Wikipedia launch list pages for SpaceX missions.

- **Method**: HTML parsing with BeautifulSoup, extracting table rows labeled as launches and mapping each cell to the schema above. Basic helpers handled date/time parsing, payload mass normalization (kg), and landing outcome strings.

- **Environment**: Python (BeautifulSoup4, pandas, requests/`html5lib` or `lxml`).

## Known limitations

- Wikipedia tables evolve; historical edits and formatting changes can introduce gaps or mismatches.

- Timezones are not harmonized; treat `Time` as display text unless you normalize externally.

- Some complex missions (rideshares, dual-stacks) may have multiple payload lines on source pages—only the primary line may be captured.

## License & attribution

- **Data attribution**: Derived from Wikipedia contributors’ launch list pages.

- **License**: Follow Wikipedia’s content licensing for downstream use. If you publish derivatives, include appropriate attribution to Wikipedia contributors and note modifications.

---

# `processed/dataset_part_2.csv`

This CSV is the direct output of **Lab 2: Data Wrangling** from the Capstone **“SpaceX Falcon 9 First Stage Landing Prediction”** (Module 1 – Introduction).

It consolidates launches and creates a binary landing label to be used in the next parts of the project.


## What’s inside

A table of **Falcon 9** launches with rocket, payload, orbit, launch site and mission outcome fields, plus a derived target:

- **`Class` (0/1)** — Binary landing label created from `Outcome`:
  - `1` = landing considered **successful** (per the lab’s rules)
  - `0` = **failed** or **no attempt**

> ***Note***: This file follows the lab’s data-wrangling rules (e.g., excluding certain intermediate categories and normalizing simple text fields). It is intended for educational use in the Capstone.


## Data dictionary

| Column           | Type    | Description                                                                                  |
|------------------|---------|----------------------------------------------------------------------------------------------|
| `FlightNumber`   | int     | Sequential flight number within the Falcon 9 subset.                                         |
| `Date`           | string  | Launch date as text (parseable to datetime/UTC).                                             |
| `BoosterVersion` | string  | Booster model/version (e.g., *Falcon 9 Block 5*).                                            |
| `PayloadMass`    | float   | Payload mass in **kg** (may contain missing values).                                         |
| `Orbit`          | string  | Target orbit (e.g., LEO, ISS, GTO, SSO, …).                                                  |
| `LaunchSite`     | string  | Launch complex/platform (e.g., CCAFS SLC 40, KSC LC 39A, VAFB SLC 4E).                       |
| `Outcome`        | string  | Textual landing outcome (e.g., `True ASDS`, `False ASDS`, `None None`).                      |
| `Flights`        | int     | Cumulative flight count of the same core at that mission.                                    |
| `GridFins`       | bool    | Whether the booster used grid fins.                                                          |
| `Reused`         | bool    | Whether the core was reused on that mission.                                                 |
| `Legs`           | bool    | Whether the booster deployed landing legs.                                                   |
| `LandingPad`     | string  | Landing zone/drone-ship identifier (OCISLY, JRTI-2, LZ-1, etc.).                             |
| `Block`          | float   | Core Block version (1–5).                                                                    |
| `ReusedCount`    | float   | Total reuse count of the core up to that launch.                                             |
| `Serial`         | string  | Core serial number (e.g., B1049).                                                            |
| `Longitude`      | float   | Longitude of the launch site.                                                                |
| `Latitude`       | float   | Latitude of the launch site.                                                                 |
| `Class`          | 0/1     | **Target**: landing success label derived from `Outcome` (1 = success, 0 = failure/no attempt). |


## How this dataset was built (per the lab)

1. Loaded the curated Falcon 9 launches assembled in Lab 1 (data collection).
2. Performed basic cleaning/selection of relevant fields.
3. Computed counts/frequencies by orbit (often **excluding GTO** as it’s a transfer orbit).
4. Converted `Outcome` into a binary **`Class`** label (success vs. non-success) using a set of “bad outcomes” defined in the lab.
5. Saved the result as `dataset_part_2.csv` for downstream EDA/modeling.

## Provenance & license

- **Provenance**: Produced as the final artifact of Lab 2 (Data Wrangling) in the Capstone *SpaceX Falcon 9 First Stage Landing Prediction* (Module 1 – Introduction).

- **Data sources**: Derived from SpaceX/Wikipedia public information as guided by the course.

- **Intended use**: Educational purposes within the Capstone. If you reuse it publicly, please include appropriate attribution to the original sources and note any modifications.




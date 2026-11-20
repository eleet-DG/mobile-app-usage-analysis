# Mobile App Usage & User Engagement Analysis

> **Industry:** Technology / Mobile Applications
> **Author:** Piyush Pal  |  **Admission No.:** 2026B01010868

A complete, modular Python project that studies mobile-app sessions, the
features used, session duration and user ratings in order to understand
engagement and suggest improvements to the user experience.  It covers all 15
tasks of the assignment, produces every required deliverable and is covered by
an automated test-suite.

---

## Highlights

| Deliverable | Where to find it |
|---|---|
| Feature popularity table (top 10) | `outputs/tables/feature_popularity_top10.csv` |
| Device comparison | `outputs/tables/device_comparison.csv` |
| Peak-usage summary (hours + weekdays) | `outputs/tables/peak_hours.csv`, `sessions_by_weekday.csv` |
| Engagement labels (Low / Medium / High) | `outputs/cleaned_app_usage.csv` -> `Engagement_Level` |
| Session statistics (NumPy) | `outputs/tables/duration_statistics.csv` |
| Five app-improvement recommendations | `outputs/analysis_report.md` (section 15) |
| 10 charts | `outputs/figures/` |
| Documents | `docs/SRS_*.pdf`, `docs/Source_Code_*.pdf` |

## Quick start

```bash
# 1. clone and enter the project
git clone https://github.com/<your-username>/mobile-app-usage-analysis.git
cd mobile-app-usage-analysis

# 2. (optional) create a virtual environment
python -m venv .venv && source .venv/bin/activate     # Windows: .venv\Scripts\activate

# 3. install dependencies
pip install -r requirements.txt

# 4. run the whole analysis
python main.py
```

`main.py` options:

```text
--data PATH       CSV to analyse               (default data/24_mobile_app_usage.csv)
--output DIR      folder for results           (default outputs/)
--generate        create a fresh sample CSV first
--seed N          random seed for --generate   (default 42)
--feature NAME    feature for the task-12 function, e.g. --feature "Search"
--no-plots        skip chart creation
--quiet           do not print the full report
```

### Using the real assignment file

The repository ships with a **synthetic sample** `data/24_mobile_app_usage.csv`
(same schema, with injected missing values, duplicate `Session_ID`s and
extreme sessions) so the project runs out of the box.  To analyse the
official file, simply replace it:

```bash
cp /path/to/24_mobile_app_usage.csv data/24_mobile_app_usage.csv
python main.py
```

Required columns: `Session_ID, User_ID, Session_Date, Device_Type, Age_Group,
App_Feature, Session_Duration_Mins, User_Rating`.

> All numbers shown in the generated reports and PDFs come from the sample
> data; they will change when you analyse the real file.

## Task coverage

| # | Task | Module / function |
|---|---|---|
| 1 | Load and inspect | `data_loader.load_dataset`, `inspect_dataset` |
| 2 | Missing values and duplicate `Session_ID`s | `cleaning.missing_value_report`, `duplicate_report` |
| 3 | Justified imputation | `cleaning.impute_missing_values` |
| 4 | Datetime, month, weekday, hour | `feature_engineering.add_time_features` |
| 5 | Sessions, unique users, mean duration | `metrics.compute_headline_metrics` |
| 6 | Top-10 features | `metrics.feature_popularity` |
| 7 | Duration by device | `metrics.device_comparison` |
| 8 | Age-group ranking | `metrics.age_group_ranking` |
| 9 | Rating by feature | `metrics.feature_rating_comparison` |
| 10 | Peak hours and busiest weekdays | `time_analysis.*` |
| 11 | List (top features) and tuple (devices) | `collections_demo.most_used_features_list`, `device_categories_tuple` |
| 12 | Set of users and feature-duration function | `collections_demo.unique_users_set`, `average_duration_for_feature` |
| 13 | NumPy mean / median / std | `stats_numpy.compute_duration_statistics` |
| 14 | IQR outliers and engagement labels | `outliers_engagement.*` |
| 15 | `AppUser` class and recommendations | `models.AppUser`, `recommendations.generate_recommendations` |

## Methodology notes

* **Duplicates** - the first record per `Session_ID` is kept; the report also
  checks whether duplicates are exact copies or conflicting.
* **Missing values** - duration: median of the same *feature + device*
  (fallbacks: feature, global); rating: median of the *feature*, rounded to a
  whole star.  Rows are never dropped and imputed cells are flagged.
* **Outliers** - Tukey rule: duration > `Q3 + 1.5 x IQR`, using
  `numpy.percentile`.
* **Engagement labels** - duration percentiles (Low < P25, High >= P75) with a
  rating adjustment (High needs rating >= 4; a 5-star Low becomes Medium).

## Project structure

```text
mobile-app-usage-analysis/
├── main.py                     # command-line entry point
├── requirements.txt
├── README.md
├── LICENSE
├── app_engagement/             # the analysis package
│   ├── config.py               # constants, paths, categories
│   ├── data_generator.py       # reproducible sample data
│   ├── data_loader.py          # task 1
│   ├── cleaning.py             # tasks 2-3
│   ├── feature_engineering.py  # task 4
│   ├── metrics.py              # tasks 5-9
│   ├── time_analysis.py        # task 10
│   ├── collections_demo.py     # tasks 11-12
│   ├── stats_numpy.py          # task 13
│   ├── outliers_engagement.py  # task 14
│   ├── models.py               # task 15 (AppUser)
│   ├── recommendations.py      # task 15 (recommendations)
│   ├── pipeline.py             # orchestration
│   ├── visualization.py        # charts
│   └── report.py               # console / CSV / Markdown output
├── tests/                      # pytest suite (60 tests)
├── tools/build_pdfs.py         # builds the SRS and source-code PDFs
├── data/                       # input CSV
├── outputs/                    # generated tables, charts, reports
└── docs/                       # SRS.pdf and Source_Code.pdf
```

## Running the tests

```bash
pytest -q
```

## Rebuilding the PDFs

```bash
python tools/build_pdfs.py
```

## Requirements

Python 3.10+ with `pandas`, `numpy`, `matplotlib` (see `requirements.txt`);
`reportlab` is needed only for building the PDFs and `pytest` only for tests.

## License

Released under the MIT License - see [LICENSE](LICENSE).

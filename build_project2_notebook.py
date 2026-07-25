import nbformat as nbf


nb = nbf.v4.new_notebook()
cells = []

cells.append(
    nbf.v4.new_markdown_cell(
        """# AI Programming Foundations Project

Student: Grant Collings

Dataset: Cincinnati Fire Incidents (CAD) including EMS ALS/BLS

This notebook builds a reproducible data workflow using public Cincinnati Fire/EMS CAD incident data. The workflow loads the dataset, inspects its structure, cleans selected fields, performs exploratory data analysis, creates visualizations, and summarizes key findings and limitations."""
    )
)

cells.append(
    nbf.v4.new_markdown_cell(
        """## 1. Import Libraries

This section imports the Python libraries used for data loading, cleaning, analysis, and visualization."""
    )
)

cells.append(
    nbf.v4.new_code_cell(
        """import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

pd.set_option("display.max_columns", None)
pd.set_option("display.width", 120)"""
    )
)

cells.append(
    nbf.v4.new_markdown_cell(
        """## 2. Load the Dataset

The dataset is loaded from the local CSV file included with this repository."""
    )
)

cells.append(
    nbf.v4.new_code_cell(
        """DATA_PATH = "cincinnati_fire_incidents_2025.csv"

df = pd.read_csv(DATA_PATH)

print("Dataset shape:", df.shape)
df.head()"""
    )
)

cells.append(
    nbf.v4.new_markdown_cell(
        """## 3. Initial Data Inspection

This section reviews column names, data types, and missing values before cleaning."""
    )
)

cells.append(
    nbf.v4.new_code_cell(
        """print("Columns:")
print(df.columns.tolist())

print("\\nData types:")
print(df.dtypes)

print("\\nMissing values:")
print(df.isna().sum())"""
    )
)

cells.append(nbf.v4.new_code_cell('df.describe(include="all")'))

cells.append(
    nbf.v4.new_markdown_cell(
        """## 4. Cleaning Functions

Project 2 requires at least two cleaning functions with docstrings. These functions clean text fields and convert incident time columns into datetime values."""
    )
)

cells.append(
    nbf.v4.new_code_cell(
        '''def clean_text_columns(dataframe):
    """Return a copy of the dataframe with selected text columns cleaned.

    This function strips extra spaces and standardizes empty text values as missing values.
    It helps make grouping and counting more consistent during exploratory analysis.
    """
    cleaned = dataframe.copy()
    text_columns = [
        column
        for column in cleaned.columns
        if pd.api.types.is_object_dtype(cleaned[column])
        or pd.api.types.is_string_dtype(cleaned[column])
    ]

    for column in text_columns:
        cleaned[column] = cleaned[column].astype("string").str.strip()
        cleaned[column] = cleaned[column].replace(
            {"": pd.NA, "nan": pd.NA, "None": pd.NA}
        )

    return cleaned


def convert_time_columns(dataframe):
    """Return a copy of the dataframe with incident time columns converted to datetime.

    The source CSV stores time fields as text. Converting them to datetime values allows
    time-based analysis such as incident hour, day of week, and response interval calculations.
    """
    cleaned = dataframe.copy()
    time_columns = [
        "CREATE_TIME_INCIDENT",
        "DISPATCH_TIME_PRIMARY_UNIT",
        "ARRIVAL_TIME_PRIMARY_UNIT",
        "CLOSED_TIME_INCIDENT",
    ]

    for column in time_columns:
        cleaned[column] = pd.to_datetime(
            cleaned[column], format="mixed", errors="coerce"
        )

    return cleaned'''
    )
)

cells.append(
    nbf.v4.new_code_cell(
        """cleaned_df = clean_text_columns(df)
cleaned_df = convert_time_columns(cleaned_df)

print("Cleaned data types:")
print(cleaned_df.dtypes)

print("\\nMissing values after cleaning:")
print(cleaned_df.isna().sum())"""
    )
)

cells.append(
    nbf.v4.new_markdown_cell(
        """## 5. Feature Creation

This section creates simple analysis fields from the cleaned datetime columns."""
    )
)

cells.append(
    nbf.v4.new_code_cell(
        """cleaned_df["incident_hour"] = cleaned_df["CREATE_TIME_INCIDENT"].dt.hour
cleaned_df["incident_day_name"] = cleaned_df["CREATE_TIME_INCIDENT"].dt.day_name()

cleaned_df["dispatch_to_arrival_minutes"] = (
    cleaned_df["ARRIVAL_TIME_PRIMARY_UNIT"]
    - cleaned_df["DISPATCH_TIME_PRIMARY_UNIT"]
).dt.total_seconds() / 60

cleaned_df[
    [
        "CREATE_TIME_INCIDENT",
        "DISPATCH_TIME_PRIMARY_UNIT",
        "ARRIVAL_TIME_PRIMARY_UNIT",
        "incident_hour",
        "incident_day_name",
        "dispatch_to_arrival_minutes",
    ]
].head()"""
    )
)

cells.append(
    nbf.v4.new_markdown_cell(
        """## 6. Exploratory Data Analysis Function

Project 2 requires at least one EDA function. This function summarizes common incident categories, dispositions, neighborhoods, and response-time values."""
    )
)

cells.append(
    nbf.v4.new_code_cell(
        '''def summarize_incident_data(dataframe):
    """Print key exploratory summaries for the incident dataset.

    The function displays dataset size, top incident types, top dispositions,
    top neighborhoods, and response-time summary statistics.
    """
    print("Rows and columns:", dataframe.shape)

    print("\\nTop incident types:")
    print(dataframe["INCIDENT_TYPE_ID"].value_counts(dropna=False).head(10))

    print("\\nTop dispositions:")
    print(dataframe["DISPOSITION_TEXT"].value_counts(dropna=False).head(10))

    print("\\nTop neighborhoods:")
    print(dataframe["NEIGHBORHOOD"].value_counts(dropna=False).head(10))

    print("\\nDispatch-to-arrival minutes:")
    print(dataframe["dispatch_to_arrival_minutes"].describe())


summarize_incident_data(cleaned_df)'''
    )
)

cells.append(
    nbf.v4.new_markdown_cell(
        """## 7. Visualization 1: Top Incident Types

This bar chart compares the 10 most common incident type IDs in the dataset."""
    )
)

cells.append(
    nbf.v4.new_code_cell(
        """top_incident_types = cleaned_df["INCIDENT_TYPE_ID"].value_counts().head(10)

plt.figure(figsize=(10, 6))
top_incident_types.sort_values().plot(kind="barh")
plt.title("Top 10 Cincinnati Fire/EMS Incident Type IDs")
plt.xlabel("Number of Incidents")
plt.ylabel("Incident Type ID")
plt.tight_layout()
plt.show()"""
    )
)

cells.append(
    nbf.v4.new_markdown_cell(
        """### Interpretation

EMS was the largest individual incident category, with 4,792 records, followed by `=FALARM` with 4,278 records. Other leading categories included person-down, accident, and informational calls. The chart therefore shows that the dataset contains a varied mixture of EMS, fire-alarm, person-down, accident, informational, and other incidents rather than one overwhelmingly dominant category.

These labels are operational incident codes rather than fully standardized plain-language categories. Because several more descriptive incident-type fields contain substantial missingness, the categories should be interpreted cautiously."""
    )
)

cells.append(
    nbf.v4.new_markdown_cell(
        """## 8. Visualization 2: Incidents by Hour of Day

This chart shows how recorded incident volume changes by hour of day based on incident creation time."""
    )
)

cells.append(
    nbf.v4.new_code_cell(
        """incidents_by_hour = cleaned_df["incident_hour"].value_counts().sort_index()

plt.figure(figsize=(10, 6))
incidents_by_hour.plot(kind="bar")
plt.title("Cincinnati Fire/EMS Incidents by Hour of Day")
plt.xlabel("Hour of Day")
plt.ylabel("Number of Incidents")
plt.tight_layout()
plt.show()"""
    )
)

cells.append(
    nbf.v4.new_markdown_cell(
        """### Interpretation

Incident volume was not distributed evenly throughout the day. Counts were lower during the overnight and early-morning hours, increased during the daytime, and were highest during the afternoon and evening. This reveals a recognizable time-of-day pattern in the recorded incidents.

The pattern does not establish why demand changes by hour or indicate whether staffing was sufficient. Population activity, commuting, business hours, weather, reporting behavior, incident severity, and other factors may contribute to the observed distribution. The chart is an exploratory description rather than an operational staffing recommendation."""
    )
)

cells.append(
    nbf.v4.new_markdown_cell(
        """## 9. Visualization 3: Dispatch-to-Arrival Time Distribution

This histogram displays dispatch-to-arrival intervals between 0 and 60 minutes. Limiting the displayed range makes the main distribution easier to examine while reducing the visual influence of negative, invalid, or extreme values."""
    )
)

cells.append(
    nbf.v4.new_code_cell(
        """response_times = cleaned_df["dispatch_to_arrival_minutes"].dropna()
response_times = response_times[
    (response_times >= 0) & (response_times <= 60)
]

plt.figure(figsize=(10, 6))
plt.hist(response_times, bins=30)
plt.title("Distribution of Dispatch-to-Arrival Times")
plt.xlabel("Dispatch-to-Arrival Time in Minutes")
plt.ylabel("Number of Incidents")
plt.tight_layout()
plt.show()"""
    )
)

cells.append(
    nbf.v4.new_markdown_cell(
        """### Interpretation

Dispatch-to-arrival times were concentrated in the low single digits, with a median of approximately 4.4 minutes. Most observations were grouped toward the lower end of the displayed range, while fewer incidents had substantially longer intervals. This right-skewed distribution means that the median is more representative of a typical observation than the mean alone because longer-duration records can pull the mean upward.

Filtering improves the readability of the histogram but does not prove that every excluded observation was erroneous. Unusual intervals may reflect exceptional incidents, staging, delayed timestamp entry, documentation practices, or other circumstances requiring further investigation."""
    )
)

cells.append(
    nbf.v4.new_markdown_cell(
        """## 10. Summary and Interpretation

### Initial Findings

1. The dataset contains 97,881 real public Cincinnati Fire/EMS incident records and 17 columns, providing enough data for a meaningful and reproducible workflow.
2. EMS was the largest individual incident category, with 4,792 records, followed by fire alarms with 4,278 records.
3. Incident volume increased during the daytime and was highest during the afternoon and evening.
4. Dispatch-to-arrival times were concentrated in the low single digits, with a median of approximately 4.4 minutes and a smaller number of longer-duration observations.
5. Incident type, disposition, neighborhood, and timestamp fields provide useful structure for exploratory analysis.
6. Several descriptive incident-type fields contain substantial missingness, making cleaning, validation, and careful column selection important.
7. Datetime conversion enables time-based analysis, including incident-hour patterns and dispatch-to-arrival intervals.

### Limitations, Bias, and Assumptions

1. This workflow uses public municipal incident data and does not validate operational accuracy against internal department records.
2. Missing values may reflect documentation practices, system exports, or fields that were not used consistently.
3. Converting blank text to missing values treats all blank entries alike even though they may have different operational meanings.
4. Using more complete fields while excluding mostly missing descriptive fields improves usability but may remove information that is absent systematically for particular incidents.
5. Raw neighborhood counts do not account for population, daytime population, geography, hazards, reporting practices, or other contextual differences.
6. Dispatch-to-arrival time is a simplified interval and should not be treated as a complete performance measure.
7. Filtering the histogram to intervals from 0 to 60 minutes improves readability but does not establish that all excluded values are invalid.
8. This project is limited to data-workflow practice and does not provide clinical, operational, staffing, or deployment recommendations.

### Future Machine-Learning Integration

For machine learning, the workflow would require a clearly defined prediction target, an appropriate unit of analysis, training-validation-test splits, categorical encoding, feature engineering, leakage prevention, baseline models, suitable evaluation metrics, subgroup assessment, and temporal-drift monitoring. Preprocessing steps would need to be fitted only on training data to prevent data leakage.

### Preparing the Pipeline for a Neural Network

For a neural network, the cleaned tabular data would need to be converted into numeric tensors. Continuous features would be scaled, categorical variables would be one-hot encoded or represented through embeddings, and missing-value handling would need to be applied consistently. Reproducible data loaders, batch sizes, random seeds, loss functions, optimization settings, and validation procedures would also be required. Performance should be compared with simpler baseline models because a neural network is not automatically the best approach for structured tabular data.

### Potential Agent Automation

An agent could automate the detection or downloading of new public data releases, schema validation, missingness and duplicate checks, timestamp validation, execution of the cleaning pipeline, regeneration of figures and reports, and preparation of a human-review checklist. The agent should alert a human when validation fails and should not independently delete records, redefine categories, change analytical thresholds, or publish operational conclusions."""
    )
)

nb["cells"] = cells

with open("data_workflow.ipynb", "w", encoding="utf-8") as file:
    nbf.write(nb, file)

print("Created data_workflow.ipynb")

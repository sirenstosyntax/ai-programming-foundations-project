import nbformat as nbf

nb = nbf.v4.new_notebook()

cells = []

cells.append(nbf.v4.new_markdown_cell("""# AI Programming Foundations Project

Student: Grant Collings

Dataset: Cincinnati Fire Incidents (CAD) including EMS ALS/BLS

This notebook builds a reproducible data workflow using public Cincinnati Fire/EMS CAD incident data. The workflow loads the dataset, inspects its structure, cleans selected fields, performs exploratory data analysis, creates visualizations, and summarizes key findings and limitations."""))

cells.append(nbf.v4.new_markdown_cell("""## 1. Import Libraries

This section imports the Python libraries used for data loading, cleaning, analysis, and visualization."""))

cells.append(nbf.v4.new_code_cell("""import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

pd.set_option("display.max_columns", None)
pd.set_option("display.width", 120)"""))

cells.append(nbf.v4.new_markdown_cell("""## 2. Load the Dataset

The dataset is loaded from the local CSV file included with this repository."""))

cells.append(nbf.v4.new_code_cell("""DATA_PATH = "cincinnati_fire_incidents_2025.csv"

df = pd.read_csv(DATA_PATH)

print("Dataset shape:", df.shape)
df.head()"""))

cells.append(nbf.v4.new_markdown_cell("""## 3. Initial Data Inspection

This section reviews column names, data types, and missing values before cleaning."""))

cells.append(nbf.v4.new_code_cell("""print("Columns:")
print(df.columns.tolist())

print("\\nData types:")
print(df.dtypes)

print("\\nMissing values:")
print(df.isna().sum())"""))

cells.append(nbf.v4.new_code_cell("""df.describe(include="all")"""))

cells.append(nbf.v4.new_markdown_cell("""## 4. Cleaning Functions

Project 2 requires at least two cleaning functions with docstrings. These functions clean text fields and convert incident time columns into datetime values."""))

cells.append(nbf.v4.new_code_cell("""def clean_text_columns(dataframe):
    \"\"\"Return a copy of the dataframe with selected text columns cleaned.

    This function strips extra spaces and standardizes empty text values as missing values.
    It helps make grouping and counting more consistent during exploratory analysis.
    \"\"\"
    cleaned = dataframe.copy()
    text_columns = [column for column in cleaned.columns if pd.api.types.is_object_dtype(cleaned[column]) or pd.api.types.is_string_dtype(cleaned[column])]

    for column in text_columns:
        cleaned[column] = cleaned[column].astype("string").str.strip()
        cleaned[column] = cleaned[column].replace({"": pd.NA, "nan": pd.NA, "None": pd.NA})

    return cleaned


def convert_time_columns(dataframe):
    \"\"\"Return a copy of the dataframe with incident time columns converted to datetime.

    The source CSV stores time fields as text. Converting them to datetime values allows
    time-based analysis such as incident hour, day of week, and response interval calculations.
    \"\"\"
    cleaned = dataframe.copy()
    time_columns = [
        "CREATE_TIME_INCIDENT",
        "DISPATCH_TIME_PRIMARY_UNIT",
        "ARRIVAL_TIME_PRIMARY_UNIT",
        "CLOSED_TIME_INCIDENT",
    ]

    for column in time_columns:
        cleaned[column] = pd.to_datetime(cleaned[column], format="mixed", errors="coerce")

    return cleaned"""))

cells.append(nbf.v4.new_code_cell("""cleaned_df = clean_text_columns(df)
cleaned_df = convert_time_columns(cleaned_df)

print("Cleaned data types:")
print(cleaned_df.dtypes)

print("\\nMissing values after cleaning:")
print(cleaned_df.isna().sum())"""))

cells.append(nbf.v4.new_markdown_cell("""## 5. Feature Creation

This section creates simple analysis fields from the cleaned datetime columns."""))

cells.append(nbf.v4.new_code_cell("""cleaned_df["incident_hour"] = cleaned_df["CREATE_TIME_INCIDENT"].dt.hour
cleaned_df["incident_day_name"] = cleaned_df["CREATE_TIME_INCIDENT"].dt.day_name()

cleaned_df["dispatch_to_arrival_minutes"] = (
    cleaned_df["ARRIVAL_TIME_PRIMARY_UNIT"] - cleaned_df["DISPATCH_TIME_PRIMARY_UNIT"]
).dt.total_seconds() / 60

cleaned_df[[
    "CREATE_TIME_INCIDENT",
    "DISPATCH_TIME_PRIMARY_UNIT",
    "ARRIVAL_TIME_PRIMARY_UNIT",
    "incident_hour",
    "incident_day_name",
    "dispatch_to_arrival_minutes"
]].head()"""))

cells.append(nbf.v4.new_markdown_cell("""## 6. Exploratory Data Analysis Function

Project 2 requires at least one EDA function. This function summarizes common incident categories, dispositions, neighborhoods, and response-time values."""))

cells.append(nbf.v4.new_code_cell("""def summarize_incident_data(dataframe):
    \"\"\"Print key exploratory summaries for the incident dataset.

    The function displays dataset size, top incident types, top dispositions,
    top neighborhoods, and response-time summary statistics.
    \"\"\"
    print("Rows and columns:", dataframe.shape)

    print("\\nTop incident types:")
    print(dataframe["INCIDENT_TYPE_ID"].value_counts(dropna=False).head(10))

    print("\\nTop dispositions:")
    print(dataframe["DISPOSITION_TEXT"].value_counts(dropna=False).head(10))

    print("\\nTop neighborhoods:")
    print(dataframe["NEIGHBORHOOD"].value_counts(dropna=False).head(10))

    print("\\nDispatch-to-arrival minutes:")
    print(dataframe["dispatch_to_arrival_minutes"].describe())


summarize_incident_data(cleaned_df)"""))

cells.append(nbf.v4.new_markdown_cell("""## 7. Visualization 1: Top Incident Types

This bar chart shows the most common incident type IDs in the dataset."""))

cells.append(nbf.v4.new_code_cell("""top_incident_types = cleaned_df["INCIDENT_TYPE_ID"].value_counts().head(10)

plt.figure(figsize=(10, 6))
top_incident_types.sort_values().plot(kind="barh")
plt.title("Top 10 Cincinnati Fire/EMS Incident Type IDs")
plt.xlabel("Number of Incidents")
plt.ylabel("Incident Type ID")
plt.tight_layout()
plt.show()"""))

cells.append(nbf.v4.new_markdown_cell("""## 8. Visualization 2: Incidents by Hour of Day

This chart shows how incident volume changes by hour of day based on incident creation time."""))

cells.append(nbf.v4.new_code_cell("""incidents_by_hour = cleaned_df["incident_hour"].value_counts().sort_index()

plt.figure(figsize=(10, 6))
incidents_by_hour.plot(kind="bar")
plt.title("Cincinnati Fire/EMS Incidents by Hour of Day")
plt.xlabel("Hour of Day")
plt.ylabel("Number of Incidents")
plt.tight_layout()
plt.show()"""))

cells.append(nbf.v4.new_markdown_cell("""## 9. Visualization 3: Dispatch-to-Arrival Time Distribution

This histogram shows the distribution of dispatch-to-arrival times. The chart filters to values from 0 to 60 minutes to reduce the effect of extreme or invalid values."""))

cells.append(nbf.v4.new_code_cell("""response_times = cleaned_df["dispatch_to_arrival_minutes"].dropna()
response_times = response_times[(response_times >= 0) & (response_times <= 60)]

plt.figure(figsize=(10, 6))
plt.hist(response_times, bins=30)
plt.title("Distribution of Dispatch-to-Arrival Times")
plt.xlabel("Dispatch-to-Arrival Time in Minutes")
plt.ylabel("Number of Incidents")
plt.tight_layout()
plt.show()"""))

cells.append(nbf.v4.new_markdown_cell("""## 10. Summary and Interpretation

Initial findings:

1. The dataset contains real public Cincinnati Fire/EMS incident records with enough rows and columns for a meaningful data workflow.
2. Incident type, disposition, neighborhood, and timestamp fields provide useful structure for exploratory analysis.
3. Several fields contain substantial missing values, especially some descriptive incident type fields, so cleaning and careful column selection are important.
4. Datetime conversion enables time-based analysis, including incident hour and dispatch-to-arrival intervals.
5. The response-time calculation depends on available dispatch and arrival timestamps, so missing or unusual values should be interpreted cautiously.

Limitations and assumptions:

1. This workflow uses public municipal incident data and does not validate operational accuracy against internal department records.
2. Missing values may reflect documentation practices, system exports, or fields that were not used consistently.
3. Dispatch-to-arrival time is a simplified interval and should not be treated as a complete performance measure.
4. This project is limited to data workflow practice and does not provide clinical, operational, or deployment recommendations.

Future integration:

This workflow could support later statistical analysis, machine learning, demand forecasting, and agentic routing projects by creating a repeatable process for loading, cleaning, validating, and summarizing public incident data before more advanced modeling."""))

nb["cells"] = cells

with open("data_workflow.ipynb", "w", encoding="utf-8") as f:
    nbf.write(nb, f)

print("Created data_workflow.ipynb")


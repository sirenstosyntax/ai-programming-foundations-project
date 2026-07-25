\# Cincinnati Fire/EMS Data Workflow



\## Project Overview



This project builds a reproducible data workflow using public Cincinnati Fire/EMS computer-aided dispatch (CAD) incident data. The workflow loads, cleans, validates, explores, visualizes, and summarizes real municipal incident data using Python, pandas, and Jupyter Notebook.



The project demonstrates foundational data-engineering and analytical practices that could support later machine-learning, deep-learning, or agentic workflows. It does not perform prediction, clinical decision support, or operational deployment.



\## Dataset



\*\*Dataset name:\*\* Cincinnati Fire Incidents (CAD), including EMS ALS/BLS



\*\*Source:\*\* https://data.cincinnati-oh.gov/Safety/Cincinnati-Fire-Incidents-CAD-including-EMS-ALS-BL/vnsz-a3wp



\*\*Local file:\*\* `cincinnati\_fire\_incidents\_2025.csv`



The dataset contains public fire and EMS incident-response records from Cincinnati, Ohio. This project uses the data solely for academic workflow practice. It does not include patient records, departmental records, protected health information (PHI), or clinical outcomes.



\## Workflow



The notebook performs the following steps:



1\. Imports the required Python libraries.

2\. Loads the local CSV dataset.

3\. Inspects its structure, columns, data types, and missing values.

4\. Cleans text fields and converts blank text values to missing values.

5\. Parses date and time fields for analysis.

6\. Removes fields that are unusable because of excessive missingness.

7\. Creates reusable analytical summaries.

8\. Examines incident categories, hourly incident volume, and response-time distributions.

9\. Produces labeled visualizations.

10\. Summarizes the main findings and limitations.



\## Key Findings



The exploratory analysis produced three main observations:



\* EMS was the largest incident category in the analyzed data, with 4,792 records, followed by fire alarms with 4,278 records. This shows that EMS-related demand represented a substantial portion of the incidents in the dataset.

\* Incident volume increased during daytime hours and was highest during the afternoon and evening. This pattern suggests that demand was not evenly distributed throughout the day.

\* Dispatch-to-arrival times were concentrated in the low single digits, with a median of approximately 4.4 minutes. The distribution also included longer-duration observations, so the median provides a more representative measure of a typical response than the mean alone.



These findings describe the analyzed records only. They should not be interpreted as causal conclusions, performance standards, or recommendations for operational staffing.



\## Project Files



\* `data\_workflow.ipynb` — Main notebook for loading, cleaning, exploratory analysis, visualization, and summary.

\* `cincinnati\_fire\_incidents\_2025.csv` — Public dataset used by the notebook.

\* `module\_summary.md` — Source version of the written project summary.

\* `module\_summary.pdf` — Final project summary report.

\* `requirements.txt` — Python dependencies needed to reproduce the workflow.

\* `README.md` — Project overview, instructions, limitations, and reflections.

\* `build\_project2\_notebook.py` — Script used to build or update the notebook reproducibly.

\* `create\_module\_summary\_pdf.py` — Script used to generate the PDF report.

\* `sanitize\_report\_text.py` — Utility for preparing report text safely for PDF generation.



\## How to Run



1\. Clone or download this repository.

2\. Open a terminal in the project folder.

3\. Install the required dependencies:



```bash

pip install -r requirements.txt

```



4\. Start Jupyter Notebook:



```bash

jupyter notebook

```



5\. Open `data\_workflow.ipynb`.

6\. Run the notebook from top to bottom.



The notebook expects `cincinnati\_fire\_incidents\_2025.csv` to be located in the project’s root directory.



\## Data Quality, Bias, and Reliability



The results depend on the completeness and accuracy of the source CAD data. Records may contain missing values, inconsistent text labels, reporting differences, data-entry errors, duplicate or revised incidents, and extreme response-time values. The dataset represents recorded incidents rather than every underlying community need or event.



Workflow decisions can also influence the results:



\* Dropping fields with extensive missingness improves usability but may remove information that is systematically absent for particular incident types, locations, or circumstances.

\* Converting blank text entries to missing values makes the data more consistent, but it treats all blank values alike even though some may have different operational meanings.

\* Grouping or standardizing incident labels can simplify analysis while hiding distinctions between detailed incident subtypes.

\* Comparing raw neighborhood incident counts can favor neighborhoods with larger populations or more recorded calls. Population-adjusted rates would be needed for fair comparisons of relative incident burden.

\* Removing records with missing or invalid timestamps may disproportionately exclude certain incidents and change time-based findings.

\* Extreme response times may be legitimate events, data-entry problems, or artifacts of how timestamps were recorded. Automatically removing them without investigation could bias the distribution.

\* CAD timestamps measure recorded workflow events and may not capture every operational circumstance affecting an incident.



For these reasons, the analysis is descriptive and should not be used by itself to evaluate personnel, compare neighborhood performance, make clinical conclusions, or guide resource allocation. Any operational use would require additional validation, domain review, documentation, and appropriate governance.



\## Future Machine-Learning Integration



To adapt this workflow for machine learning, the project would need a clearly defined prediction target and an appropriate unit of analysis. The data would then be divided into training, validation, and test sets. Preprocessing steps would need to be fitted only on training data to prevent data leakage.



Additional work would include encoding categorical variables, engineering time and location features, handling class imbalance, selecting suitable evaluation metrics, comparing baseline models, examining subgroup performance, and monitoring for temporal drift. Features unavailable at the intended prediction time would need to be excluded.



\## Preparing the Tabular Pipeline for a Neural Network



A neural-network workflow would convert the cleaned table into numeric tensors. Continuous variables would be scaled, categorical variables would be one-hot encoded or represented with learned embeddings, and missing-value handling would be applied consistently.



The pipeline would also define reproducible data loaders, batch sizes, random seeds, loss functions, optimization settings, and validation procedures. Model performance should be compared with simpler baseline methods because a neural network is not automatically the best choice for structured tabular data.



\## Potential Agent Automation



An agent could automate several repeatable workflow tasks while keeping consequential decisions under human review. Possible tasks include:



\* Downloading or detecting new public data releases.

\* Confirming the expected file name and schema.

\* Validating required columns and data types.

\* Checking missingness, duplicate records, invalid timestamps, and unexpected category changes.

\* Running the cleaning and summary pipeline.

\* Regenerating figures and reports.

\* Recording validation results and creating a review checklist.

\* Alerting a human when the dataset fails a quality threshold or when the schema changes.



The agent should not silently delete records, redefine incident categories, alter analytical thresholds, or publish operational conclusions. Those actions require documented rules and human approval.



\## Scope and Limitations



This project is limited to academic data-workflow practice. It does not perform machine learning, prediction, clinical decision support, personnel evaluation, or operational deployment. Its outputs should not be interpreted as medical advice or as an assessment of Cincinnati Fire Department performance.




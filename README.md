# Bachelor's Thesis

This thesis uses the DEPAR dataset provided by CICERO to determine the best predictor columns to impute the missing values of the SF-36 questionnaire.

## File Structure

This repository has multiple files, with their respective descriptions below:
- `find_correlation_and_threshold.py`: A Python file that preprocesses the data by encoding the categorical values, finding the correlations, and generating CSV files of columns and their values that meet the requirement for the thresholds
- `imputation.r`: An R file that uses MICE with PMM to impute the missing data, then generates a CSV file of a joined dataset containing multiple imputed datasets with no missing values
- `evaluation.py`: A Python file that evaluates the performance of the imputation by calculating the metrics and generating density plots
- `correlation.csv`: A CSV file generated from `find_correlation_and_threshold.py` containing the correlations of all the target columns and the predictor columns
- `comparison.csv`: A CSV file generated from `evaluation.py` containing the metrics of the imputations

## Instructions

### Step 1: Preprocessing

Assuming a stable connection has been set up to access the dataset, run `find_correlation_and_threshold.py` in a Python environment

### Step 2: Imputation

After step 1 has been finished, run `imputation.r` in an R environment

### Step 3: Evaluation

After step 2 has been finished, run `evaluation.py` in a Python environment

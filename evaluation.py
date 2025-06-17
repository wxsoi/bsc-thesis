import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

file_path = "file path of the dataset"
full = pd.read_stata(file_path)
folder_path = 'imputed/'
summary_list = []

# loop through each CSV with the imputed dataset in the folder
for filename in os.listdir(folder_path):
    if filename.endswith('.csv'):
        # get the target column and threshold
        target_column = filename.split('_')[0] + "_a"
        threshold = filename.split('_')[2].replace("threshold", "")

        # read each CSV file as a dataframe
        file_path = os.path.join(folder_path, filename)
        df = pd.read_csv(file_path)

        # find the rows with missing values of the target column
        missing_rows = full[full[target_column].isna()].index.tolist()
        missing_rows = [i + 1 for i in missing_rows]
        df = df[df['.id'].isin(missing_rows)]

        # find the rows with observed values of the target column
        observed = full[full[target_column].notna()]

        # calculate the metrics for the imputed values
        mean_imputed = df[target_column].mean()
        median_imputed = df[target_column].median()
        std_imputed = df[target_column].std()
        iqr_imputed = df[target_column].quantile(0.75) - df[target_column].quantile(0.25)
    
        # calculate the metrics for the observed values
        mean = observed[target_column].mean()
        median = observed[target_column].median()
        std = observed[target_column].std()
        iqr = observed[target_column].quantile(0.75) - observed[target_column].quantile(0.25)

        # append the calculated metrics into a list
        summary_list.append({
            'target_column': target_column,
            'threshold': threshold,
            'mean_imputed': round(mean_imputed, 2),
            'mean_observed': round(mean, 2),
            'mean_diff': round(mean_imputed - mean, 2),
            'median_imputed': round(median_imputed, 2),
            'median_observed': round(median, 2),
            'median_diff': round(median_imputed - median, 2),
            'std_imputed': round(std_imputed, 2),
            'std_observed': round(std, 2),
            'std_diff': round(std_imputed - std, 2),
            'iqr_imputed': round(iqr_imputed, 2),
            'iqr_observed': round(iqr, 2),
            'iqr_diff': round(iqr_imputed - iqr, 2)
        })

        # create a graph for the comparison
        sns.kdeplot(df[target_column], label=f'Imputed with threshold {threshold}', fill=True, alpha=0.5)
        sns.kdeplot(observed[target_column], label='Observed', fill=True, alpha=0.5)
        plt.xlabel(f'Values of imputed and observed {target_column}')
        plt.title(f'Density comparison for {target_column} with threshold {threshold}')
        plt.ylim(0, 0.1)
        plt.legend(loc='upper left')
        plt.savefig(f'plots/{target_column}_{threshold}_distribution.png', dpi=300, bbox_inches='tight')
        plt.clf()

# output the list of metrics for each target column and threshold as a CSV
compare = pd.DataFrame(summary_list)
compare.to_csv("comparison.csv", index=False)

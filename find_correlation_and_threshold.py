import pandas as pd

def one_hot_encode(df, columns):
    """
    Function that one hot encodes the columns with categorical values
    :param df: The dataframe to be encoded
    :param columns: The categorical columns that need to be one hot encoded
    :return: An one hot encoded dataframe
    """
    # one hot encoding
    encoded = pd.get_dummies(df, columns=columns)
    # replace true/false with 1/0
    encoded = encoded.replace({True: 1, False: 0})
    encoded = encoded.drop(columns=['respondentid', 'mm'])
    return encoded


def calc_correlation(df):
    """
    Function to calculate the Pearson correlations between the columns and SF-36 related columns
    :param df: The dataframe that needs to have its columns' Pearson correlations calculated
    :return: A dataframe of correlations calculated against SF-36 related columns
    """
    # round correlation to 2 decimal points
    correlation = df.corr()[df.corr().index.astype(str).str.startswith('sf')].round(2)
    correlation.to_csv("correlation.csv")
    return correlation


def find_threshold(df, threshold, target_column):
    """
    Function finds the columns that are >= the threshold
    :param df: The dataframe with correlations
    :param threshold: The threshold for the correlation
    :param target_column: The targets column to be imputed
    :return: Returns a list of columns that are >= the threshold
    """
    predictor_columns = []
    for col, value in df.items():
        # uses absolute correlation
        if abs(value) >= threshold:
            predictor_columns.append(col)
    predictor_columns.append(target_column)
    return predictor_columns


categorical_columns = ['fa20_T0', 'fa21_T0', 'fa22_T0', 'Geslacht_T0', 'fa04_T0',
                          'fa15_T0', 'fa16_T0', 'pm112_T0', 'gp01', 'gp02', 'gp03', 'gp04',
                          'gp05', 'gp06', 'gp07', 'gp08', 'gp09', 'gp10', 'gp11', 'gp12']

file_path = "redacted"
df = pd.read_stata(file_path)

# one hot encodes columns with categorical values
df = one_hot_encode(df, categorical_columns)

# find the correlations between other columns and SF-36 questionnaire columns
correlation = calc_correlation(df)

# find the columns >= threshold for each SF-36 questionnaire column
for target_column in ['sf36pf_a', 'sf36rp_a', 'sf36bp_a', 'sf36gh_a',
                      'sf36vi_a', 'sf36sf_a', 'sf36re_a', 'sf36mh_a']:

    # only takes the row of the targets column
    target = correlation.loc[target_column]

    # remove the correlation of the targets column against itself
    target = target.drop(target_column)

    # create a CSV file for each threshold of each SF-36 questionnaire column
    for threshold in [0, 0.1, 0.2, 0.4, 0.5]:
        predictor_columns = find_threshold(target, threshold, target_column)

        # filters the df to only have predictor columns
        predictors = df[predictor_columns]

        # columns with 12.5% missing data
        if (target_column == 'sf36pf_a' or target_column == 'sf36rp_a'
            or target_column == 'sf36bp_a' or target_column == 'sf36gh_a'):
            predictors.to_csv("targets/" + target_column + "_threshold" + str(threshold) + "_13.csv")

        # columns with 31.2% missing data
        else:
            predictors.to_csv("targets/" + target_column + "_threshold" + str(threshold) + "_31.csv")
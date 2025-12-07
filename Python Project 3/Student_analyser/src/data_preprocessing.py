import pandas as pd
from sklearn.preprocessing import LabelEncoder

def preprocess_data(filepath):
    df = pd.read_csv(filepath)
    df.dropna(inplace=True)


    label_cols = ['school', 'sex', 'address', 'famsize', 'Pstatus']
    encoder = LabelEncoder()
    for col in label_cols:
        df[col] = encoder.fit_transform(df[col])

    df.to_csv(r'C:\Users\KEERTHAN\OneDrive\Documents\GitHub\Keerthan-Projects\Python Project 3\Student_analyser\data\student_por_cleaned1.csv', index=False)
    return df

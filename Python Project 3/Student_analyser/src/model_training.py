import os
import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score, mean_absolute_error
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import TransformedTargetRegressor


def train_model():
    RAW_CSV = r"C:\Users\KEERTHAN\OneDrive\Documents\GitHub\Keerthan-Projects\Python Project 3\Student_analyser\data\student-por.csv"

    df = pd.read_csv(RAW_CSV)

    if 'G3' not in df.columns:
        raise RuntimeError('Expected column G3 in raw CSV')

    X = df.drop(columns=['G3'])
    y = df['G3'].astype(float)

    categorical_cols = [
        'school', 'sex', 'address', 'famsize', 'Pstatus', 'Mjob', 'Fjob',
        'reason', 'guardian', 'schoolsup', 'famsup', 'paid', 'activities',
        'nursery', 'higher', 'internet', 'romantic'
    ]

    numeric_cols = [c for c in X.columns if c not in categorical_cols]

    preprocessor = ColumnTransformer(
        transformers=[
            ('num', StandardScaler(), numeric_cols),
            ('cat', OneHotEncoder(handle_unknown='ignore', sparse_output=False), categorical_cols),
        ],
        remainder='drop',
        sparse_threshold=0,
    )

    base_reg = RandomForestRegressor(n_estimators=200, random_state=42)

    ttr = TransformedTargetRegressor(regressor=base_reg, transformer=StandardScaler())

    pipeline = Pipeline([
        ('preprocessor', preprocessor),
        ('regressor', ttr),
    ])

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    pipeline.fit(X_train, y_train)

    preds = pipeline.predict(X_test)

    print('R2 Score:', r2_score(y_test, preds))
    print('MAE:', mean_absolute_error(y_test, preds))

    save_path = os.path.join(os.path.dirname(__file__), '..', 'models', 'pipeline.pkl')
    save_path = os.path.abspath(save_path)
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    joblib.dump(pipeline, save_path, compress=3)

    print(f'Model pipeline saved successfully at: {save_path}')


if __name__ == '__main__':
    train_model()

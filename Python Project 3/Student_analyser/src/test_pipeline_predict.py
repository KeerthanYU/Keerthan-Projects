import joblib
import pandas as pd
import os

PIPELINE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'models', 'pipeline.pkl'))
RAW_CSV = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data', 'student-por.csv'))

if not os.path.exists(PIPELINE_PATH):
    raise SystemExit(f"Pipeline not found at {PIPELINE_PATH}. Run `python src/model_training.py` first.")

pipeline = joblib.load(PIPELINE_PATH)
print('Loaded pipeline from', PIPELINE_PATH)

# Load raw CSV and build a sample input using medians/modes
if not os.path.exists(RAW_CSV):
    raise SystemExit(f"Raw CSV not found at {RAW_CSV}")

df_raw = pd.read_csv(RAW_CSV)

template = {}
for col in df_raw.columns:
    if col == 'G3':
        continue
    if pd.api.types.is_numeric_dtype(df_raw[col]):
        template[col] = float(df_raw[col].median())
    else:
        try:
            template[col] = df_raw[col].mode().iloc[0]
        except Exception:
            template[col] = df_raw[col].iloc[0]

# Example user inputs
template['studytime'] = 2  # category (1-4)
template['absences'] = 3
template['health'] = 3
template['failures'] = 0

feature_cols = [c for c in df_raw.columns if c != 'G3']
input_df = pd.DataFrame([template], columns=feature_cols)

# Standardized prediction (internal regressor prediction)
preproc = pipeline.named_steps.get('preprocessor')
reg_ttr = pipeline.named_steps.get('regressor')
X_trans = preproc.transform(input_df)
std_pred = None
if hasattr(reg_ttr, 'regressor_'):
    std_pred = float(reg_ttr.regressor_.predict(X_trans)[0])

final_pred = float(pipeline.predict(input_df)[0])

print('Standardized model output:', std_pred)
print('Inverted final grade (0-20):', final_pred)

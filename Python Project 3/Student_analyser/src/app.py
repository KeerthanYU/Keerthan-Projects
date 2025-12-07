import os
import joblib
import pandas as pd
import numpy as np
import streamlit as st

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
MODEL_PATH = os.path.join(BASE_DIR, "models", "pipeline.pkl")
LEGACY_MODEL_PATH = os.path.join(BASE_DIR, "models", "best_model1.pkl")
DATA_CSV = os.path.join(BASE_DIR, "data", "student-por.csv")

st.set_page_config(page_title="Smart Student Performance", layout="centered")

CSS = """
<style>
body { color: #222; }
.big-title {font-size:48px; font-weight:800; color:#222; margin:0;}
.big-sub {font-size:28px; color:#222; margin-top:6px;}
/* red slider accent */
input[type=range] { accent-color: #ff4757; }
.input-box { background:#f1f3f5; border-radius:10px; padding:10px 14px; }
.predict-btn { border-radius:10px; padding:10px 18px; background:transparent; }
.result-banner { background:#0b57d0; color:white; padding:12px 18px; border-radius:6px; display:inline-block; font-size:28px; font-weight:700; }
.label-small { color:#333; margin-bottom:6px; }
.spacer { height:18px }
.container { max-width:900px; margin-left:auto; margin-right:auto }
</style>
"""

def load_pipeline(path):
    if not os.path.exists(path):
        return None
    try:
        return joblib.load(path)
    except Exception:
        return None

def get_feature_template(df):
    cols = [c for c in df.columns if c != "G3"]
    template = {}
    for c in cols:
        if pd.api.types.is_numeric_dtype(df[c]):
            template[c] = float(df[c].median())
        else:
            modes = df[c].mode()
            template[c] = modes.iat[0] if not modes.empty else ""
    return cols, template

def build_full_row(feature_cols, template, user_inputs):
    row = {}
    for c in feature_cols:
        if c in user_inputs:
            row[c] = user_inputs[c]
        else:
            row[c] = template[c]
    for c in feature_cols:
        try:
            if isinstance(template[c], float) or isinstance(template[c], (int, np.integer, np.floating)):
                row[c] = float(row[c])
        except Exception:
            pass
    return pd.DataFrame([row], columns=feature_cols)

def main():
    st.markdown(CSS, unsafe_allow_html=True)
    pipeline = load_pipeline(MODEL_PATH)
    legacy = None
    if pipeline is None and os.path.exists(LEGACY_MODEL_PATH):
        try:
            legacy = joblib.load(LEGACY_MODEL_PATH)
        except Exception:
            legacy = None

    if not os.path.exists(DATA_CSV):
        st.error("Training CSV not found: " + DATA_CSV)
        return

    df = pd.read_csv(DATA_CSV)
    feature_cols, template = get_feature_template(df)

    st.markdown("<div class='container'><div style='display:flex;align-items:center;gap:18px;margin-bottom:6px'><div style='font-size:44px'>🎓</div><div><h1 class='big-title'>Smart Student Performance</h1><div class='big-sub'>Analyze & Predictor</div></div></div>", unsafe_allow_html=True)

    st.markdown("<div class='spacer'></div>", unsafe_allow_html=True)

    st.markdown("<div class='container'>", unsafe_allow_html=True)

    st.markdown("<div class='label-small'>Daily Study Time (hours)</div>", unsafe_allow_html=True)
    study_time = st.slider("", min_value=0, max_value=10, value=3, key='study_time')
    st.markdown("<div class='spacer'></div>", unsafe_allow_html=True)

    st.markdown("<div class='label-small'>Number of Absences</div>", unsafe_allow_html=True)
    absences = st.number_input("", min_value=0, max_value=200, value=int(template.get("absences", 0)), key='absences', format='%d')
    st.markdown("<div class='spacer'></div>", unsafe_allow_html=True)

    st.markdown("<div class='label-small'>Health (1=Poor, 5=Excellent)</div>", unsafe_allow_html=True)
    health = st.slider("", 1, 5, int(template.get("health", 3)), key='health')
    st.markdown("<div class='spacer'></div>", unsafe_allow_html=True)

    st.markdown("<div class='label-small'>Number of Past Failures</div>", unsafe_allow_html=True)
    failures = st.number_input("", min_value=0, max_value=10, value=int(template.get("failures", 0)), key='failures', format='%d')

    st.markdown("<div class='spacer'></div>", unsafe_allow_html=True)
    predict_btn = st.button("Predict Performance")

    if predict_btn:
        user_inputs = {}
        user_inputs["studytime"] = int(np.clip(round(study_time / 2), 1, 4))
        user_inputs["absences"] = int(absences)
        user_inputs["health"] = int(health)
        user_inputs["failures"] = int(failures)
        user_inputs["G1"] = float(template.get("G1", 10.0))
        user_inputs["G2"] = float(template.get("G2", 10.0))

        input_df = build_full_row(feature_cols, template, user_inputs)

        if pipeline is not None:
            try:
                pred = pipeline.predict(input_df)[0]
                st.markdown(f"<div style='margin-top:18px'><div class='result-banner'>Predicted Final Grade: {pred:.2f}</div></div>", unsafe_allow_html=True)
            except Exception as e:
                st.error(f"Pipeline prediction failed: {e}")
        elif legacy is not None:
            try:
                if hasattr(legacy, "feature_names_in_"):
                    cols_for_legacy = [c for c in input_df.columns if c in legacy.feature_names_in_.tolist()]
                else:
                    cols_for_legacy = input_df.columns[:4]
                X_legacy = input_df[cols_for_legacy]
                pred = legacy.predict(X_legacy)[0]
                st.markdown(f"<div class='result-banner'>Predicted Final Grade (legacy): {pred:.2f}</div>", unsafe_allow_html=True)
            except Exception as e:
                st.error(f"Legacy model prediction failed: {e}")
        else:
            st.warning("No model found. Train a pipeline with `python src/model_training.py` to create `models/pipeline.pkl`.")

        suggestions = []
        if study_time < 2:
            suggestions.append("Increase daily study time to at least 2 hours.")
        if absences > 5:
            suggestions.append("Reduce absences; attend more classes for better performance.")
        if failures > 0:
            suggestions.append("Focus on weak subjects and seek help to avoid repeat failures.")
        if health < 3:
            suggestions.append("Improve sleep and nutrition to boost concentration.")

        st.markdown("<div style='margin-top:22px'><h3>Personalized Suggestions:</h3></div>", unsafe_allow_html=True)
        if suggestions:
            for s in suggestions:
                st.write("- ", s)
        else:
            st.write("- You're on track! Keep maintaining your study habits.")

    st.markdown("</div>", unsafe_allow_html=True)

if __name__ == '__main__':
    main()
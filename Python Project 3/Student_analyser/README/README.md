# 🎓 Smart Student Performance Analyzer & Predictor

## 📘 Overview
An AI-powered system that analyzes and predicts student performance using Machine Learning, and provides personalized study recommendations.

## ⚙️ Features
- Data cleaning and analysis (EDA)
- Grade prediction using Random Forest
- Smart study recommendations (AI logic)
- Interactive dashboard with Streamlit

## 🧠 Tech Stack
Python, Pandas, Scikit-learn, Streamlit, Matplotlib, Seaborn

## 🚀 How to Run
1. Clone this repository  
2. Install dependencies: `pip install -r requirements.txt`  
3. Run: `streamlit run src/app.py`

## 🔧 Troubleshooting: Model loading / prediction errors

If the app fails to load the saved model or you see errors like "InconsistentVersionWarning" or
"ValueError: The feature names should match those that were passed during fit", follow these steps.

Reproduce the error
- From the project root run:

```powershell
streamlit run src/app.py
```

Common causes and recommended fixes
- Option A — Install the scikit-learn version used to save the model (quickest)

```powershell
python -m pip install --upgrade pip
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r Requirements\requirements.txt
python -m pip install "scikit-learn==1.6.1"
streamlit run src/app.py
```

- Option B — Re-save the model using your current scikit-learn (safer long-term)

1. Create a temporary environment with the older scikit-learn (1.6.1), load the existing pickle, and re-save it as a plain pipeline or re-dump after re-training in your current environment.

Example (run in environment with scikit-learn 1.6.1):

```python
import joblib
model = joblib.load('models/best_model.pkl')
# Optionally re-save so it can be reloaded in newer sklearn
joblib.dump(model, 'models/best_model_resaved.pkl')
```

Then switch back to your regular environment (with newer scikit-learn) and try loading `best_model_resaved.pkl`. If that still fails, retrain the model in your current environment (Option C).

- Option C — Retrain and save a complete sklearn Pipeline (recommended)

1. Update `src/model_training.py` to build and save a `sklearn.pipeline.Pipeline` or `ColumnTransformer` that includes all preprocessing (encoders, scalers) and the estimator.
2. Save that pipeline with `joblib.dump(pipeline, 'models/pipeline.pkl')` and in `src/app.py` call `pipeline.predict(...)` directly. This avoids manual feature/encoder mismatches at inference time.

Why this helps
- Matching scikit-learn versions prevents unpickling of objects that moved or changed internally.
- Saving a full pipeline (preprocessor + model) ensures the exact feature transformations used at training are applied consistently at inference.

If you want, I can add a small script to save a proper pipeline and update `src/app.py` to load it. — tell me which option you prefer and I will implement it.

## 📊 Example Output
- Predicted Final Grade  
- Personalized AI Suggestions  
- Visual Insights and Correlations

## 👨‍💻 Author
Keerthan Y U

# router_ml_classifier.py
import time
import re
import joblib
import pickle
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import VotingClassifier
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score
from xgboost import XGBClassifier
from catboost import CatBoostClassifier

# ---------------------
# 1. Load & Preprocess
# ---------------------
print("📂 Loading dataset...")
df = pd.read_csv("Router_Dataset.csv")

if 'question' not in df.columns or 'llm' not in df.columns:
    raise ValueError("CSV must contain 'question' and 'llm' columns.")

print(f"✅ Loaded {len(df)} rows.")

# Clean text (same normalization as used elsewhere)
print("🧹 Cleaning text...")
df['text_clean'] = df['question'].str.lower().str.replace(r'[^\w\s]', '', regex=True)

X = df['text_clean']
y = df['llm'].astype(int)

# ---------------------
# 2. Define Models
# ---------------------
print("⚙️ Initializing models...")
xgb = XGBClassifier(
    n_estimators=100,
    max_depth=5,
    learning_rate=0.1,
    subsample=0.8,
    colsample_bytree=0.8,
    eval_metric='mlogloss',
    verbosity=1,
    tree_method='hist',
    use_label_encoder=False
)

cat = CatBoostClassifier(
    iterations=200,
    depth=6,
    learning_rate=0.1,
    loss_function='MultiClass',
    verbose=50
)

ensemble = VotingClassifier(
    estimators=[('xgb', xgb), ('cat', cat)],
    voting='soft'
)

# ---------------------
# 3. Create Pipeline
# ---------------------
pipeline = Pipeline([
    ('tfidf', TfidfVectorizer(ngram_range=(1, 2), min_df=3, max_features=5000)),
    ('ensemble', ensemble)
])

# ---------------------
# 4. Train
# ---------------------
print("\n🚀 Training started...")
start = time.time()
pipeline.fit(X, y)
end = time.time()
print(f"✅ Training completed in {(end - start):.2f} seconds.")

# ---------------------
# 5. Evaluate
# ---------------------
print("\n📊 Evaluating on training data...")
y_pred = pipeline.predict(X)
acc = accuracy_score(y, y_pred)
print(f"✅ Training Accuracy: {acc:.4f}")

# ---------------------
# 6. Test with examples
# ---------------------
print("\n🧠 Example predictions:")
samples = [
    "I'm under a lot of stress about my grades and college admissions.",
    "I keep comparing my looks to others and it makes me anxious.",
    "I can't sleep because I'm constantly worrying about my career."
]
preds = pipeline.predict(samples)
for q, pred in zip(samples, preds):
    print(f"Q: {q}\n→ Predicted LLM: {pred}\n")

# ---------------------
# 7. Save TFIDF and Ensemble separately (protocol=4)
# ---------------------
print("💾 Saving TF-IDF vectorizer and Voting ensemble separately (protocol=4)...")
joblib.dump(pipeline.named_steps["tfidf"], "tfidf_vectorizer.joblib", protocol=4)
joblib.dump(pipeline.named_steps["ensemble"], "voting_model.joblib", protocol=4)
print("Saved: tfidf_vectorizer.joblib, voting_model.joblib")

# (optional) Also save a pickle for the entire pipeline using protocol=4 if you want:
# joblib.dump(pipeline, "ensemble_router_model.joblib", protocol=4)
# print("Saved full pipeline: ensemble_router_model.joblib")

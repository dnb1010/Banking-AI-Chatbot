import pandas as pd
import joblib

from sklearn.ensemble import IsolationForest
from database.db import engine
from ai.feature_engineering import create_features

query = """
SELECT * FROM completedtrans
"""

df = pd.read_sql(query, engine)

X = create_features(df)

model = IsolationForest(
    contamination=0.02,
    random_state=42
)
model.fit(X)

joblib.dump(
    model,
    r'C:\Users\admin\Documents\MySQL\middle_term\Banking-AI-Chatbot\models\isolation_forest.pkl'
)
print("Fraud detection model trained successfully")

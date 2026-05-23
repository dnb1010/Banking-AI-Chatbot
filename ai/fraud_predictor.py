import joblib

from ai.feature_engineering import create_features
model = joblib.load(
    r'middle_term\Banking-AI-Chatbot\models\isolation_forest.pkl'
)

def predict_transaction(df):
    X = create_features(df)
    prediction = model.predict(X)
    score = model.decision_function(X)
    return prediction, score
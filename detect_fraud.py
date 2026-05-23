import pandas as pd
from sqlalchemy import text
from ai.fraud_predictor import predict_transaction
from database.db import engine
query = """
SELECT *
FROM completedtrans
ORDER BY fulldatewithtime DESC
LIMIT 1
"""


df = pd.read_sql(query, engine)

prediction, score = predict_transaction(df)

label = int(prediction[0])

anomaly_score = float(score[0])

risk_level = 'LOW'

if anomaly_score < -0.2:
    risk_level = 'HIGH'
elif anomaly_score < 0:
    risk_level = 'MEDIUM'

trans_id = df.iloc[0]['trans_id']
account_id = df.iloc[0]['account_id']

insert_query = text("""
INSERT INTO fraud_detection(
    trans_id,
    account_id,
    anomaly_score,
    risk_level,
    predicted_label
)
VALUES(
    :trans_id,
    :account_id,
    :anomaly_score,
    :risk_level,
    :predicted_label
)
""")

with engine.connect() as conn:

    conn.execute(
        insert_query,
        {
            'trans_id': trans_id,
            'account_id': account_id,
            'anomaly_score': anomaly_score,
            'risk_level': risk_level,
            'predicted_label': label
        }
    )

    conn.commit()

print('Fraud detection completed')
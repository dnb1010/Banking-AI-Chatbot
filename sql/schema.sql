create table fraud_detection (
    detect_id int AUTO_INCREMENT PRIMARY KEY,

    trans_id VARCHAR(50),
    account_id VARCHAR(50),
    anomaly_score DECIMAL(10, 5),
    risk_level VARCHAR(20),
    predicted_label INT,
    created_at DATETIME DEFAULT NOW()
);
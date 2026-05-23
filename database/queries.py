import pandas as pd

from sqlalchemy import text

from database.db import engine



def get_balance(account_id):

    query = text("""
    SELECT fn_get_balance(:account_id) AS balance
    """)

    with engine.connect() as conn:

        result = conn.execute(
            query,
            {
                'account_id': account_id
            }
        ).fetchone()

        return float(result.balance)



def get_latest_transactions(account_id):
    query = text("""
    SELECT *
    FROM completedtrans
    WHERE account_id = :account_id
    ORDER BY fulldatewithtime DESC
    LIMIT 5
    """)

    try:
        df = pd.read_sql(
            query,
            engine,
            params={
                'account_id': account_id
            }
        )

        # Debug: nếu DataFrame có dữ liệu thì log tên cột để kiểm tra schema
        try:
            if df is not None:
                print(f"[get_latest_transactions] account_id={account_id} columns={list(df.columns)} rows={len(df)}")
        except Exception:
            pass

        # Trả về list rỗng nếu không có bản ghi
        if df is None or df.empty:
            return pd.DataFrame()

        return df

    except Exception as e:
        print(f"[get_latest_transactions] ERROR account_id={account_id} err={e}")
        # Trả về DataFrame rỗng để router/response vẫn hoạt động
        return pd.DataFrame()



def transfer_money(from_acc, to_acc, amount):

    query = text("""
    CALL sp_chuyenKhoan(
        :from_acc,
        :to_acc,
        :amount
    )
    """)

    with engine.connect() as conn:

        conn.execute(
            query,
            {
                'from_acc': from_acc,
                'to_acc': to_acc,
                'amount': amount
            }
        )

        conn.commit()


def withdraw_money(account_id, amount):
    """Rút tiền: gọi stored procedure sp_rutTien (nếu tồn tại)."""
    query = text("""
    CALL sp_rutTien(
        :account_id,
        :amount
    )
    """)

    with engine.connect() as conn:
        conn.execute(query, {"account_id": account_id, "amount": amount})
        conn.commit()


def get_loan_info(account_id):
    """Lấy thông tin khoản vay. Ưu tiên gọi stored procedure nếu có."""
    # Không có schema đọc được trong repo, nên fallback theo view/table nếu procedure không tồn tại.
    # Nếu DB đã có sp_thanhToanNoHangThang/sp_... thì chỉnh lại cho khớp tên.
    query = text("""
    SELECT *
    FROM loans
    WHERE account_id = :account_id
    ORDER BY due_date DESC
    LIMIT 1
    """)

    with engine.connect() as conn:
        row = conn.execute(query, {"account_id": account_id}).fetchone()
        if row is None:
            return None
        # SQLAlchemy Row -> dict
        return dict(row._mapping)


def repay_loan(account_id, amount):
    """Trả nợ: gọi stored procedure sp_thanhToanNoHangThang nếu tồn tại."""
    query = text("""
    CALL sp_thanhToanNoHangThang(
        :account_id,
        :amount
    )
    """)

    with engine.connect() as conn:
        conn.execute(query, {"account_id": account_id, "amount": amount})
        conn.commit()


def get_savings_info(account_id):
    """Lấy thông tin tiết kiệm."""
    query = text("""
    SELECT *
    FROM savings
    WHERE account_id = :account_id
    ORDER BY created_at DESC
    LIMIT 1
    """)

    with engine.connect() as conn:
        row = conn.execute(query, {"account_id": account_id}).fetchone()
        if row is None:
            return None
        return dict(row._mapping)


def run_fraud_detection():
    """Chạy fraud detection cho giao dịch mới nhất, lưu vào fraud_detection, trả về risk info."""
    import pandas as pd
    from ai.fraud_predictor import predict_transaction

    query = text("""
    SELECT *
    FROM completedtrans
    ORDER BY fulldatewithtime DESC
    LIMIT 1
    """)

    df = pd.read_sql(query, engine)
    if df is None or df.empty:
        return None

    prediction, score = predict_transaction(df)
    label = int(prediction[0])
    anomaly_score = float(score[0])

    risk_level = "LOW"
    if anomaly_score < -0.2:
        risk_level = "HIGH"
    elif anomaly_score < 0:
        risk_level = "MEDIUM"

    trans_id = str(df.iloc[0].get("trans_id"))
    account_id = df.iloc[0].get("account_id")

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
                "trans_id": trans_id,
                "account_id": account_id,
                "anomaly_score": anomaly_score,
                "risk_level": risk_level,
                "predicted_label": label,
            },
        )
        conn.commit()

    return {
        "risk_level": risk_level,
        "anomaly_score": anomaly_score,
        "predicted_label": label,
        "trans_id": trans_id,
        "account_id": account_id,
    }


def withdraw_money(from_acc: str, amount: float):
    """Rút tiền từ tài khoản (dùng stored procedure sp_rutTien nếu tồn tại)."""
    query = text("""
    CALL sp_rutTien(
        :from_acc,
        :amount
    )
    """)

    with engine.connect() as conn:
        conn.execute(
            query,
            {
                'from_acc': from_acc,
                'amount': amount,
            },
        )
        conn.commit()


def get_loan_info(account_id: str):
    """Lấy thông tin khoản vay của account (dùng view/table nếu có)."""
    # Fallback: cố đọc một vài cột phổ biến từ bảng loan (nếu schema thực tế khác sẽ cần chỉnh)
    query = text("""
    SELECT *
    FROM loan
    WHERE account_id = :account_id
    ORDER BY created_at DESC
    LIMIT 1
    """)

    try:
        df = pd.read_sql(query, engine, params={'account_id': account_id})
        if df is None or df.empty:
            return {}
        return df.iloc[0].to_dict()
    except Exception:
        # Nếu không có bảng loan, trả về dict rỗng để router vẫn chạy
        return {}


def repay_loan(account_id: str, amount: float):
    """Trả nợ vay (dùng stored procedure sp_thanhToanNoHangThang nếu tồn tại)."""
    query = text("""
    CALL sp_thanhToanNoHangThang(
        :account_id,
        :amount
    )
    """)

    with engine.connect() as conn:
        conn.execute(query, {'account_id': account_id, 'amount': amount})
        conn.commit()


def get_savings_info(account_id: str):
    """Lấy thông tin sổ tiết kiệm của account (fallback đọc bảng savings)."""
    query = text("""
    SELECT *
    FROM savings
    WHERE account_id = :account_id
    ORDER BY created_at DESC
    LIMIT 1
    """)

    try:
        df = pd.read_sql(query, engine, params={'account_id': account_id})
        if df is None or df.empty:
            return {}
        return df.iloc[0].to_dict()
    except Exception:
        return {}


def run_fraud_detection_latest():
    """Chạy fraud detection cho giao dịch mới nhất và ghi vào fraud_detection."""
    # Tránh import theo kiểu script để không gây side-effect
    from detect_fraud import engine as _engine
    # Nếu detect_fraud.py dùng engine import lại thì vẫn dùng đúng engine
    # Lấy kết quả risk level bằng cách chạy lại logic cơ bản ở đây.
    query = """
    SELECT *
    FROM completedtrans
    ORDER BY fulldatewithtime DESC
    LIMIT 1
    """

    df = pd.read_sql(query, _engine)
    if df is None or df.empty:
        return {
            'risk_level': 'LOW',
            'anomaly_score': None,
            'predicted_label': None,
            'trans_id': None,
        }

    from ai.fraud_predictor import predict_transaction

    prediction, score = predict_transaction(df)
    label = int(prediction[0])
    anomaly_score = float(score[0])

    risk_level = 'LOW'
    if anomaly_score < -0.2:
        risk_level = 'HIGH'
    elif anomaly_score < 0:
        risk_level = 'MEDIUM'

    trans_id = df.iloc[0].get('trans_id')
    account_id = df.iloc[0].get('account_id')

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

    with _engine.connect() as conn:
        conn.execute(
            insert_query,
            {
                'trans_id': trans_id,
                'account_id': account_id,
                'anomaly_score': anomaly_score,
                'risk_level': risk_level,
                'predicted_label': label,
            },
        )
        conn.commit()

    return {
        'risk_level': risk_level,
        'anomaly_score': anomaly_score,
        'predicted_label': label,
        'trans_id': trans_id,
        'account_id': account_id,
    }


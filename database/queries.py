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
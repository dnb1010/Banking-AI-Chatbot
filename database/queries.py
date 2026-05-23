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

    return pd.read_sql(
        query,
        engine,
        params={
            'account_id': account_id
        }
    )



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
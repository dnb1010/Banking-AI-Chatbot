from ai.intent_classifier import classify_intent
from ai.entity_extractor import *

from database.queries import *

from chatbot.response_builder import *


def handle_message(message, user_account):

    intent = classify_intent(message)

    if intent == 'get_balance':

        balance = get_balance(user_account)

        return build_balance_response(balance)

    if intent == 'transaction_history':

        transactions = get_latest_transactions(user_account)

        # Đảm bảo trả về dữ liệu JSON-serializable cho frontend (không dùng Timestamp/np types)
        try:
            df = transactions

            if df is None or getattr(df, "empty", True):
                return []

            records = df.to_dict(orient='records')

            safe_records = []
            for row in records:
                safe_row = {}
                for k, v in row.items():
                    # Chuyển NaN/None về None, các kiểu lạ về string
                    if v is None:
                        safe_row[k] = None
                    else:
                        try:
                            # pandas NaN
                            if str(v) == 'nan':
                                safe_row[k] = None
                            else:
                                safe_row[k] = v if isinstance(v, (int, float, bool, str)) else str(v)
                        except Exception:
                            safe_row[k] = str(v)

                safe_records.append(safe_row)

            return safe_records
        except Exception:
            return []

    if intent == 'transfer':

        amount = extract_amount(message)
        to_account = extract_account(message)

        transfer_money(
            user_account,
            to_account,
            amount
        )

        fraud = run_fraud_detection()
        return {
            "message": build_transfer_response(),
            "fraud": fraud,
        }

    if intent == 'withdraw':

        amount = extract_amount(message)
        # withdraw dùng account_id từ UI (user_account)
        withdraw_money(user_account, amount)

        fraud = run_fraud_detection()
        return {
            "message": "Rút tiền thành công",
            "fraud": fraud,
        }

    if intent == 'loan':
        # loan: lấy thông tin khoản vay
        info = get_loan_info(user_account)
        if not info:
            return "Không tìm thấy thông tin khoản vay"
        return {
            "message": "Thông tin khoản vay",
            "loan": info,
        }

    if intent == 'savings':
        info = get_savings_info(user_account)
        if not info:
            return "Không tìm thấy thông tin sổ tiết kiệm"
        return {
            "message": "Thông tin sổ tiết kiệm",
            "savings": info,
        }

    return build_unknown_response()

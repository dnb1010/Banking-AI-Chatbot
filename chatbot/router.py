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

        return build_transfer_response()

    return build_unknown_response()
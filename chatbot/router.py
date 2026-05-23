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

        return transactions.to_dict(
            orient='records'
        )

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
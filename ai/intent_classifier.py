def classify_intent(message: str):
    msg = message.lower()

    if 'số dư' in msg:
        return 'get_balance'
    if 'lịch sử' in msg:
        return 'transaction_history'
    if 'chuyển' in msg:
        return 'transfer'
    if 'rút' in msg:
        return 'withdraw'
    if 'vay' in msg:
        return 'loan'
    if 'tiết kiệm' in msg:
        return 'savings'
    return 'unknown'
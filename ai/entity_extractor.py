import re

def extract_amount(message: str):
    numbers = re.findall(r'\d+', message)
    if not numbers:
        return None
    return int(numbers[0])

def extract_account(message: str):
    match = re.search(r'ACC\d+', message)
    if match:
        return match.group()
    return None
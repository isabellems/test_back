from typing import TypedDict
from datetime import datetime, timezone

class Transaction(TypedDict):
    sender: str
    iban: str
    recipient: str
    amount: float
    description: str
    timestamp: datetime

transactions = [Transaction]

def add_transaction(sender: str, iban: str, recipient: str, amount: float, description: str):
    dt = datetime.now(timezone.utc)
    timestamp = dt.isoformat()

    transactions.append(Transaction(sender=sender, 
                                    iban=iban,
                                    recipient=recipient, 
                                    amount=amount, 
                                    description=description, 
                                    timestamp=timestamp))
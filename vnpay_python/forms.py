from django import forms
from typing import Optional

from pydantic import BaseModel
from schemas.Default import Config


class PaymentForm(BaseModel, Config):
    payment_id: Optional[int]
    order_id: Optional[int]
    amount: Optional[int]
    # txnRef: Optional[str]
    # bank_code: Optional[str]
    # language: Optional[str]

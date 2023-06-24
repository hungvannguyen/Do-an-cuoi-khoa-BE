from django import forms
from typing import Optional

from pydantic import BaseModel
from schemas.Default import Config


class PaymentForm(BaseModel, Config):
    # order_id: Optional[str]
    # order_type: Optional[str]
    amount: Optional[int]
    order_info: Optional[str]
    txnRef: Optional[str]
    # bank_code: Optional[str]
    # language: Optional[str]

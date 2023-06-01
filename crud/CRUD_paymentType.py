from datetime import datetime
from typing import Any

from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from fastapi.encoders import jsonable_encoder
import models
import schemas.user
from crud.base import CRUDBase
from models.paymentType import PaymentType
from schemas.paymentType import *
from constants import Const
from security.security import hash_password, verify_password, gen_token


class CRUDPaymentType(CRUDBase[PaymentType, PaymentTypeCreate, PaymentTypeUpdate]):

    def get_payment_type(self, paymentType_id, db: Session):
        data_db = db.query(self.model).filter(
            self.model.id == paymentType_id,
            self.model.delete_flag == Const.DELETE_FLAG_NORMAL
        ).first()
        return {
            'id': data_db.id,
            'name': data_db.name
        }

    def get_all_payment_type(self, db: Session):
        data_db = db.query(self.model).filter(
            self.model.delete_flag == Const.DELETE_FLAG_NORMAL
        ).all()
        result = []
        for item in data_db:
            result.append({
                'id': item.id,
                'name': item.name
            })
        return result


crud_paymentType = CRUDPaymentType(PaymentType)

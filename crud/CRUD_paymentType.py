from datetime import datetime
from typing import Any
from crud import logger
from constants import Method, Target
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

    def create_payment_type(self, request, db: Session, admin_id):
        if not isinstance(request, dict):
            request = request.dict()
        obj_db = self.model(**request, insert_id=admin_id, update_id=admin_id)
        db.add(obj_db)
        db.commit()
        db.refresh(obj_db)
        return {
            'detail': 'success'
        }


crud_paymentType = CRUDPaymentType(PaymentType)

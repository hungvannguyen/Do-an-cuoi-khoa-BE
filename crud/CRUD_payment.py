from datetime import datetime
from typing import Any

from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from fastapi.encoders import jsonable_encoder
import models
import schemas.user
from crud.base import CRUDBase
from models.payment import Payment
from schemas.payment import *
from constants import Const
from crud.CRUD_paymentType import crud_paymentType
from security.security import hash_password, verify_password, gen_token


class CRUDPayment(CRUDBase[Payment, PaymentCreate, PaymentUpdate]):

    def get_payment_by_order_id(self, order_id, db: Session):
        data_db = db.query(self.model).filter(
            self.model.order_id == order_id,
            self.model.delete_flag == Const.DELETE_FLAG_NORMAL
        ).first()

        payment_type_db = crud_paymentType.get_payment_type(paymentType_id=data_db.payment_type_id, db=db)

        return {
            'id': data_db.id,
            'order_id': data_db.order_id,
            'payment_type_id': data_db.payment_type_id,
            'payment_type_name': payment_type_db.name,
            'status': data_db.status
        }

    def add_payment(self, request, db: Session, user_id):
        obj_data = self.model(**request, insert_id=user_id, update_id=user_id, insert_at=datetime.utcnow(),
                              update_at=datetime.utcnow())

        db.add(obj_data)
        db.commit()
        db.refresh(obj_data)

        return obj_data

    def update_payment(self, request, db: Session, user_id):
        if not isinstance(request, dict):
            request = request.dict()
        data_db = db.query(self.model).filter(
            self.model.order_id == request.order_id,
            self.model.delete_flag == Const.DELETE_FLAG_NORMAL
        ).first()

        self.update(db=db, db_obj=data_db, obj_in=request, admin_id=user_id)

        return {
            'detail': 'Đã cập nhật thành công'
        }


crud_payment = CRUDPayment(Payment)

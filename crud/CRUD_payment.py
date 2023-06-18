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
from models.payment import Payment
from schemas.payment import *
from constants import Const
from crud.CRUD_paymentType import crud_paymentType
from security.security import hash_password, verify_password, gen_token


class CRUDPayment(CRUDBase[Payment, PaymentCreate, PaymentUpdate]):

    def get_payment_by_id(self, id, db: Session):
        data_db = db.query(self.model).filter(
            self.model.id == id,
            self.model.delete_flag == Const.DELETE_FLAG_NORMAL
        ).first()

        payment_type_db = crud_paymentType.get_payment_type(paymentType_id=data_db.payment_type_id, db=db)
        logger.log(Method.GET, Target.PAYMENT, comment=f"GET PAYMENT BY ID #{id}",
                   status=Target.SUCCESS,
                   id=0,
                   db=db)
        return {
            'id': data_db.id,
            'payment_type_id': data_db.payment_type_id,
            'payment_type_name': payment_type_db['name'],
            'status': data_db.status
        }

    def add_payment(self, request, db: Session, user_id):
        if not isinstance(request, dict):
            request = request.dict()
        obj_data = self.model(**request, insert_id=user_id, update_id=user_id, insert_at=datetime.now(),
                              update_at=datetime.now())

        db.add(obj_data)
        db.commit()
        db.refresh(obj_data)
        logger.log(Method.POST, Target.PAYMENT, comment=f"CREATE NEW PAYMENT FOR USER ID #{user_id}",
                   status=Target.SUCCESS,
                   id=user_id,
                   db=db)
        return obj_data

    def update_payment(self, request, db: Session, user_id):
        if not isinstance(request, dict):
            request = request.dict()
        data_db = db.query(self.model).filter(
            self.model.order_id == request.order_id,
            self.model.delete_flag == Const.DELETE_FLAG_NORMAL
        ).first()

        self.update(db=db, db_obj=data_db, obj_in=request, admin_id=user_id)
        logger.log(Method.PUT, Target.PAYMENT, comment=f"UPDATE PAYMENT FOR ORDER ID #{request.order_id}",
                   status=Target.SUCCESS,
                   id=user_id,
                   db=db)
        return {
            'detail': 'Đã cập nhật thành công'
        }


crud_payment = CRUDPayment(Payment)

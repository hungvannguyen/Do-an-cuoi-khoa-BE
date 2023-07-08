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
from models.order import Order
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
            'status': data_db.status,
            'bankCode': data_db.bankCode,
            'transactionNo': data_db.transactionNo,
            'insert_at': data_db.insert_at
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

    def update_payment(self, payment_id, payment_status, bankCode, transactionNo, db: Session, user_id):
        data_db = db.query(self.model).filter(
            self.model.id == payment_id,
            self.model.delete_flag == Const.DELETE_FLAG_NORMAL
        ).first()

        data_db.status = payment_status
        data_db.bankCode = bankCode
        data_db.transactionNo = transactionNo
        data_db.update_id = user_id
        data_db.update_at = datetime.now()

        db.merge(data_db)
        db.commit()

        order_db = db.query(Order).filter(
            Order.payment_id == payment_id
        ).first()

        order_db.status = Const.ORDER_CONFIRMED
        order_db.update_at = datetime.now()

        db.merge(order_db)
        db.commit()

        logger.log(Method.PUT, Target.PAYMENT, comment=f"UPDATE PAYMENT ID #{payment_id}",
                   status=Target.SUCCESS,
                   id=user_id,
                   db=db)
        return {
            'detail': 'Đã cập nhật thành công'
        }


    def complete_cod_payment(self, payment_id, db:Session):
        payment_db = db.query(self.model).filter(
            self.model.id == payment_id,
            self.model.status == Const.UNPAID
        ).first()

        payment_db.status = Const.PAID
        payment_db.update_at = datetime.now()

        db.merge(payment_db)
        db.commit()

        order_db = db.query(Order).filter(
            Order.payment_id == payment_id
        ).first()

        order_db.status = Const.ORDER_SUCCESS
        order_db.update_at = datetime.now()
        db.merge(order_db)
        db.commit()

        return {
            'detail': "Đã cập nhật"
        }

    def payment_return(self, vnp_Amount,
                       vnp_BankCode,
                       vnp_BankTranNo,
                       vnp_CardType,
                       vnp_PayDate,
                       vnp_ResponseCode,
                       vnp_TmnCode,
                       vnp_TransactionNo,
                       vnp_TransactionStatus,
                       vnp_TxnRef,
                       vnp_SecureHash, db: Session):
        print(vnp_TxnRef)

        obj_db = db.query(self.model).filter(
            self.model.txnRef == vnp_TxnRef
        ).first()
        obj_db.status = vnp_ResponseCode
        obj_db.bankCode = vnp_BankCode
        obj_db.transactionNo = vnp_TransactionNo
        obj_db.update_at = datetime.now()

        db.merge(obj_db)
        db.commit()
        logger.log(Method.PUT, Target.PAYMENT, comment=f"UPDATE PAYMENT OF TXNREF #{vnp_TxnRef}", status=Target.SUCCESS,
                   id=0, db=db)
        return {
            'detail': "Đã cập nhật tình trạng thanh toán"
        }


crud_payment = CRUDPayment(Payment)

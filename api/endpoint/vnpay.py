from fastapi import Depends, UploadFile, File, APIRouter, status
from passlib.context import CryptContext
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from security.security import verify_password
from fastapi.encoders import jsonable_encoder
from crud.CRUD_payment import crud_payment
from schemas.cart import *
from schemas.token import TokenPayload
from database import deps
from vnpay_python import forms, views

router = APIRouter()


@router.post("/create")
def create_vnpay_url(request: forms.PaymentForm, token: TokenPayload = Depends(deps.get_current_user)):
    return views.payment(request=request, user_id=token.id)


@router.get("/return")
def get_return_payment(vnp_Amount: int = None,
                       vnp_BankCode: str = None,
                       vnp_BankTranNo: str = None,
                       vnp_CardType: str = None,
                       vnp_PayDate: str = None,
                       vnp_ResponseCode: int = None,
                       vnp_TmnCode: str = None,
                       vnp_TransactionNo: str = None,
                       vnp_TransactionStatus: str = None,
                       vnp_TxnRef: str = None,
                       vnp_SecureHash: str = None, db: Session = Depends(deps.get_db)):
    return crud_payment.payment_return(vnp_Amount=vnp_Amount,
                                       vnp_BankCode=vnp_BankCode,
                                       vnp_BankTranNo=vnp_BankTranNo,
                                       vnp_CardType=vnp_CardType,
                                       vnp_PayDate=vnp_PayDate,
                                       vnp_ResponseCode=vnp_ResponseCode,
                                       vnp_TmnCode=vnp_TmnCode,
                                       vnp_TransactionNo=vnp_TransactionNo,
                                       vnp_TransactionStatus=vnp_TransactionStatus,
                                       vnp_TxnRef=vnp_TxnRef,
                                       vnp_SecureHash=vnp_SecureHash, db=db)

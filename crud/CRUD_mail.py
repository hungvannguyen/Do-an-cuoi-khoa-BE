import datetime
from crud import logger
from constants import Method, Target
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from constants import Const
from mail.mail import send_mail
from models.user import User
from models.code_confirm import Code_Confirm
from mail.template import confirm_code_template, confirm_email_template
from security.generator import *


def create_confirm_mail(mail_to, db: Session):
    link = f"http://localhost:3000/email/confirm?email={mail_to}"
    text = confirm_email_template
    text = text.replace('<a href="http://dhsgundam3" class="es-button"', f'<a href="{link}" class="es-button"')
    logger.log(Method.POST, Target.MAIL_CONFIRM, comment=f"CREATE CONFIRM MAIL",
               status=Target.SUCCESS,
               id=Const.ADMIN_ID,
               db=db)
    return send_mail(mail_to=mail_to, title="[DhsGundam] Please confirm your Email!", content=text, db=db)


def create_confirm_code_email(account, db: Session):
    user_db = db.query(User).filter(
        User.account == account,
        User.is_confirmed == Const.IS_CONFIRMED,
        User.delete_flag == Const.DELETE_FLAG_NORMAL
    ).first()
    if not user_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Không tìm thấy tài khoản")

    user_id = user_db.id
    mail_to = user_db.email

    code_db = db.query(Code_Confirm).filter(
        Code_Confirm.user_id == user_id,
        Code_Confirm.delete_flag == Const.DELETE_FLAG_NORMAL
    ).first()
    if code_db:
        code_db.delete_flag = Const.DELETE_FLAG_DELETED
        code_db.delete_id = 1
        code_db.delete_at = datetime.now()
        db.merge(code_db)
        db.commit()

    expire, code = code_confirm_generator()

    obj_db = Code_Confirm()
    obj_db.user_id = user_db.id,
    obj_db.expire_time = expire
    obj_db.code = code
    obj_db.insert_id = user_id
    obj_db.update_id = user_id
    obj_db.insert_at = datetime.now()
    obj_db.update_at = datetime.now()
    obj_db.delete_flag = Const.DELETE_FLAG_NORMAL
    db.add(obj_db)
    db.commit()
    db.refresh(obj_db)

    text = confirm_code_template.replace("11111", str(code))
    logger.log(Method.POST, Target.MAIL_CONFIRM, comment=f"CREATE CODE CONFIRM MAIL",
               status=Target.SUCCESS,
               id=user_id,
               db=db)
    return send_mail(mail_to=mail_to, title="[DhsGundam] Đây là mã xác thực của bạn!", content=text, db=db)

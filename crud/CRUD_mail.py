import datetime
from crud import logger
from constants import Method, Target
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from constants import Const
from mail.mail import send_mail
from models.order import Order
from models.order_product import Order_Product
from models.payment import Payment
from models.user import User
from models.code_confirm import Code_Confirm
from mail.template import confirm_code_template, confirm_email_template, email_order_detail, one_order_detail
from security.generator import *
from security.security import hash_password


def create_confirm_mail(mail_to, db: Session):
    hash_mail = hash_password(mail_to)
    link = f"http://dhsgundam.online/email/confirm?email={hash_mail}"
    text = confirm_email_template
    text = text.replace('<a href="http://dhsgundam3" class="es-button"', f'<a href="{link}" class="es-button"')

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

    return send_mail(mail_to=mail_to, title="[DhsGundam] Đây là mã xác thực của bạn!", content=text, db=db)


def create_order_detail_email(order_id, db: Session):
    order_db = db.query(Order).filter(
        Order.id == order_id
    ).first()

    mail_to = order_db.email

    order_detail_db = db.query(Order_Product).filter(
        Order_Product.order_id == order_id
    ).all()

    main_template = email_order_detail

    main_template = main_template.replace("ward_district,", "")

    main_template = main_template.replace("city", "")

    main_template = main_template.replace("1111", f"{order_id}")

    main_template = main_template.replace("Đơn hàng #1111 đã được xác nhận!",
                                          f"Đơn hàng #{order_id} đã đặt thành công!")

    total_price = int(order_db.total_price)
    main_template = main_template.replace("$2222", f"{total_price} VNĐ")

    total_prd_price = 0

    for item in order_detail_db:
        total_prd_price += item.price
    total_prd_price = int(total_prd_price)
    main_template = main_template.replace("$4444", f"{total_prd_price} VNĐ")

    ship_price = total_price - total_prd_price
    main_template = main_template.replace("$3333", f"{ship_price} VNĐ")

    name = order_db.name

    main_template = main_template.replace("aaaa", f"{name}")

    address = order_db.address

    main_template = main_template.replace("details,", f"{address}")

    order_date = str(order_db.insert_at)[0:10]

    main_template = main_template.replace("Apr 17, 2021", f"{order_date}")

    payment_id = order_db.payment_id

    payment_db = db.query(Payment).filter(
        Payment.id == payment_id
    ).first()

    bankCode = payment_db.bankCode

    main_template = main_template.replace("PayPal", f"{bankCode}")

    return send_mail(mail_to=mail_to, title="[DhsGundam] Kiểm tra đơn hàng của bạn!", content=main_template, db=db)
from datetime import datetime, timedelta

from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from crud import CRUD_mail
from models.address import Address
from models.cart import Cart
from models.payment import Payment
from models.product_quantity import ProductQuantity
from models.user import User
from vnpay_python import views as CRUD_vnpay
import models
from models.product import Product

from crud.base import CRUDBase
from models.order import Order
from schemas.order import *
from crud.CRUD_order_product import crud_order_product

from crud.CRUD_payment import crud_payment

from crud.CRUD_address import crud_address
from crud.CRUD_user import crud_user
from constants import Const



class CRUDOrder(CRUDBase[Order, OrderCreate, OrderUpdate]):

    def get_order_by_id(self, order_id, db: Session, user_id):
        obj_db = db.query(self.model).filter(
            self.model.id == order_id
        ).first()
        result = {
            'id': order_id,
            'products': [],
            'total_price': obj_db.total_price,
            'name': obj_db.name,
            'phone_number': obj_db.phone_number,
            'email': obj_db.email,
            'address': obj_db.address,
            'note': obj_db.note,
            'status': obj_db.status,
            'payment_id': obj_db.payment_id,
            'payment_type': '',
            'payment_type_id': 0,
            'payment_status': 0,
            'bankCode': '',
            'transactionNo': '',
            'insert_at': obj_db.insert_at,
            'cancel_reason': obj_db.cancel_reason
        }
        # total_price = 0
        if obj_db:
            order_id = obj_db.id
            order_product_db = crud_order_product.get_by_order_id(order_id=order_id, db=db)
            for item in order_product_db:
                prd_id = item.product_id
                # prd_db = self.get_product_by_id(id=prd_id, db=db)
                prd_name = item.name
                prd_img_url = item.img_url
                # total_price += item.price * item.quantity
                prd_obj = {
                    'prd_id': prd_id,
                    'name': prd_name,
                    'img_url': prd_img_url,
                    'price': item.price,
                    'quantity': item.quantity,
                    'total_price': item.price * item.quantity
                }
                result['products'].append(prd_obj)

        # result['total_price'] = total_price

        if obj_db.status == Const.ORDER_DELIVERED:
            confirm_time = obj_db.update_at + timedelta(
                #  Chuyển về 5 ngày
                seconds=3600 * 5
            )
            if confirm_time <= datetime.now():
                obj_db.status = Const.ORDER_SUCCESS
                obj_db.update_at = confirm_time
                obj_db.update_id = user_id

                db.merge(obj_db)
                db.commit()
                db.refresh(obj_db)

                result['status'] = obj_db.status

        payment_id = obj_db.payment_id
        payment_db = crud_payment.get_payment_by_id(id=payment_id, db=db)

        payment_insert_at = payment_db['insert_at']
        payment_type_id = payment_db['payment_type_id']
        payment_status = payment_db['status']
        if payment_type_id == Const.ONLINE_PAYMENT and payment_status == 99:
            insert_at = payment_insert_at + timedelta(
                seconds=30 * 60
            )

            if insert_at < datetime.now():
                obj_db.status = Const.ORDER_CANCEL
                obj_db.update_at = insert_at
                obj_db.update_id = Const.SYSTEM_ID
                obj_db.cancel_reason = "Tự động huỷ do quá thời gian thanh toán"

                db.merge(obj_db)
                db.commit()
                db.refresh(obj_db)

                result['status'] = obj_db.status

        result['payment_type_id'] = payment_db['payment_type_id']
        result['payment_type'] = payment_db['payment_type_name']
        result['payment_status'] = payment_db['status']
        result['bankCode'] = payment_db['bankCode']
        result['transactionNo'] = payment_db['transactionNo']



        return result

    def get_all_orders_by_user_id(self, page, order_status, user_id, db: Session):
        order_db = db.query(self.model).filter(
            self.model.user_id == user_id
        )
        if order_status is not None and order_status != -1:
            order_db = order_db.filter(
                self.model.status == order_status
            )

        total_order = order_db.count()
        total_page = int(total_order / Const.ROW_PER_PAGE_ORDER)
        # total_order = int(total_order / Const.ROW_PER_PAGE_ORDER)
        if total_order % Const.ROW_PER_PAGE_ORDER > 0:
            total_page += 1
        current_page = page
        if current_page < 1:
            current_page = 1
        if current_page > total_page > 0:
            current_page = total_page

        start = (current_page - 1) * Const.ROW_PER_PAGE_ORDER

        order_db = order_db.order_by(self.model.insert_at.desc()).offset(start).limit(Const.ROW_PER_PAGE).all()

        if not order_db:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Không có đơn hàng")

        result = []
        for item in order_db:
            result.append(self.get_order_by_id(order_id=item.id, db=db, user_id=user_id))

        return {
            'data': result,
            'current_page': current_page,
            'total_page': total_page
        }

    def get_all_orders(self, page, order_status, db: Session, admin_id):
        order_db = db.query(self.model)
        if order_status is not None:
            order_db = order_db.filter(
                self.model.status == order_status
            )

        total_order = order_db.count()
        total_page = int(total_order / Const.ROW_PER_PAGE_ADMIN)
        if total_order % Const.ROW_PER_PAGE_ADMIN > 0:
            total_page += 1
        current_page = page
        if current_page < 1:
            current_page = 1
        if current_page > total_page > 0:
            current_page = total_page

        start = (current_page - 1) * Const.ROW_PER_PAGE_ADMIN

        if order_status == Const.ORDER_PENDING or order_status == Const.ORDER_REFUND_REQUEST:
            order_db = order_db.order_by(self.model.insert_at.asc()).offset(start).limit(Const.ROW_PER_PAGE_ADMIN).all()
        else:
            order_db = order_db.order_by(self.model.insert_at.desc()).offset(start).limit(Const.ROW_PER_PAGE_ADMIN).all()

        if not order_db:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Không có đơn hàng")

        result = []
        for item in order_db:
            result.append(self.get_order_by_id(order_id=item.id, db=db, user_id=admin_id))

        return {
            'data': result,
            'current_page': current_page,
            'total_page': total_page
        }

    def add_order(self, request, db: Session, user_id, email, role_id):
        # Add payment method
        payment_type_id = request.payment_type_id
        bankCode = ''
        txnRef = str(user_id) + str(datetime.now().strftime('%Y%m%d%H%M%S'))
        if payment_type_id == Const.COD_PAYMENT:
            bankCode = "COD"
        payment_status = Const.UNPAID
        if role_id == 1 or role_id == 10:
            payment_status = Const.PAID
        request_payment = {
            'payment_type_id': payment_type_id,
            'status': payment_status,
            'bankCode': bankCode,
            'txnRef': txnRef,
            'insert_at': datetime.now()
        }
        payment_db = crud_payment.add_payment(request=request_payment, db=db, user_id=user_id)

        # Get Address Info
        address_id = request.address_id
        address_db = db.query(Address).filter(
            Address.id == address_id,
            Address.delete_flag == Const.DELETE_FLAG_NORMAL
        ).first()
        name = address_db.name
        phone_number = address_db.phone_number

        # Add Order Info
        payment_id = payment_db.id
        email = email
        status = 0
        if role_id == 1 or role_id == 10:
            status = Const.ORDER_SUCCESS
        note = request.note

        order_obj_db = self.model(user_id=user_id, payment_id=payment_id, name=name, phone_number=phone_number,
                                  note=note, total_price=0,
                                  email=email, address="", status=status, insert_at=datetime.now(),
                                  insert_id=user_id, update_id=user_id, update_at=datetime.now())

        db.add(order_obj_db)
        db.commit()
        db.refresh(order_obj_db)

        # Add Order_Product Info
        order_id = order_obj_db.id
        cart_db = []

        prd_ids = list(str(request.prd_ids).split(","))
        for prd_id in prd_ids:
            product_db = db.query(Product).filter(
                Product.id == prd_id
            ).first()

            setattr(product_db, 'sale_price', product_db.price)
            if product_db.is_sale == 1:
                setattr(product_db, 'sale_price', product_db.price * (100 - product_db.sale_percent) / 100)

            cart_obj = db.query(Cart).filter(
                Cart.user_id == user_id,
                Cart.prd_id == prd_id,
                Cart.delete_flag == Const.DELETE_FLAG_NORMAL
            ).first()

            obj = {
                'prd_id': prd_id,
                'quantity': cart_obj.quantity,
                'name': product_db.name,
                'img_url': product_db.img_url,
                'sale_price': product_db.sale_price,
                'import_price': product_db.import_price
            }

            cart_db.append(obj)

            cart_obj.delete_flag = Const.DELETE_FLAG_DELETED
            db.merge(cart_obj)
            db.commit()
            db.refresh(cart_obj)

        prd_carts = cart_db
        total_price = 0
        for item in prd_carts:
            product_id = item['prd_id']
            quantity = item['quantity']
            prd_name = item['name']
            img_url = item['img_url']
            price = item['sale_price']

            total_price += price * quantity

            quantity_obj = db.query(ProductQuantity).filter(
                ProductQuantity.prd_id == product_id
            ).order_by(ProductQuantity.import_price.asc()).all()

            for qtt in quantity_obj:
                if quantity == 0:
                    break
                prd_quantity = qtt.quantity
                import_price = qtt.import_price
                if quantity <= prd_quantity:
                    order_product_obj_db = models.order_product.Order_Product(order_id=order_id, product_id=product_id,
                                                                              quantity=quantity, name=prd_name,
                                                                              img_url=img_url,
                                                                              price=price, import_price=import_price)

                    db.add(order_product_obj_db)
                    db.commit()
                    db.refresh(order_product_obj_db)
                    quantity = 0
                    qtt.quantity = prd_quantity - quantity
                    db.merge(qtt)
                    db.commit()
                else:
                    qtt.quantity = 0
                    db.merge(qtt)
                    db.commit()

                    order_product_obj_db = models.order_product.Order_Product(order_id=order_id, product_id=product_id,
                                                                              quantity=prd_quantity, name=prd_name,
                                                                              img_url=img_url,
                                                                              price=price, import_price=import_price)

                    db.add(order_product_obj_db)
                    db.commit()
                    db.refresh(order_product_obj_db)

                    quantity -= prd_quantity

        # Update Total_price
        address_user = crud_address.get_address_detail_by_address_id(address_id=address_id, db=db)
        city_id = address_user['city_id']
        if city_id != 1:
            total_price += 30000

        order_obj_db.total_price = total_price
        db.merge(order_obj_db)
        db.commit()
        db.refresh(order_obj_db)

        # Delete Cart Info

        # Update Address in Order

        city = address_user['city']
        district = address_user['district']
        ward = address_user['ward']
        detail = address_user['detail']

        address_detail = detail + ", " + ward + ", " + district + ", " + city
        order_obj_db.address = address_detail
        db.merge(order_obj_db)
        db.commit()
        db.refresh(order_obj_db)

        # Update User Info

        user_db = db.query(User).filter(
            User.id == user_id,
            User.delete_flag == Const.DELETE_FLAG_NORMAL
        ).first()

        if user_db.name is None:
            user_update_info = {
                'name': name,
                'phone_number': phone_number
            }
            crud_user.update_info(request=user_update_info, db=db, user_id=user_id)

        if payment_type_id == Const.COD_PAYMENT:
            CRUD_mail.create_order_detail_email(order_id=order_id, db=db)

        # Generate VNPAY link
        vnpay_url = ""
        if payment_type_id == Const.ONLINE_PAYMENT:
            request_vnpay = {
                'amount': total_price,
                'order_info': f"THANH TOAN DON HANG DHSGUNDAM #{order_id}",
                'txnRef': txnRef
            }
            vnpay_url = CRUD_vnpay.payment(request=request_vnpay, user_id=user_id)

        if payment_type_id == 1:
            result = {
                'detail': 'Đã đặt hàng thành công',
                'vnpay_url': vnpay_url
            }
        else:
            result = {
                'detail': 'Đã đặt hàng thành công'
            }
        return result

    def update_order_status(self, order_status, order_id, cancel_reason, db: Session, user_id):
        obj_db = db.query(self.model).filter(
            self.model.id == order_id
        ).first()
        if obj_db.status == 99:

            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="Không thể cập nhật tình trạng cho đơn hàng này")

        if obj_db.status != 0 and order_status == 99:

            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="Không thể huỷ đơn hàng đã xác nhận")

        if order_status <= obj_db.status:

            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="Không thể cập nhật tình trạng cho đơn hàng này")

        if order_status == Const.ORDER_DELIVERED:
            payment_id = obj_db.payment_id
            payment_db = db.query(Payment).filter(
                Payment.id == payment_id,

            ).first()

            payment_db.status = Const.PAID
            db.merge(payment_db)
            db.commit()

        if order_status == Const.ORDER_REFUND_REQUEST:
            obj_db.cancel_reason = cancel_reason

        obj_db.status = order_status
        obj_db.update_id = user_id
        obj_db.update_at = datetime.now()

        db.merge(obj_db)
        db.commit()
        db.refresh(obj_db)

        return {
            'detail': "Đã cập nhật trạng thái đơn hàng"
        }

    def cancel_order(self, order_id, cancel_reason, db: Session, user_id):

        order_db = db.query(self.model).filter(
            self.model.id == order_id
        ).first()

        if order_db.status > Const.ORDER_CONFIRMED:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Không thể hủy đơn hàng đã được xác nhận!")

        order_db.status = Const.ORDER_CANCEL
        order_db.update_at = datetime.now()
        order_db.update_id = user_id
        order_db.cancel_reason = cancel_reason

        db.merge(order_db)
        db.commit()


        return {
            'detail': "Đã hủy đơn hàng thành công"
        }


crud_order = CRUDOrder(Order)

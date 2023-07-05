from datetime import datetime
from typing import Any
from crud import logger
from constants import Method, Target
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from fastapi.encoders import jsonable_encoder

from models.address import Address
from vnpay_python import views as CRUD_vnpay
import models
from models.product import Product

from crud.base import CRUDBase
from models.order import Order
from schemas.order import *
from crud.CRUD_order_product import crud_order_product
from crud.CRUD_product import crud_product
from crud.CRUD_payment import crud_payment
from crud.CRUD_cart import crud_cart
from crud.CRUD_address import crud_address
from crud.CRUD_user import crud_user
from constants import Const
from security.security import hash_password, verify_password, gen_token


class CRUDOrder(CRUDBase[Order, OrderCreate, OrderUpdate]):

    def get_product_by_id(self, id, db: Session):
        prd_data_db = db.query(Product).filter(
            Product.id == id
        ).first()
        if not prd_data_db:
            return None
        if prd_data_db.is_sale == 1:
            setattr(prd_data_db, 'sale_price', prd_data_db.price * (100 - prd_data_db.sale_percent) / 100)
        else:
            setattr(prd_data_db, 'sale_price', prd_data_db.price)
        return prd_data_db

    def get_order_by_id(self, order_id, db: Session, user_id):
        obj_db = db.query(self.model).filter(
            self.model.id == order_id,
            self.model.delete_flag == Const.DELETE_FLAG_NORMAL
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
            'insert_at': obj_db.insert_at
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

        payment_id = obj_db.payment_id
        payment_db = crud_payment.get_payment_by_id(id=payment_id, db=db)

        payment_insert_at = payment_db['insert_at']



        result['payment_type_id'] = payment_db['payment_type_id']
        result['payment_type'] = payment_db['payment_type_name']
        result['payment_status'] = payment_db['status']
        result['bankCode'] = payment_db['bankCode']
        result['transactionNo'] = payment_db['transactionNo']
        logger.log(Method.GET, Target.ORDER, comment=f"GET ORDER BY ID #{order_id}",
                   status=Target.SUCCESS,
                   id=user_id,
                   db=db)
        return result

    def get_all_orders_by_user_id(self, page, order_status, user_id, db: Session):
        order_db = db.query(self.model).filter(
            self.model.user_id == user_id,
            self.model.delete_flag == Const.DELETE_FLAG_NORMAL
        )
        if order_status is not None and order_status != -1:
            order_db = order_db.filter(
                self.model.status == order_status
            )

        total_order = order_db.count()
        total_page = int(total_order / Const.ROW_PER_PAGE_ORDER)
        if total_order % Const.ROW_PER_PAGE > 0:
            total_page += 1
        current_page = page
        if current_page < 1:
            current_page = 1
        if current_page > total_page > 0:
            current_page = total_page

        start = (current_page - 1) * Const.ROW_PER_PAGE

        order_db = order_db.order_by(self.model.insert_at.desc()).offset(start).limit(Const.ROW_PER_PAGE).all()

        if not order_db:
            logger.log(Method.GET, Target.ORDER, comment=f"GET ALL ORDER BY USER ID #{user_id}",
                       status=Target.FAIL,
                       id=user_id,
                       db=db)
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Không có đơn hàng")

        result = []
        for item in order_db:
            result.append(self.get_order_by_id(order_id=item.id, db=db, user_id=user_id))
        logger.log(Method.GET, Target.PRODUCT, comment=f"GET ALL ORDER BY USER ID #{user_id}",
                   status=Target.SUCCESS,
                   id=user_id,
                   db=db)
        return {
            'data': result,
            'current_page': current_page,
            'total_page': total_page
        }

    def get_all_orders(self, page, order_status, db: Session, admin_id):
        order_db = db.query(self.model).filter(
            self.model.delete_flag == Const.DELETE_FLAG_NORMAL
        )
        if order_status:
            order_db = order_db.filter(
                self.model.status == order_status
            )

        total_order = order_db.count()
        total_page = int(total_order / Const.ROW_PER_PAGE_ADMIN)
        if total_order % Const.ROW_PER_PAGE > 0:
            total_page += 1
        current_page = page
        if current_page < 1:
            current_page = 1
        if current_page > total_page > 0:
            current_page = total_page

        start = (current_page - 1) * Const.ROW_PER_PAGE

        order_db = order_db.order_by(self.model.insert_at.desc()).offset(start).limit(Const.ROW_PER_PAGE).all()

        if not order_db:
            logger.log(Method.GET, Target.ORDER, comment=f"GET ALL ORDERS",
                       status=Target.FAIL,
                       id=admin_id,
                       db=db)
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Không có đơn hàng")

        result = []
        for item in order_db:
            result.append(self.get_order_by_id(order_id=item.id, db=db, user_id=admin_id))
        logger.log(Method.GET, Target.PRODUCT, comment=f"GET ALL ORDERS",
                   status=Target.SUCCESS,
                   id=admin_id,
                   db=db)
        return {
            'data': result,
            'current_page': current_page,
            'total_page': total_page
        }

    def add_order(self, request, db: Session, user_id):
        # Add payment method
        payment_type_id = request.payment_type_id
        bankCode = ''
        txnRef = str(user_id) + str(datetime.now().strftime('%Y%m%d%H%M%S'))
        if payment_type_id == 2:
            bankCode = "COD"
        request_payment = {
            'payment_type_id': payment_type_id,
            'status': 99,
            'bankCode': bankCode,
            'txnRef': txnRef
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
        email = request.email
        status = 0
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
        cart_db = crud_cart.get_cart(user_id=user_id, db=db)
        prd_carts = cart_db['products']
        total_price = 0
        for item in prd_carts:
            product_id = item['prd_id']
            quantity = item['quantity']
            prd_name = item['name']
            img_url = item['img_url']
            price = item['sale_price']
            import_price = item['import_price']
            total_price += price * quantity
            order_product_obj_db = models.order_product.Order_Product(order_id=order_id, product_id=product_id,
                                                                      quantity=quantity, name=prd_name, img_url=img_url,
                                                                      price=price, insert_at=datetime.now(),
                                                                      import_price=import_price,
                                                                      insert_id=user_id, update_id=user_id,
                                                                      update_at=datetime.now())

            db.add(order_product_obj_db)
            db.commit()
            db.refresh(order_product_obj_db)

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

        crud_cart.delete_all_cart(db=db, user_id=user_id)

        # Update Address Info
        # address_update_info = {
        #     'city_id': request.city_id,
        #     'district_id': request.district_id,
        #     'ward_id': request.ward_id,
        #     'detail': request.detail
        # }
        #
        # crud_address.create_address(request=address_update_info, db=db, user_id=user_id)

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

        # user_update_info = {
        #     'name': name,
        #     'email': email,
        #     'phone_number': phone_number
        # }
        # crud_user.update_info(request=user_update_info, db=db, user_id=user_id)
        logger.log(Method.POST, Target.ORDER, comment=f"CREATE ORDER FOR USER ID #{user_id}",
                   status=Target.SUCCESS,
                   id=user_id,
                   db=db)

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

    def update_order_status(self, order_status, order_id, db: Session, user_id):
        obj_db = db.query(self.model).filter(
            self.model.id == order_id,
            self.model.delete_flag == Const.DELETE_FLAG_NORMAL
        ).first()
        if obj_db.status == 99:
            logger.log(Method.PUT, Target.ORDER, comment=f"UPDATE STATUS {order_status} OF ORDER ID #{order_id}",
                       status=Target.FAIL,
                       id=user_id, db=db)
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="Không thể cập nhật tình trạng cho đơn hàng này")

        if obj_db.status != 0 and order_status == 99:
            logger.log(Method.PUT, Target.ORDER, comment=f"UPDATE STATUS {order_status} OF ORDER ID #{order_id}",
                       status=Target.FAIL,
                       id=user_id, db=db)
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="Không thể huỷ đơn hàng đã xác nhận")

        if order_status <= obj_db.status:
            logger.log(Method.PUT, Target.ORDER, comment=f"UPDATE STATUS {order_status} OF ORDER ID #{order_id}",
                       status=Target.FAIL,
                       id=user_id, db=db)
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="Không thể cập nhật tình trạng cho đơn hàng này")

        obj_db.status = order_status
        obj_db.update_id = user_id
        obj_db.update_at = datetime.now()

        db.merge(obj_db)
        db.commit()
        db.refresh(obj_db)

        return {
            'detail': "Đã cập nhật trạng thái đơn hàng"
        }

    def cancel_order(self, order_id, db: Session, user_id):

        order_db = db.query(self.model).filter(
            self.model.id == order_id,
            self.model.user_id == user_id,
            self.model.delete_flag == Const.DELETE_FLAG_NORMAL
        ).first()

        if order_db.status != Const.ORDER_PENDING:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Không thể hủy đơn hàng này")

        order_db.status = Const.ORDER_CANCEL
        order_db.update_at = datetime.now()
        order_db.update_id = user_id

        db.merge(order_db)
        db.commit()

        logger.log(Method.DELETE, Target.ORDER, comment=f"CANCEL ORDER #{order_id}", status=Target.FAIL, id=user_id,
                   db=db)
        return {
            'detail': "Đã hủy đơn hàng thành công"
        }



crud_order = CRUDOrder(Order)

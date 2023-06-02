from datetime import datetime
from typing import Any

from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from fastapi.encoders import jsonable_encoder
import models
import schemas.user
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

    def get_order_by_id(self, order_id, db: Session):
        obj_db = db.query(self.model).filter(
            self.model.id == order_id,
            self.model.delete_flag == Const.DELETE_FLAG_NORMAL
        ).first()
        result = {
            'products': [],
            'total_price': 0,
            'name': obj_db.name,
            'phone_number': obj_db.phone_number,
            'email': obj_db.email,
            'address': obj_db.address,
            'status': obj_db.status,
            'payment_type': '',
            'payment_status': 0,
        }
        total_price = 0
        if obj_db:
            order_id = obj_db.id
            order_product_db = crud_order_product.get_by_order_id(order_id=order_id, db=db)
            for item in order_product_db:
                prd_id = order_product_db.prd_id
                prd_db = crud_product.get_product_by_id(id=prd_id, db=db)
                prd_name = prd_db.name
                prd_img_url = prd_db.img_url
                total_price += item.price * item.quantity
                prd_obj = {
                    'prd_id': prd_id,
                    'name': prd_name,
                    'img_url': prd_img_url,
                    'price': item.price,
                    'quantity': item.quantity,
                    'total_price': item.price * item.quantity
                }
                result['products'].append(prd_obj)

        return result

    def get_all_orders_by_user_id(self, user_id, db: Session):
        pass

    def add_order(self, request, db: Session, user_id):
        # Add payment method
        payment_type_id = request.payment_type_id
        request_payment = {
            'payment_type_id': payment_type_id,
            'status': 0
        }
        payment_db = crud_payment.add_payment(request=request_payment, db=db, user_id=user_id)

        # Add Order Info
        payment_id = payment_db.id
        name = request.name
        phone_number = request.phone_number
        email = request.email
        address = request.address
        status = request.status

        order_obj_db = self.model(user_id=user_id, payment_id=payment_id, name=name, phone_number=phone_number,
                                  email=email, address=address, status=status, insert_at=datetime.utcnow(),
                                  insert_id=user_id, update_id=user_id, update_at=datetime.utcnow())

        db.add(order_obj_db)
        db.commit()
        db.refresh(order_obj_db)

        # Add Order_Product Info
        order_id = order_obj_db.id
        cart_db = crud_cart.get_cart(user_id=user_id, db=db)
        prd_carts = cart_db['products']
        for item in prd_carts:
            product_id = item['prd_id']
            quantity = item['quantity']
            price = item['price']
            order_product_obj_db = models.order_product.Order_Product(order_id=order_id, product_id=product_id,
                                                                      quantity=quantity,
                                                                      price=price, insert_at=datetime.utcnow(),
                                                                      insert_id=user_id, update_id=user_id,
                                                                      update_at=datetime.utcnow())

            db.add(order_product_obj_db)
            db.commit()
            db.refresh(order_product_obj_db)

        # Delete Cart Info

        crud_cart.delete_all_cart(db=db, user_id=user_id)

        # Update Address Info
        address_update_info = {
            'city_id': request.city_id,
            'district_id': request.district_id,
            'ward_id': request.ward_id,
            'detail': request.detail
        }
        crud_address.create_address(request=address_update_info, db=db, user_id=user_id)

        # Update User Info

        user_update_info = {
            'name': name,
            'email': email,
            'phone_number': phone_number
        }
        crud_user.update_info(request=user_update_info, db=db, user_id=user_id)

        return {
            'detail': 'Đã đặt hàng thành công'
        }


crud_order = CRUDOrder(Order)

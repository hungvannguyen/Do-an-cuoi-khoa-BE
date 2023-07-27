import json
from datetime import datetime, timedelta

from fastapi import HTTPException
from sqlalchemy.orm import Session

from crud.CRUD_product import crud_product
from models.order import Order

from crud.CRUD_order import crud_order_product
from constants import Const
from models.product import Product
from models.product_quantity import ProductQuantity
from models.user import User


def total_income(db: Session, mode, year):
    order_db = db.query(Order).filter(
        Order.status >= Const.ORDER_DELIVERED,
        Order.status != Const.ORDER_REFUND,
        Order.status != Const.ORDER_CANCEL
    )

    total_income = 0
    total_profit = 0
    count = 0

    # month_count -= 1
    now = datetime.utcnow()

    if year is None:
        year = now.year
    day = 1

    days_in_month = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

    if (year % 4 == 0 and year % 100 != 0) or (year % 100 == 0 and year % 400 == 0):
        days_in_month[1] = 29

    if mode == 0:
        month = now.month
        first_date_current_month = datetime(year=year, month=month, day=1)
        end_date_current_month = datetime(year=year, month=month, day=days_in_month[month-1])
        order_db = order_db.filter(
            Order.insert_at >= first_date_current_month,
            Order.insert_at <= end_date_current_month
        )
    if 1 <= mode <= 5:
        start_month = 1
        end_month = 12
        start_day = 1
        end_day = 31

        if mode <= 4:
            start_month = 3 * (mode - 1) + 1
            end_month = 3 * mode
            end_day = days_in_month[end_month - 1]

        first_date_to_count = datetime(year=year, month=start_month, day=start_day)
        end_date_to_count = datetime(year=year, month=end_month, day=end_day)
        order_db = order_db.filter(
            Order.insert_at >= first_date_to_count,
            Order.insert_at <= end_date_to_count
        )

    order_db = order_db.all()

    for item in order_db:
        count += 1
        order_product_db = crud_order_product.get_by_order_id(order_id=item.id, db=db)
        for item2 in order_product_db:
            total_income += item2.price * item2.quantity
            total_profit += (item2.price - item2.import_price) * item2.quantity

    return {
        'total_income': total_income,
        'total_profit': total_profit,
        'order_count': count
    }


def order_count(db: Session, mode, year):
    total_count = 0
    cancel_count = 0
    pending_count = 0
    confirm_count = 0
    delivering_count = 0
    delivered_count = 0
    pending_refund = 0
    refunded_count = 0
    success_count = 0

    order_db = db.query(Order)

    now = datetime.utcnow()

    if year is None:
        year = now.year
    days_in_month = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

    if (year % 4 == 0 and year % 100 != 0) or (year % 100 == 0 and year % 400 == 0):
        days_in_month[1] = 29

    if mode == 0:
        month = now.month
        first_date_current_month = datetime(year=year, month=month, day=1)
        end_date_current_month = datetime(year=year, month=month, day=days_in_month[month-1])
        order_db = order_db.filter(
            Order.insert_at >= first_date_current_month,
            Order.insert_at <= end_date_current_month
        )
    if 1 <= mode <= 5:
        start_month = 1
        end_month = 12
        start_day = 1
        end_day = 31

        if mode <= 4:
            start_month = 3 * (mode - 1) + 1
            end_month = 3 * mode
            end_day = days_in_month[end_month - 1]

        first_date_to_count = datetime(year=year, month=start_month, day=start_day)
        end_date_to_count = datetime(year=year, month=end_month, day=end_day)
        order_db = order_db.filter(
            Order.insert_at >= first_date_to_count,
            Order.insert_at <= end_date_to_count
        )

    order_db = order_db.all()

    for item in order_db:
        total_count += 1
        if item.status == Const.ORDER_CANCEL:
            cancel_count += 1
        if item.status == Const.ORDER_PENDING:
            pending_count += 1
        if item.status == Const.ORDER_CONFIRMED:
            confirm_count += 1
        if item.status == Const.ORDER_DELIVERING:
            delivering_count += 1
        if item.status == Const.ORDER_DELIVERED:
            delivered_count += 1
        if item.status == Const.ORDER_REFUND:
            refunded_count += 1
        if item.status == Const.ORDER_REFUND_REQUEST:
            pending_refund += 1
        if item.status == Const.ORDER_SUCCESS:
            success_count += 1

    return {
        'total_order': total_count,
        'cancel_order': cancel_count,
        'pending_order': pending_count,
        'confirmed_order': confirm_count,
        'delivering_order': delivering_count,
        'delivered_order': delivered_count,
        'pending_refund_order': pending_refund,
        'refunded_order': refunded_count,
        'success_order': success_count
    }


def order_count_by_user_id(user_id: int, db: Session):
    total_count = 0
    cancel_count = 0
    pending_count = 0
    confirm_count = 0
    delivering_count = 0
    delivered_count = 0
    pending_refund = 0
    refunded_count = 0
    success_count = 0

    order_db = db.query(Order).filter(
        Order.user_id == user_id
    ).all()

    for item in order_db:
        total_count += 1
        if item.status == Const.ORDER_CANCEL:
            cancel_count += 1
        if item.status == Const.ORDER_PENDING:
            pending_count += 1
        if item.status == Const.ORDER_CONFIRMED:
            confirm_count += 1
        if item.status == Const.ORDER_DELIVERING:
            delivering_count += 1
        if item.status == Const.ORDER_DELIVERED:
            delivered_count += 1
        if item.status == Const.ORDER_REFUND:
            refunded_count += 1
        if item.status == Const.ORDER_REFUND_REQUEST:
            pending_refund += 1
        if item.status == Const.ORDER_SUCCESS:
            success_count += 1

    return {
        'total_order': total_count,
        'cancel_order': cancel_count,
        'pending_order': pending_count,
        'confirmed_order': confirm_count,
        'delivering_order': delivering_count,
        'delivered_order': delivered_count,
        'pending_refund_order': pending_refund,
        'refunded_order': refunded_count,
        'success_order': success_count
    }


def order_count_by_status(db: Session):
    total_count = 0
    cancel_count = 0
    pending_count = 0
    confirm_count = 0
    delivering_count = 0
    delivered_count = 0
    pending_refund = 0
    refunded_count = 0
    success_count = 0

    order_db = db.query(Order).all()

    for item in order_db:
        total_count += 1
        if item.status == Const.ORDER_CANCEL:
            cancel_count += 1
        if item.status == Const.ORDER_PENDING:
            pending_count += 1
        if item.status == Const.ORDER_CONFIRMED:
            confirm_count += 1
        if item.status == Const.ORDER_DELIVERING:
            delivering_count += 1
        if item.status == Const.ORDER_DELIVERED:
            delivered_count += 1
        if item.status == Const.ORDER_REFUND:
            refunded_count += 1
        if item.status == Const.ORDER_REFUND_REQUEST:
            pending_refund += 1
        if item.status == Const.ORDER_SUCCESS:
            success_count += 1

    return {
        'pending_order': pending_count,
        'pending_refund_order': pending_refund,
    }


def get_total_pending_orders(db: Session):
    count = db.query(Order).filter(
        Order.status == Const.ORDER_PENDING
    ).count()

    return {
        'count': count
    }


def get_total_pending_refund_orders(db: Session):
    count = db.query(Order).filter(
        Order.status == Const.ORDER_REFUND_REQUEST
    ).count()

    return {
        'count': count
    }


def get_price(user):
    return user['total_price']


def get_top_customer(db: Session):
    user_db = db.query(User).filter(
        User.is_confirmed == Const.IS_CONFIRMED,
        User.role_id == 99,
        User.delete_flag == Const.DELETE_FLAG_NORMAL
    ).all()
    arr = []
    stt = 0
    for user in user_db:
        user_id = user.id
        order_db = db.query(Order).filter(
            Order.user_id == user_id,
            Order.status >= Const.ORDER_DELIVERED,
            Order.status != Const.ORDER_REFUND,
            Order.status != Const.ORDER_CANCEL
        ).all()

        total_price = 0
        total_order = 0

        for order in order_db:
            total_order += 1
            total_price += order.total_price

        user_name = user.name
        obj = {
            'id': user_id,
            'name': user_name,
            'total_price': total_price,
            'total_order': total_order,
            'stt': 0
        }
        arr.append(obj)

    arr.sort(key=lambda x: x['total_price'], reverse=True)
    arr[0]['stt'] = 1
    arr[1]['stt'] = 2
    arr[2]['stt'] = 3
    return {
        'data': arr[0:3]
    }


def get_low_quantity_products(db: Session):
    data_db = db.query(Product).filter(
        Product.status == Const.ACTIVE_STATUS,
        Product.delete_flag == Const.DELETE_FLAG_NORMAL
    ).all()

    # total_quantity = 0
    arr = []
    for item in data_db:
        setattr(item, 'sale_price', item.price)
        if item.is_sale == 1:
            setattr(item, 'sale_price', item.price * (100 - item.sale_percent) / 100)

        prd_id = item.id
        quantity_obj = db.query(ProductQuantity).filter(
            ProductQuantity.prd_id == prd_id
        ).all()
        total_quantity = 0
        setattr(item, 'details', quantity_obj)
        for item2 in quantity_obj:
            total_quantity += item2.quantity

        item.quantity = total_quantity
        obj = {
            'id': item.id,
            'name': item.name,
            'quantity': item.quantity,
            'img_url': item.img_url,
            'import_price': item.import_price,
            'sale_price': item.sale_price,
            'is_sale': item.is_sale,
            'sale_percent': item.sale_percent,
        }
        arr.append(obj)

    arr.sort(key=lambda x: x['quantity'])

    return {
        'data': arr[0:5]
    }

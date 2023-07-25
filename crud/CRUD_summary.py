import json
from datetime import datetime, timedelta

from sqlalchemy.orm import Session

from models.order import Order

from crud.CRUD_order import crud_order_product
from constants import Const
from models.user import User


def total_income(db: Session, month_count):
    total_income = 0
    total_profit = 0
    count = 0

    month_count -= 1
    now = datetime.utcnow()
    month = now.month
    year = now.year
    day = 1

    days_in_month = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

    first_date_current_month = datetime(year=year, month=month, day=1)

    time_to_count = first_date_current_month - timedelta(
        days=month_count * days_in_month[month - 1] - 1
    )

    order_db = db.query(Order).filter(
        Order.status >= Const.ORDER_DELIVERED,
        Order.status != Const.ORDER_REFUND,
        Order.status != Const.ORDER_CANCEL,
        Order.insert_at >= time_to_count
    ).all()

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


def order_count(db: Session, month_count):
    total_count = 0
    cancel_count = 0
    pending_count = 0
    confirm_count = 0
    delivering_count = 0
    delivered_count = 0
    pending_refund = 0
    refunded_count = 0
    success_count = 0

    month_count -= 1
    now = datetime.utcnow()
    month = now.month
    year = now.year
    day = 1

    days_in_month = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

    first_date_current_month = datetime(year=year, month=month, day=1)

    time_to_count = first_date_current_month - timedelta(
        days=month_count * days_in_month[month - 1] - 1
    )

    order_db = db.query(Order).filter(Order.insert_at >= time_to_count).all()

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
            'total_order': total_order
        }
        arr.append(obj)

    arr.sort(key=lambda x: x['total_price'], reverse=True)
    return {
        'data': arr[0:3]
    }

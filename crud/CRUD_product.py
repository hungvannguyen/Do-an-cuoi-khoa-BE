import json
from datetime import datetime
from typing import Any

import sqlalchemy

from crud import logger
from constants import Method, Target
from sqlalchemy import asc, desc
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from fastapi.encoders import jsonable_encoder
from crud.CRUD_category import crud_category
from crud.CRUD_order_product import crud_order_product
from models.order import Order
from models.order_product import Order_Product
from models.product import Product
from models.product_quantity import ProductQuantity
from schemas.product import *
from crud.base import CRUDBase
from constants import Const
from security.security import hash_password, verify_password, gen_token


class CRUDProduct(CRUDBase[Product, ProductCreate, ProductUpdate]):

    def check_product_quantity(self, db: Session):
        prd_db = db.query(self.model).filter(
            self.model.status == Const.ACTIVE_STATUS,
            self.model.delete_flag == Const.DELETE_FLAG_NORMAL
        ).all()

        for item in prd_db:
            prd_id = item.id
            quantity_obj = db.query(ProductQuantity).filter(
                ProductQuantity.prd_id == prd_id
            ).all()
            total_quantity = 0
            setattr(item, 'details', quantity_obj)
            for item2 in quantity_obj:
                total_quantity += item2.quantity

            if total_quantity == 0:
                item.status = Const.NOT_ACTIVE_STATUS
                db.merge(item)
                db.commit()
                db.refresh(item)
        return None


    def get_all_products(self, page: int, condition, db: Session):

        self.check_product_quantity(db=db)

        current_page = page
        if current_page <= 0:
            current_page = 1
        # total_product = db.query(self.model).filter(
        #     self.model.delete_flag == Const.DELETE_FLAG_NORMAL
        # ).count()
        # total_page = int(total_product / Const.ROW_PER_PAGE_ADMIN)
        # if total_product % Const.ROW_PER_PAGE_ADMIN > 0:
        #     total_page += 1
        # if current_page > total_page and total_page > 0:
        #     current_page = total_page
        # offset = (current_page - 1) * Const.ROW_PER_PAGE_ADMIN
        # limit = Const.ROW_PER_PAGE_ADMIN

        data_db = db.query(self.model).filter(
            # self.model.status == Const.ACTIVE_STATUS,
            self.model.delete_flag == Const.DELETE_FLAG_NORMAL
        )
        if condition['sort'] == 1:
            data_db = data_db.order_by(
                asc(self.model.price * (100 - self.model.sale_percent) / 100)
            )
        if condition['sort'] == 2:
            data_db = data_db.order_by(
                desc(self.model.price * (100 - self.model.sale_percent) / 100)
            )
        if condition['sort'] == 3:
            data_db = data_db.filter(
                self.model.price * (100 - self.model.sale_percent) / 100 >= condition['min_price'],
                self.model.price * (100 - self.model.sale_percent) / 100 <= condition['max_price']
            )

        count = data_db.count()

        total_page = int(count / Const.ROW_PER_PAGE_ADMIN)
        if count % Const.ROW_PER_PAGE_ADMIN > 0:
            total_page += 1
        if current_page > total_page and total_page > 0:
            current_page = total_page
        offset = (current_page - 1) * Const.ROW_PER_PAGE_ADMIN
        limit = Const.ROW_PER_PAGE_ADMIN

        data_db = data_db.order_by(self.model.insert_at.desc()).offset(offset).limit(limit).all()

        if not data_db:

            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Không tìm thấy sản phẩm phù hợp")

        # total_quantity = 0
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

        # if condition['sort'] == 1:
        #     data_db.sort(key=lambda x: x.sale_price, reverse=False)
        # elif condition['sort'] == 2:
        #     data_db.sort(key=lambda x: x.sale_price, reverse=True)

        return {
            'data': data_db,
            'current_page': current_page,
            'total_page': total_page
        }

    def get_all_active_products(self, page: int, condition, db: Session):
        self.check_product_quantity(db=db)
        current_page = page
        if current_page <= 0:
            current_page = 1
        # total_product = db.query(self.model).filter(
        #     self.model.status == Const.ACTIVE_STATUS,
        #     self.model.delete_flag == Const.DELETE_FLAG_NORMAL
        # ).count()
        # total_page = int(total_product / Const.ROW_PER_PAGE)
        # if total_product % Const.ROW_PER_PAGE > 0:
        #     total_page += 1
        # if current_page > total_page and total_page > 0:
        #     current_page = total_page
        #
        # offset = (current_page - 1) * Const.ROW_PER_PAGE
        # limit = Const.ROW_PER_PAGE
        data_db = db.query(self.model).filter(
            self.model.status == Const.ACTIVE_STATUS,
            self.model.delete_flag == Const.DELETE_FLAG_NORMAL
        )
        if condition['sort'] == 1:
            data_db = data_db.order_by(
                asc(self.model.price * (100 - self.model.sale_percent) / 100)
            )
        if condition['sort'] == 2:
            data_db = data_db.order_by(
                desc(self.model.price * (100 - self.model.sale_percent) / 100)
            )
        if condition['sort'] == 3:
            data_db = data_db.filter(
                self.model.price * (100 - self.model.sale_percent) / 100 >= condition['min_price'],
                self.model.price * (100 - self.model.sale_percent) / 100 <= condition['max_price']
            )

        count = data_db.count()

        total_page = int(count / Const.ROW_PER_PAGE_ADMIN)
        if count % Const.ROW_PER_PAGE_ADMIN > 0:
            total_page += 1
        if current_page > total_page and total_page > 0:
            current_page = total_page
        offset = (current_page - 1) * Const.ROW_PER_PAGE_ADMIN
        limit = Const.ROW_PER_PAGE_ADMIN

        data_db = data_db.order_by(self.model.insert_at.desc()).offset(offset).limit(limit).all()
        if not data_db:

            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Không tìm thấy sản phẩm phù hợp")

        for item in data_db:
            setattr(item, 'sale_price', item.price)
            if item.is_sale == 1:
                setattr(item, 'sale_price', item.price * (100 - item.sale_percent) / 100)

        # if condition['sort'] == 1:
        #     data_db.sort(key=lambda x: x.sale_price, reverse=False)
        # elif condition['sort'] == 2:
        #     data_db.sort(key=lambda x: x.sale_price, reverse=True)

        return {
            'data': data_db,
            'current_page': current_page,
            'total_page': total_page
        }

    def get_product_by_id(self, id, db: Session):
        data_db = db.query(self.model).filter(
            self.model.id == id,
            # self.model.status == Const.ACTIVE_STATUS,
            self.model.delete_flag == Const.DELETE_FLAG_NORMAL
        ).first()
        if not data_db:

            return None

        if data_db.is_sale == 1:
            setattr(data_db, 'sale_price', data_db.price * (100 - data_db.sale_percent) / 100)
        else:
            setattr(data_db, 'sale_price', data_db.price)

        prd_id = data_db.id
        quantity_obj = db.query(ProductQuantity).filter(
            ProductQuantity.prd_id == prd_id
        ).all()
        total_quantity = 0
        for item in quantity_obj:
            total_quantity += item.quantity

        setattr(data_db, 'quantity', total_quantity)

        prd_id = data_db.id
        quantity_obj = db.query(ProductQuantity).filter(
            ProductQuantity.prd_id == prd_id
        ).all()

        setattr(data_db, 'details', quantity_obj)

        return data_db

    def get_product_by_id_for_cart(self, id, db: Session):
        data_db = db.query(self.model).filter(
            self.model.id == id,
            self.model.status == Const.ACTIVE_STATUS,
            self.model.delete_flag == Const.DELETE_FLAG_NORMAL
        ).first()
        if not data_db:

            return None

        if data_db.is_sale == 1:
            setattr(data_db, 'sale_price', data_db.price * (100 - data_db.sale_percent) / 100)
        else:
            setattr(data_db, 'sale_price', data_db.price)

        prd_id = data_db.id
        quantity_obj = db.query(ProductQuantity).filter(
            ProductQuantity.prd_id == prd_id
        ).all()
        total_quantity = 0
        for item in quantity_obj:
            total_quantity += item.quantity

        setattr(data_db, 'quantity', total_quantity)

        prd_id = data_db.id
        quantity_obj = db.query(ProductQuantity).filter(
            ProductQuantity.prd_id == prd_id
        ).all()

        setattr(data_db, 'details', quantity_obj)

        return data_db

    def get_sale_products(self, page: int, condition, db: Session):
        current_page = page
        if current_page <= 0:
            current_page = 1
        total_product = db.query(self.model).filter(
            self.model.status == Const.ACTIVE_STATUS,
            self.model.is_sale == Const.IS_SALE,
            self.model.delete_flag == Const.DELETE_FLAG_NORMAL
        ).count()
        total_page = int(total_product / Const.ROW_PER_PAGE)
        if total_product % Const.ROW_PER_PAGE > 0:
            total_page += 1
        if current_page > total_page and total_page > 0:
            current_page = total_page
        offset = (current_page - 1) * Const.ROW_PER_PAGE
        limit = Const.ROW_PER_PAGE
        data_db = db.query(self.model).filter(
            self.model.status == Const.ACTIVE_STATUS,
            self.model.is_sale == Const.IS_SALE,
            self.model.delete_flag == Const.DELETE_FLAG_NORMAL
        )

        if condition['sort'] == 1:
            data_db = data_db.order_by(
                asc(self.model.price * (100 - self.model.sale_percent) / 100)
            )
        if condition['sort'] == 2:
            data_db = data_db.order_by(
                desc(self.model.price * (100 - self.model.sale_percent) / 100)
            )

        if condition['sort'] == 3:
            data_db = data_db.filter(
                self.model.price * (100 - self.model.sale_percent) / 100 >= condition['min_price'],
                self.model.price * (100 - self.model.sale_percent) / 100 <= condition['max_price']
            )
        data_db = data_db.order_by(self.model.insert_at.desc()).offset(offset).limit(limit).all()
        if not data_db:

            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Không tìm thấy sản phẩm phù hợp")

        for item in data_db:
            setattr(item, 'sale_price', item.price)
            if item.is_sale == 1:
                setattr(item, 'sale_price', item.price * (100 - item.sale_percent) / 100)

        # if condition['sort'] == 1:
        #     data_db.sort(key=lambda x: x.sale_price, reverse=False)
        # elif condition['sort'] == 2:
        #     data_db.sort(key=lambda x: x.sale_price, reverse=True)

        return {
            'data': data_db,
            'current_page': current_page,
            'total_page': total_page
        }

    def get_new_products(self, page: int, db: Session):
        current_page = page
        if current_page <= 0:
            current_page = 1
        total_product = db.query(self.model).filter(
            self.model.status == Const.ACTIVE_STATUS,
            self.model.delete_flag == Const.DELETE_FLAG_NORMAL
        ).count()
        total_page = int(total_product / Const.ROW_PER_PAGE)
        if total_product % Const.ROW_PER_PAGE > 0:
            total_page += 1
        if current_page > total_page and total_page > 0:
            current_page = total_page
        offset = (current_page - 1) * Const.ROW_PER_PAGE
        limit = Const.ROW_PER_PAGE
        data_db = db.query(self.model).filter(
            self.model.status == Const.ACTIVE_STATUS,
            self.model.delete_flag == Const.DELETE_FLAG_NORMAL
        )
        data_db = data_db.order_by(self.model.insert_at.desc()).offset(offset).limit(limit).all()
        if not data_db:

            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Không tìm thấy sản phẩm phù hợp")

        for item in data_db:
            if item.is_sale == 1:
                setattr(item, 'sale_price', item.price * (100 - item.sale_percent) / 100)

        return {
            'data': data_db,
            'current_page': current_page,
            'total_page': total_page
        }

    def get_best_seller_products(self, db: Session):

        order_product_db = db.query(Order_Product.product_id, sqlalchemy.func.sum(Order_Product.quantity)) \
            .group_by(Order_Product.product_id) \
            .order_by(sqlalchemy.func.sum(Order_Product.quantity).desc()) \
            .all()

        # print(order_product_db[0][0])
        result = []
        count = 0
        for item in order_product_db:
            product_id = item[0]
            product_db = self.get_product_by_id(id=product_id, db=db)

            if product_db is not None and product_db.status == 1:
                count += 1
                product = {
                    "is_sale": product_db.is_sale,
                    "name": product_db.name,
                    "price": product_db.price,
                    'sale_price': product_db.sale_price,
                    "id": product_db.id,
                    "sale_percent": product_db.sale_percent,
                    "cat_id": product_db.cat_id,
                    "img_url": product_db.img_url,
                }
                result.append(product)

            if count == 3:
                return {
                    'data': result,
                    'count': count
                }

        return {
            'data': result,
            'count': count
        }

    def get_by_cat_id(self, cat_id, page, condition, db: Session):
        current_page = page
        if current_page <= 0:
            current_page = 1
        total_product = db.query(self.model).filter(
            self.model.status == Const.ACTIVE_STATUS,
            self.model.cat_id == cat_id,
            self.model.delete_flag == Const.DELETE_FLAG_NORMAL
        ).count()
        total_page = int(total_product / Const.ROW_PER_PAGE)
        if total_product % Const.ROW_PER_PAGE > 0:
            total_page += 1
        if current_page > total_page and total_page > 0:
            current_page = total_page
        offset = (current_page - 1) * Const.ROW_PER_PAGE
        limit = Const.ROW_PER_PAGE
        data_db = db.query(self.model).filter(
            self.model.status == Const.ACTIVE_STATUS,
            self.model.cat_id == cat_id,
            self.model.delete_flag == Const.DELETE_FLAG_NORMAL
        )
        if condition['sort'] == 1:
            data_db = data_db.order_by(
                asc(self.model.price * (100 - self.model.sale_percent) / 100)
            )
        if condition['sort'] == 2:
            data_db = data_db.order_by(
                desc(self.model.price * (100 - self.model.sale_percent) / 100)
            )
        if condition['sort'] == 3:
            data_db = data_db.filter(
                self.model.price * (100 - self.model.sale_percent) / 100 >= condition['min_price'],
                self.model.price * (100 - self.model.sale_percent) / 100 <= condition['max_price']
            )

        data_db = data_db.order_by(self.model.insert_at.desc()).offset(offset).limit(limit).all()
        if not data_db:

            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Không tìm thấy sản phẩm phù hợp")

        for item in data_db:
            setattr(item, 'sale_price', item.price)
            if item.is_sale == Const.IS_SALE:
                setattr(item, 'sale_price', item.price * (100 - item.sale_percent) / 100)

        # if condition['sort'] == 1:
        #     data_db.sort(key=lambda x: x.sale_price, reverse=False)
        # elif condition['sort'] == 2:
        #     data_db.sort(key=lambda x: x.sale_price, reverse=True)

        return {
            'data': data_db,
            'current_page': current_page,
            'total_page': total_page
        }

    def search_product(self, keyword: str, page: int, condition, db: Session):

        keyword = "%" + keyword.replace(" ", "%") + "%"

        current_page = page
        if current_page <= 0:
            current_page = 1
        total_product = db.query(self.model).filter(
            self.model.status == Const.ACTIVE_STATUS,
            self.model.name.like(keyword),
            self.model.delete_flag == Const.DELETE_FLAG_NORMAL
        ).count()
        total_page = int(total_product / Const.ROW_PER_PAGE)
        if total_product % Const.ROW_PER_PAGE > 0:
            total_page += 1
        if current_page > total_page and total_page > 0:
            current_page = total_page
        offset = (current_page - 1) * Const.ROW_PER_PAGE
        limit = Const.ROW_PER_PAGE
        data_db = db.query(self.model).filter(
            self.model.status == Const.ACTIVE_STATUS,
            self.model.name.like(keyword),
            self.model.delete_flag == Const.DELETE_FLAG_NORMAL
        )
        if condition['sort'] == 1:
            data_db = data_db.order_by(
                asc(self.model.price * (100 - self.model.sale_percent) / 100)
            )
        if condition['sort'] == 2:
            data_db = data_db.order_by(
                desc(self.model.price * (100 - self.model.sale_percent) / 100)
            )
        if condition['sort'] == 3:
            data_db = data_db.filter(
                self.model.price * (100 - self.model.sale_percent) / 100 >= condition['min_price'],
                self.model.price * (100 - self.model.sale_percent) / 100 <= condition['max_price']
            )
        data_db = data_db.order_by(self.model.insert_at.desc()).offset(offset).limit(limit).all()
        if not data_db:

            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Không tìm thấy sản phẩm phù hợp")

        for item in data_db:
            setattr(item, 'sale_price', item.price)
            if item.is_sale == Const.IS_SALE:
                setattr(item, 'sale_price', item.price * (100 - item.sale_percent) / 100)

        # if condition['sort'] == 1:
        #     data_db.sort(key=lambda x: x.sale_price, reverse=False)
        # elif condition['sort'] == 2:
        #     data_db.sort(key=lambda x: x.sale_price, reverse=True)

        return {
            'data': data_db,
            'current_page': current_page,
            'total_page': total_page
        }

    def search_product_for_admin(self, keyword: str, page: int, condition, db: Session):

        keyword = "%" + keyword.replace(" ", "%") + "%"

        current_page = page
        if current_page <= 0:
            current_page = 1
        total_product = db.query(self.model).filter(
            self.model.name.like(keyword),
            self.model.delete_flag == Const.DELETE_FLAG_NORMAL
        ).count()
        total_page = int(total_product / Const.ROW_PER_PAGE)
        if total_product % Const.ROW_PER_PAGE > 0:
            total_page += 1
        if current_page > total_page and total_page > 0:
            current_page = total_page
        offset = (current_page - 1) * Const.ROW_PER_PAGE
        limit = Const.ROW_PER_PAGE
        data_db = db.query(self.model).filter(
            self.model.name.like(keyword),
            self.model.delete_flag == Const.DELETE_FLAG_NORMAL
        )
        if condition['sort'] == 1:
            data_db = data_db.order_by(
                asc(self.model.price * (100 - self.model.sale_percent) / 100)
            )
        if condition['sort'] == 2:
            data_db = data_db.order_by(
                desc(self.model.price * (100 - self.model.sale_percent) / 100)
            )
        if condition['sort'] == 3:
            data_db = data_db.filter(
                self.model.price * (100 - self.model.sale_percent) / 100 >= condition['min_price'],
                self.model.price * (100 - self.model.sale_percent) / 100 <= condition['max_price']
            )
        data_db = data_db.order_by(self.model.insert_at.desc()).offset(offset).limit(limit).all()
        if not data_db:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Không tìm thấy sản phẩm phù hợp")

        for item in data_db:
            setattr(item, 'sale_price', item.price)
            if item.is_sale == Const.IS_SALE:
                setattr(item, 'sale_price', item.price * (100 - item.sale_percent) / 100)

        # if condition['sort'] == 1:
        #     data_db.sort(key=lambda x: x.sale_price, reverse=False)
        # elif condition['sort'] == 2:
        #     data_db.sort(key=lambda x: x.sale_price, reverse=True)

        return {
            'data': data_db,
            'current_page': current_page,
            'total_page': total_page
        }


    def create_product(self, request, db: Session, admin_id):
        request = request.dict()
        cat_id = request['cat_id']
        if request['is_sale'] == Const.IS_NOT_SALE:
            request['sale_percent'] = 0
        if crud_category.get_category_by_id(db=db, id=cat_id):
            data_db = self.model(**request, import_price=0, quantity=0, insert_id=admin_id, update_id=admin_id,
                                 insert_at=datetime.now(),
                                 update_at=datetime.now())
            db.add(data_db)
            db.commit()
            db.refresh(data_db)
        prd_name = request['name']
        logger.log(Method.POST, Target.PRODUCT, comment=f"TẠO MỚI SẢN PHẨM {prd_name}",
                   status=Target.SUCCESS,
                   id=admin_id,
                   db=db)
        return {
            'detail': "Tạo thành công"
        }

    def update_product(self, id, request, db: Session, admin_id):
        data_db = self.get_product_by_id(id, db=db)
        if not isinstance(request, dict):
            request = request.dict()
        if request['is_sale'] == Const.IS_NOT_SALE:
            request['sale_percent'] = 0
        self.update(db_obj=data_db, obj_in=request, db=db, admin_id=admin_id)
        logger.log(Method.POST, Target.PRODUCT, comment=f"CẬP NHẬT SẢN PHẨM ID #{id}",
                   status=Target.SUCCESS,
                   id=admin_id,
                   db=db)
        return {
            'detail': 'Cập nhật thành công'
        }

    def update_quantity(self, request, db: Session):
        data = str(request).replace("'", '"')
        data = json.loads(data)

        for item in data:
            detail_id = int(item['id'])
            quantity = int(item['quantity'])

            obj_db = db.query(ProductQuantity).filter(
                ProductQuantity.id == detail_id
            ).first()

            obj_db.quantity = quantity

            db.merge(obj_db)
            db.commit()

        return {
            'detail': "Cập nhật thành công"
        }

    def add_quantity(self, prd_id, quantity, db: Session, admin_id):
        prd_db = db.query(self.model).filter(
            self.model.id == prd_id,
            self.model.delete_flag == Const.DELETE_FLAG_NORMAL
        ).first()

        prd_db.quantity = prd_db.quantity + quantity
        prd_db.update_id = admin_id
        prd_db.update_at = datetime.now()
        db.merge(prd_db)
        db.commit()


        return {
            'detail': "Đã thêm thành công"
        }

    def get_all_for_import(self, db: Session):
        prd_db = db.query(self.model).filter(
            self.model.delete_flag == Const.DELETE_FLAG_NORMAL
        ).order_by(self.model.insert_at.desc()).all()

        return prd_db


crud_product = CRUDProduct(Product)

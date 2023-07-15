import json
from datetime import datetime, timedelta
from typing import Any
from crud import logger
from constants import Method, Target
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from fastapi.encoders import jsonable_encoder

from models.product_import import ProductImport
from models.product_import_detail import ProductImportDetail
from models.payment import Payment
from models.product_quantity import ProductQuantity


from crud.base import CRUDBase
from models.order import Order
from schemas.order import *



class CRUDImportProduct(CRUDBase[ProductImport, OrderBase, OrderCreate]):

    def create_import_invoice(self, request, db: Session, admin_id):
        data = str(request.data)
        data = data.replace("'", '"')
        data = json.loads(data)
        import_quantity = 0
        total_import_price = 0

        import_db = self.model(import_quantity=0, total_import_price=0, user_id=admin_id, import_at=datetime.now())
        db.add(import_db)
        db.commit()
        db.refresh(import_db)

        import_id = import_db.id

        for item in data:
            quantity = int(item['quantity'])
            prd_id = int(item['prd_id'])
            name = item['name']
            import_price = float(item['import_price'])
            import_quantity += quantity
            total_import_price += quantity * import_price

            # Thêm vào chi tiết hoá đơn nhập
            import_detail_db = ProductImportDetail(product_import_id=import_id, prd_id=prd_id, quantity=quantity,
                                                   import_price=import_price, name=name)

            db.add(import_detail_db)
            db.commit()
            db.refresh(import_detail_db)

            # Thêm vào bảng quantity
            quantity_obj = db.query(ProductQuantity).filter(
                ProductQuantity.prd_id == prd_id,
                ProductQuantity.import_price == import_price
            ).first()

            if quantity_obj:
                quantity_obj.quantity += quantity
                db.merge(quantity_obj)
                db.commit()
            else:
                quantity_new_obj = ProductQuantity(prd_id=prd_id, import_price=import_price, quantity=quantity)
                db.add(quantity_new_obj)
                db.commit()
                db.refresh(quantity_new_obj)

        import_db.import_quantity = import_quantity
        import_db.total_import_price = total_import_price
        db.merge(import_db)
        db.commit()

        return {
            'detail': "Đã nhập hàng thành công"
        }

    def get_inport_invoice(self, db: Session):

        template = {
            'user_id': 0,
            'import_at': None,
            'import_quantity': 0,
            'total_import_price': 0,
            'products': None
        }
        result = []
        import_db = db.query(self.model).all()
        for item in import_db:
            template['user_id'] = item.user_id
            template['import_at'] = item.import_at
            template['import_quantity'] = item.import_quantity
            template['total_import_price'] = item.total_import_price

            import_id = item.id

            products_import = db.query(ProductImportDetail).filter(
                ProductImportDetail.product_import_id == import_id
            ).all()

            template['products'] = products_import

        result.append(template)

        return result


crud_import_product = CRUDImportProduct(ProductImport)

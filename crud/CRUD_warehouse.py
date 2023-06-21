import json
from datetime import datetime
from typing import Any
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from fastapi.encoders import jsonable_encoder
from models.district import District
from models.city import City
from models.ward import Ward
from models.warehouse import Warehouse
from schemas.warehouse import *
from crud.base import CRUDBase
from crud.CRUD_address import crud_address
from constants import Const
from crud import logger
from constants import Method, Target


class CRUDWarehouse(CRUDBase[Warehouse, WarehouseCreate, WarehouseUpdate]):

    def get_warehouse_info(self, db: Session):
        data_db = db.query(self.model).filter(
            self.model.delete_flag == Const.DELETE_FLAG_NORMAL
        ).first()
        if not data_db:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Không tìm thấy kho hàng nào")
        city = crud_address.get_city_by_id(city_id=data_db.city_id, db=db)
        district = crud_address.get_district_by_id(district_id=data_db.district_id, db=db)
        ward = crud_address.get_ward_by_id(ward_id=data_db.ward_id, db=db)

        return {
            'id': data_db.id,
            'city': city.name,
            'district': district.name,
            'ward': ward.name,
            'detail': data_db.detail
        }

    def create_warehouse(self, request, db: Session, admin_id):
        if not isinstance(request, dict):
            request = request.dict()
        obj = self.model(**request, insert_id=admin_id, update_id=admin_id)
        db.add(obj)
        db.commit()
        db.refresh(obj)

        logger.log(Method.POST, Target.WAREHOUSE, comment="CREATE NEW WAREHOUSE", status=Target.SUCCESS, id=admin_id,
                   db=db)

        return {
            'detail': "Đã tạo kho hàng thành công"
        }




crud_warehouse = CRUDWarehouse(Warehouse)

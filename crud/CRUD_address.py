import json
from datetime import datetime
from typing import Any
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from fastapi.encoders import jsonable_encoder
from models.district import District
from models.city import City
from models.ward import Ward
from models.address import Address
from schemas.address import AddressInfo, AddressCreate, AddressUpdate
from crud.base import CRUDBase
from constants import Const
from security.security import hash_password, verify_password


class CRUDAddress(CRUDBase[Address, AddressCreate, AddressUpdate]):

    def get_all_cities(self, db: Session):
        data_db = db.query(City).all()
        return data_db

    def get_city_by_id(self, city_id, db: Session):
        data_db = db.query(City).filter(City.id == city_id).first()
        return data_db

    def get_all_districts(self, city_id, db: Session):
        data_db = db.query(District).filter(District.city_id == city_id).all()
        return data_db

    def get_district_by_id(self, district_id, db: Session):
        data_db = db.query(District).filter(District.id == district_id).first()
        return data_db

    def get_all_wards(self, city_id, district_id, db: Session):
        data_db = db.query(Ward).filter(Ward.city_id == city_id, Ward.district_id == district_id).all()
        return data_db

    def get_ward_by_id(self, ward_id, db: Session):
        data_db = db.query(Ward).filter(Ward.id == ward_id).first()
        return data_db

    def get_address_info_by_user_id(self, user_id, db: Session):
        data_db = db.query(self.model). \
            filter(
            self.model.user_id == user_id,
            self.model.delete_flag == Const.DELETE_FLAG_NORMAL
        ).first()
        if not data_db:
            return None
        city = self.get_city_by_id(city_id=data_db.city_id, db=db)
        district = self.get_district_by_id(district_id=data_db.district_id, db=db)
        ward = self.get_ward_by_id(ward_id=data_db.ward_id, db=db)
        return {
            'user_id': user_id,
            'city': city.id,
            'district': district.id,
            'ward': ward.id,
            'detail': data_db.detail
        }

    def get_address_by_user_id(self, user_id, db: Session):
        data_db = db.query(self.model). \
            filter(
            self.model.user_id == user_id,
            self.model.delete_flag == Const.DELETE_FLAG_NORMAL
        ).first()

        return data_db

    def create_address(self, request, db: Session, user_id):
        data_db = self.get_address_by_user_id(user_id=user_id, db=db)
        if data_db:
            return self.update_address(request=request, db=db, user_id=user_id)
        request = request.dict()
        data_db = self.model(**request, insert_id=user_id, update_id=user_id, user_id=user_id)
        db.add(data_db)
        db.commit()
        db.refresh(data_db)
        return {
            'detail': "Đã tạo Địa chỉ thành công"
        }

    def update_address(self, request, db: Session, user_id):
        data_db = self.get_address_by_user_id(user_id=user_id, db=db)
        self.update(db=db, obj_in=request, db_obj=data_db, admin_id=user_id)
        return {
            'detail': "Cập nhật thành công"
        }

    def delete_address(self, user_id, db: Session, admin_id):
        data_db = self.get_address_by_user_id(user_id, db)
        if not data_db:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"User ID #{user_id} chưa có Địa chỉ nào")
        self.delete(db=db, db_obj=data_db, admin_id=admin_id)
        return {
            'detail': "Đã xoá"
        }

    # def abcd(self, data, db: Session):
    #     data_obj = json.loads(data)
    #     for item in data_obj:
    #         city = City(name=item['name'])
    #         db.add(city)
    #         db.commit()
    #         db.refresh(city)
    #         city_id = city.id
    #         for item2 in item['districts']:
    #             district = District(city_id=city_id, name=item2['name'])
    #             db.add(district)
    #             db.commit()
    #             db.refresh(district)
    #             district_id = district.id
    #             for item3 in item2['wards']:
    #                 ward = Ward(city_id=city_id, district_id=district_id, name=item3['name'])
    #                 db.add(ward)
    #                 db.commit()
    #                 db.refresh(ward)
    #     return "success"


crud_address = CRUDAddress(Address)

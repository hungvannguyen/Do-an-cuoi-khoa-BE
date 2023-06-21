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
from crud import logger
from constants import Method, Target


class CRUDAddress(CRUDBase[Address, AddressCreate, AddressUpdate]):

    def get_all_cities(self, db: Session):

        logger.log(Method.GET, Target.CITY, comment="GET ALL CITIES", status=Target.SUCCESS, id=0, db=db)

        data_db = db.query(City).filter(
            City.delete_flag == Const.DELETE_FLAG_NORMAL
        ).all()
        return data_db

    def get_city_by_id(self, city_id, db: Session):

        logger.log(Method.GET, Target.CITY, comment="GET CITY BY ID", status=Target.SUCCESS, id=0, db=db)

        data_db = db.query(City).filter(
            City.id == city_id,
            City.delete_flag == Const.DELETE_FLAG_NORMAL
        ).first()
        return data_db

    def get_all_districts(self, city_id, db: Session):

        logger.log(Method.GET, Target.DISTRICT, comment="GET ALL DISTRICTS", status=Target.SUCCESS, id=0, db=db)

        data_db = db.query(District).filter(District.city_id == city_id,
                                            District.delete_flag == Const.DELETE_FLAG_NORMAL).all()
        return data_db

    def get_district_by_id(self, district_id, db: Session):

        logger.log(Method.GET, Target.DISTRICT, comment="GET DISTRICT BY ID", status=Target.SUCCESS, id=0, db=db)

        data_db = db.query(District).filter(District.id == district_id,
                                            District.delete_flag == Const.DELETE_FLAG_NORMAL).first()
        return data_db

    def get_all_wards(self, city_id, district_id, db: Session):

        logger.log(Method.GET, Target.WARD, comment="GET ALL WARDS", status=Target.SUCCESS, id=0, db=db)

        data_db = db.query(Ward).filter(Ward.city_id == city_id, Ward.district_id == district_id,
                                        Ward.delete_flag == Const.DELETE_FLAG_NORMAL).all()
        return data_db

    def get_ward_by_id(self, ward_id, db: Session):
        logger.log(Method.GET, Target.WARD, comment="GET WARD BY ID", status=Target.SUCCESS, id=0, db=db)
        data_db = db.query(Ward).filter(Ward.id == ward_id, Ward.delete_flag == Const.DELETE_FLAG_NORMAL).first()
        return data_db

    def get_address_info_by_user_id(self, user_id, db: Session):

        data_db = db.query(self.model). \
            filter(
            self.model.user_id == user_id,
            self.model.delete_flag == Const.DELETE_FLAG_NORMAL
        ).first()
        if not data_db:
            logger.log(Method.GET, Target.ADDRESS, comment=f"GET ADDRESS INFO OF USER #{user_id}", status=Target.FAIL,
                       id=user_id, db=db)
            return None
        city = self.get_city_by_id(city_id=data_db.city_id, db=db)
        district = self.get_district_by_id(district_id=data_db.district_id, db=db)
        ward = self.get_ward_by_id(ward_id=data_db.ward_id, db=db)
        logger.log(Method.GET, Target.ADDRESS, comment=f"GET ADDRESS INFO OF USER #{user_id}", status=Target.SUCCESS,
                   id=user_id, db=db)
        return {
            'user_id': user_id,
            'city_id': city.id,
            'district_id': district.id,
            'ward_id': ward.id,
            'detail': data_db.detail
        }

    def get_detail_address_by_user_id(self, user_id, db: Session):
        data_db = db.query(self.model). \
            filter(
            self.model.user_id == user_id,
            self.model.delete_flag == Const.DELETE_FLAG_NORMAL
        ).first()
        city = self.get_city_by_id(city_id=data_db.city_id,db=db)
        district = self.get_district_by_id(district_id=data_db.district_id, db=db)
        ward = self.get_ward_by_id(ward_id=data_db.ward_id, db=db)
        detail = data_db.detail
        return {
            'city': city.name,
            'district': district.name,
            'ward': ward.name,
            'detail': detail
        }

    def get_address_by_user_id(self, user_id, db: Session):
        logger.log(Method.GET, Target.ADDRESS, comment=f"GET ADDRESS BY USER ID #{user_id}", status=Target.SUCCESS,
                   id=0, db=db)
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
        if not isinstance(request, dict):
            request = request.dict()
        data_db = self.model(**request, insert_id=user_id, update_id=user_id, user_id=user_id)
        db.add(data_db)
        db.commit()
        db.refresh(data_db)
        logger.log(Method.POST, Target.ADDRESS, comment=f"CREATE USER #{user_id} ADDRESS", status=Target.SUCCESS,
                   id=user_id, db=db)
        return {
            'detail': "Đã tạo Địa chỉ thành công"
        }

    def update_address(self, request, db: Session, user_id):
        logger.log(Method.PUT, Target.ADDRESS, comment=f"UPDATE ADDRESS USER ID #{user_id}", status=Target.SUCCESS,
                   id=user_id, db=db)
        if not isinstance(request, dict):
            request = request.dict()
        data_db = self.get_address_by_user_id(user_id=user_id, db=db)
        self.update(db=db, obj_in=request, db_obj=data_db, admin_id=user_id)
        return {
            'detail': "Cập nhật thành công"
        }

    def delete_address(self, user_id, db: Session, admin_id):

        data_db = self.get_address_by_user_id(user_id, db)
        if not data_db:
            logger.log(Method.DELETE, Target.ADDRESS, comment=f"DELETE USER ID #{user_id} ADDRESS ",
                       status=Target.FAIL,
                       id=admin_id, db=db)
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"User ID #{user_id} chưa có Địa chỉ nào")
        self.delete(db=db, db_obj=data_db, admin_id=admin_id)
        logger.log(Method.DELETE, Target.ADDRESS, comment=f"DELETE USER ID #{user_id} ADDRESS ", status=Target.SUCCESS,
                   id=admin_id, db=db)
        return {
            'detail': "Đã xoá"
        }

    def abcd(self, data, db: Session):
        data_obj = json.loads(data)
        for item in data_obj:
            city = City(name=item['name'])
            db.add(city)
            db.commit()
            db.refresh(city)
            city_id = city.id
            for item2 in item['districts']:
                district = District(city_id=city_id, name=item2['name'])
                db.add(district)
                db.commit()
                db.refresh(district)
                district_id = district.id
                for item3 in item2['wards']:
                    ward = Ward(city_id=city_id, district_id=district_id, name=item3['name'])
                    db.add(ward)
                    db.commit()
                    db.refresh(ward)
        return "success"

    def delete_address_sample(self, db: Session):

        data_db = db.query(Ward).filter(
            Ward.delete_flag == Const.DELETE_FLAG_NORMAL
        ).all()
        if data_db:
            for item in data_db:
                item.delete_flag = 1
                db.add(item)
                db.commit()
                db.refresh(item)

        data_db = db.query(District).filter(
            District.delete_flag == Const.DELETE_FLAG_NORMAL
        ).all()
        if data_db:
            for item in data_db:
                item.delete_flag = 1
                db.add(item)
                db.commit()
                db.refresh(item)

        data_db = db.query(City).filter(
            City.delete_flag == Const.DELETE_FLAG_NORMAL
        ).all()
        if data_db:
            for item in data_db:
                item.delete_flag = 1
                db.add(item)
                db.commit()
                db.refresh(item)

        return {'success'}


crud_address = CRUDAddress(Address)

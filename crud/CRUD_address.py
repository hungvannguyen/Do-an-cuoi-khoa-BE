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

        data_db = db.query(City).all()
        return data_db

    def get_city_by_id(self, city_id, db: Session):

        logger.log(Method.GET, Target.CITY, comment="GET CITY BY ID", status=Target.SUCCESS, id=0, db=db)

        data_db = db.query(City).filter(
            City.id == city_id
        ).first()
        return data_db

    def get_all_districts(self, city_id, db: Session):

        logger.log(Method.GET, Target.DISTRICT, comment="GET ALL DISTRICTS", status=Target.SUCCESS, id=0, db=db)

        data_db = db.query(District).filter(District.city_id == city_id).all()
        return data_db

    def get_district_by_id(self, district_id, db: Session):

        logger.log(Method.GET, Target.DISTRICT, comment="GET DISTRICT BY ID", status=Target.SUCCESS, id=0, db=db)

        data_db = db.query(District).filter(District.id == district_id).first()
        return data_db

    def get_all_wards(self, city_id, district_id, db: Session):

        logger.log(Method.GET, Target.WARD, comment="GET ALL WARDS", status=Target.SUCCESS, id=0, db=db)

        data_db = db.query(Ward).filter(Ward.city_id == city_id, Ward.district_id == district_id).all()
        return data_db

    def get_ward_by_id(self, ward_id, db: Session):
        logger.log(Method.GET, Target.WARD, comment="GET WARD BY ID", status=Target.SUCCESS, id=0, db=db)
        data_db = db.query(Ward).filter(Ward.id == ward_id).first()
        return data_db

    def get_address_info_by_user_id(self, user_id, db: Session):

        data_db = db.query(self.model). \
            filter(
            self.model.user_id == user_id,
            self.model.delete_flag == Const.DELETE_FLAG_NORMAL
        ).all()
        if not data_db:
            logger.log(Method.GET, Target.ADDRESS, comment=f"GET ALL ADDRESS INFO OF USER #{user_id}",
                       status=Target.FAIL,
                       id=user_id, db=db)
            return None
        quantity = 0
        result = []

        for item in data_db:
            city = self.get_city_by_id(city_id=item.city_id, db=db)
            district = self.get_district_by_id(district_id=item.district_id, db=db)
            ward = self.get_ward_by_id(ward_id=item.ward_id, db=db)
            data = {
                'id': item.id,
                'name': item.name,
                'phone_number': item.phone_number,
                'city_id': city.id,
                'city': city.name,
                'district_id': district.id,
                'district': district.name,
                'ward_id': ward.id,
                'ward': ward.name,
                'detail': item.detail,
                'is_default': item.is_default
            }
            quantity += 1
            result.append(data)

        logger.log(Method.GET, Target.ADDRESS, comment=f"GET ALL ADDRESS INFO OF USER #{user_id}",
                   status=Target.SUCCESS,
                   id=user_id, db=db)
        return {
            'data': result,
            'quantity': quantity
        }

    def get_detail_address_by_user_id(self, user_id, db: Session):
        data_db = db.query(self.model). \
            filter(
            self.model.user_id == user_id,
            self.model.delete_flag == Const.DELETE_FLAG_NORMAL
        ).all()

        quantity = 0
        result = []

        for item in data_db:
            city = self.get_city_by_id(city_id=item.city_id, db=db)
            district = self.get_district_by_id(district_id=item.district_id, db=db)
            ward = self.get_ward_by_id(ward_id=item.ward_id, db=db)
            data = {
                'id': item.id,
                'name': item.name,
                'phone_number': item.phone_number,
                'city_id': city.name,
                'district_id': district.name,
                'ward_id': ward.name,
                'detail': item.detail,
                'is_default': item.is_default
            }
            quantity += 1
            result.append(data)

        logger.log(Method.GET, Target.ADDRESS, comment=f"GET ALL ADDRESS DETAIL OF USER #{user_id}",
                   status=Target.SUCCESS,
                   id=user_id, db=db)
        return {
            'data': result,
            'quantity': quantity
        }

    def get_address_detail_by_address_id(self, address_id, db: Session):
        logger.log(Method.GET, Target.ADDRESS, comment=f"GET ADDRESS BY  ID #{address_id}", status=Target.SUCCESS,
                   id=0, db=db)
        data_db = db.query(self.model). \
            filter(
            self.model.id == address_id,
            self.model.delete_flag == Const.DELETE_FLAG_NORMAL
        ).first()

        city = self.get_city_by_id(city_id=data_db.city_id, db=db)
        district = self.get_district_by_id(district_id=data_db.district_id, db=db)
        ward = self.get_ward_by_id(ward_id=data_db.ward_id, db=db)

        data = {
            'id': data_db.id,
            'name': data_db.name,
            'phone_number': data_db.phone_number,
            'city_id': city.id,
            'city': city.name,
            'district_id': district.id,
            'district': district.name,
            'ward_id': ward.id,
            'ward': ward.name,
            'detail': data_db.detail,
            'is_default': data_db.is_default
        }

        return data

    def create_address(self, request, db: Session, user_id):

        check_db = db.query(self.model).filter(
            self.model.user_id == user_id,
            self.model.delete_flag == Const.DELETE_FLAG_NORMAL
        ).count()

        is_default = Const.ADDRESS_DEFAULT
        if check_db > 0:
            is_default = Const.ADDRESS_NOT_DEFAULT

        if not isinstance(request, dict):
            request = request.dict()

        data_db = self.model(**request, is_default=is_default, user_id=user_id)
        db.add(data_db)
        db.commit()
        db.refresh(data_db)
        logger.log(Method.POST, Target.ADDRESS, comment=f"CREATE USER #{user_id} ADDRESS", status=Target.SUCCESS,
                   id=user_id, db=db)
        return {
            'detail': "Đã tạo Địa chỉ thành công"
        }

    def update_address(self, address_id, request, db: Session, user_id):
        logger.log(Method.PUT, Target.ADDRESS, comment=f"UPDATE ADDRESS USER ID #{user_id}", status=Target.SUCCESS,
                   id=user_id, db=db)

        add_db = db.query(self.model).filter(
            self.model.id == address_id,
            self.model.delete_flag == Const.DELETE_FLAG_NORMAL
        ).first()

        city_id = request.city_id if request.city_id else None
        district_id = request.district_id if request.district_id else None
        ward_id = request.ward_id if request.ward_id else None
        detail = request.detail if request.detail else None
        name = request.name if request.name else None
        phone_number = request.phone_number if request.phone_number else None

        add_db.city_id = city_id
        add_db.district_id = district_id
        add_db.ward_id = ward_id
        add_db.detail = detail
        add_db.name = name
        add_db.phone_number = phone_number

        db.merge(add_db)
        db.commit()

        return {
            'detail': "Cập nhật thành công"
        }

    def set_address_default(self, address_id: int, db: Session, user_id):
        add_db = db.query(self.model).filter(
            self.model.user_id == user_id,
            self.model.delete_flag == Const.DELETE_FLAG_NORMAL
        ).all()

        for item in add_db:

            if item.is_default == Const.ADDRESS_DEFAULT:
                item.is_default = Const.ADDRESS_NOT_DEFAULT
                db.merge(item)
                db.commit()

            if item.id == address_id:
                item.is_default = Const.ADDRESS_DEFAULT
                db.merge(item)
                db.commit()

        logger.log(Method.PUT, Target.ADDRESS, comment=f"SET ADDRESS DEFAULT IN USER ID #{user_id}",
                   status=Target.SUCCESS, id=user_id, db=db)

        return {
            'detail': "Đã cập nhật lại địa chỉ mặc định"
        }

    def delete_address(self, address_id, user_id, db: Session):

        add_db = db.query(self.model).filter(
            self.model.id == address_id,
            self.model.delete_flag == Const.DELETE_FLAG_NORMAL
        ).first()

        if add_db.is_default == Const.ADDRESS_DEFAULT:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Không thể xóa địa chỉ mặc định")

        # add_db.delete_flag = Const.DELETE_FLAG_DELETED
        # add_db.delete_at = datetime.now()
        # add_db.delete_id = user_id

        db.merge(add_db)
        db.commit()

        logger.log(Method.DELETE, Target.ADDRESS, comment=f"DELETE ADDRESS ID #{address_id} IN USER ID #{user_id}",
                   status=Target.SUCCESS, db=db, id=user_id)

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

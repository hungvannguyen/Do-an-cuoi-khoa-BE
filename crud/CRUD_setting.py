from datetime import datetime
from typing import Any
from crud import logger
from constants import Method, Target
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from fastapi.encoders import jsonable_encoder
import models
import schemas.user
from crud.base import CRUDBase
from models.settings import Settings
from schemas.setting import *
from crud.CRUD_cart import crud_cart
from crud.CRUD_user import crud_user
from crud.CRUD_address import crud_address
from constants import Const
from security.security import hash_password, verify_password, gen_token

class CRUDSetting(CRUDBase[Settings, SettingCreate, SettingUpdate]):

    def gen_settings(self, db: Session):
        setting_db = self.model(insert_id=0, insert_at=datetime.now(), update_id=0, update_at=datetime.now())
        db.add(setting_db)
        db.commit()
        db.refresh(setting_db)

        return setting_db

    def get_settings(self, db: Session):
        setting_db = db.query(self.model).filter(
            self.model.id == 1
        ).first()

        if setting_db is None:
            setting_db = self.gen_settings(db=db)

        return setting_db

    def update_settings(self, request, db: Session, admin_id):

        setting_db = self.get_settings(db=db)

        if not isinstance(request, dict):
            request = request.dict()

        banner_1 = request['banner_1'] if "banner_1" in request \
                                          and request['banner_1'] is not None else setting_db.banner_1
        banner_2 = request['banner_2'] if "banner_2" in request \
                                          and request['banner_2'] is not None else setting_db.banner_2
        banner_3 = request['banner_3'] if "banner_3" in request \
                                          and request['banner_3'] is not None else setting_db.banner_3
        banner_4 = request['banner_4'] if "banner_4" in request \
                                          and request['banner_4'] is not None else setting_db.banner_4
        banner_5 = request['banner_5'] if "banner_5" in request \
                                          and request['banner_5'] is not None else setting_db.banner_5
        sale_banner = request['sale_banner'] if "sale_banner" in request \
                                                and request['sale_banner'] is not None else setting_db.sale_banner
        intro_banner = request['intro_banner'] if "intro_banner" in request \
                                                  and request['intro_banner'] is not None else setting_db.intro_banner
        intro_text_1 = request['intro_text_1'] if "intro_text_1" in request \
                                                  and request['intro_text_1'] is not None else setting_db.intro_text_1
        intro_text_2 = request['intro_text_2'] if "intro_text_2" in request \
                                                  and request['intro_text_2'] is not None else setting_db.intro_text_2
        intro_text_3 = request['intro_text_3'] if "intro_text_3" in request \
                                                  and request['intro_text_3'] is not None else setting_db.intro_text_3
        intro_text_footer = request['intro_text_footer'] if "intro_text_footer" in request \
                                                            and request['intro_text_footer'] is not None else setting_db.intro_text_footer

        setting_db.banner_1 = banner_1
        setting_db.banner_2 = banner_2
        setting_db.banner_3 = banner_3
        setting_db.banner_4 = banner_4
        setting_db.banner_5 = banner_5
        setting_db.sale_banner = sale_banner
        setting_db.intro_banner = intro_banner
        setting_db.intro_text_1 = intro_text_1
        setting_db.intro_text_2 = intro_text_2
        setting_db.intro_text_3 = intro_text_3
        setting_db.intro_text_footer = intro_text_footer

        db.merge(setting_db)
        db.commit()

        return {
            'detail': "Đã cập nhật"
        }


crud_setting = CRUDSetting(Settings)

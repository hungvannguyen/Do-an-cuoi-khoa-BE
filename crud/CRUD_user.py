from datetime import datetime
from typing import Any
from crud import logger
from constants import Method, Target
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from fastapi.encoders import jsonable_encoder
import models
import schemas.user
from models.code_confirm import Code_Confirm
from models.user import User
from schemas.user import UserRegis, UserInfo
from crud.base import CRUDBase
from constants import Const
from security.security import hash_password, verify_password, gen_token


class CRUDUser(CRUDBase[User, UserRegis, UserInfo]):

    def get_all_roles(self, db: Session):
        data_db = db.query(models.role.Role).filter(
            models.role.Role.delete_flag == Const.DELETE_FLAG_NORMAL
        ).all()
        return data_db

    def get_user_by_id(self, db: Session, id):
        data_db = db.query(self.model).filter(
            self.model.id == id,
            self.model.delete_flag == Const.DELETE_FLAG_NORMAL
        ).first()
        return data_db

    def get_user_by_account(self, db: Session, account):
        data_db = db.query(self.model).filter(
            User.account == account,
            User.delete_flag == Const.DELETE_FLAG_NORMAL
        ).first()
        return data_db

    def get_user_info(self, db: Session, id):
        data_db = self.get_user_by_id(db, id)
        data_db = jsonable_encoder(data_db)
        return data_db

    def get_detail_by_user_id(self, user_id, db: Session):
        user_db = db.query(self.model).filter(
            self.model.id == user_id
        ).first()

        result = {
            'id': user_db.id,
            'name': user_db.name,
            'phone_number': user_db.phone_number,
            'email': user_db.email,
            'account': user_db.account,
            'role_id': user_db.role_id,
            'is_locked': user_db.is_locked,
            'insert_at': user_db.insert_at
        }

        return result

    def login(self, db: Session, account, password):
        account = str(account).lower()
        data_db = db.query(self.model).filter(
            self.model.account == account,
            self.model.delete_flag == Const.DELETE_FLAG_NORMAL
            # User.is_confirmed == Const.IS_CONFIRMED
        ).first()
        if data_db:
            if data_db.is_confirmed == Const.IS_NOT_CONFIRMED:
                logger.log(Method.GET, Target.USER, comment=f"LOGIN INTO ACCOUNT {account}",
                           status=Target.FAIL,
                           id=0,
                           db=db)
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                    detail=f"Tài khoản này chưa xác thực Email")
            data_db = jsonable_encoder(data_db)
            if verify_password(password, data_db['password']):
                logger.log(Method.GET, Target.USER, comment=f"LOGIN INTO ACCOUNT {account}",
                           status=Target.SUCCESS,
                           id=0,
                           db=db)

                if data_db['is_locked'] == Const.IS_LOCKED:
                    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Tài khoản này đã bị khóa")

                return gen_token(data_db), data_db['role_id']
        logger.log(Method.GET, Target.USER, comment=f"LOGIN INTO ACCOUNT {account}",
                   status=Target.FAIL,
                   id=0,
                   db=db)
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Tài khoản hoặc mật khẩu không chính xác")

    def create_user(self, db: Session, request) -> Any:
        account = str(request.account).lower()
        if not request.password == request.confirm_password:
            logger.log(Method.POST, Target.USER, comment=f"CREATE NEW USER {account}",
                       status=Target.FAIL,
                       id=0,
                       db=db)
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Mật khẩu không khớp")
        email = str(request.email).lower()
        email_db = db.query(self.model).filter(
            self.model.email == email,
            self.model.delete_flag == Const.DELETE_FLAG_NORMAL
        ).first()
        if email_db:
            logger.log(Method.POST, Target.USER, comment=f"CREATE NEW USER {account}",
                       status=Target.FAIL,
                       id=0,
                       db=db)
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Email này đã tồn tại")
        data_db = db.query(self.model).filter(
            self.model.account == account,
            self.model.delete_flag == Const.DELETE_FLAG_NORMAL
        ).first()
        if data_db:
            logger.log(Method.POST, Target.USER, comment=f"CREATE NEW USER {account}",
                       status=Target.FAIL,
                       id=0,
                       db=db)
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Tài khoản này đã tồn tại")
        else:
            request = request.dict()
            password = request['password']
            hashed_password = hash_password(password)
            request['password'] = hashed_password
            data_db = self.model(account=account, password=request['password'], email=email)
            db.add(data_db)
            db.commit()
            db.refresh(data_db)
            logger.log(Method.POST, Target.USER, comment=f"CREATE NEW USER {account}",
                       status=Target.SUCCESS,
                       id=0,
                       db=db)
            return {"result": "Tạo thành công"}

    def create_admin(self, db: Session, request, role_id) -> Any:
        account = request.account
        if not request.password == request.confirm_password:
            logger.log(Method.POST, Target.USER, comment=f"CREATE NEW ADMIN {account}",
                       status=Target.FAIL,
                       id=0,
                       db=db)
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Mật khẩu không khớp")
        email_db = db.query(self.model).filter(
            self.model.email == request.email,
            self.model.delete_flag == Const.DELETE_FLAG_NORMAL
        ).first()
        if email_db:
            logger.log(Method.POST, Target.USER, comment=f"CREATE NEW ADMIN {account}",
                       status=Target.FAIL,
                       id=0,
                       db=db)
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Email này đã tồn tại")
        data_db = db.query(self.model).filter(
            self.model.account == request.account,
            self.model.delete_flag == Const.DELETE_FLAG_NORMAL
        ).first()
        if data_db:
            logger.log(Method.POST, Target.USER, comment=f"CREATE NEW ADMIN {account}",
                       status=Target.FAIL,
                       id=0,
                       db=db)
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Tài khoản này đã tồn tại")
        else:
            request = request.dict()
            password = request['password']
            hashed_password = hash_password(password)
            request['password'] = hashed_password
            data_db = self.model(account=request['account'], password=request['password'], email=request['email'],
                                 role_id=role_id, is_confirmed=1)
            db.add(data_db)
            db.commit()
            db.refresh(data_db)
            logger.log(Method.POST, Target.USER, comment=f"CREATE NEW ADMIN {account}",
                       status=Target.SUCCESS,
                       id=0,
                       db=db)
            return {"result": "Tạo thành công"}

    def confirm_email(self, email, db: Session):
        email = str(email).lower()
        data_db = db.query(self.model).filter(
            self.model.email == email,
            self.model.is_confirmed == Const.IS_NOT_CONFIRMED,
            self.model.delete_flag == Const.DELETE_FLAG_NORMAL
        ).first()
        if not data_db:
            logger.log(Method.POST, Target.MAIL_CONFIRM, comment=f"CONFIRM EMAIL {email}",
                       status=Target.FAIL,
                       id=0,
                       db=db)
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Email không chính xác hoặc đã xác nhận")
        data_db.is_confirmed = Const.IS_CONFIRMED
        db.add(data_db)
        db.commit()
        db.refresh(data_db)
        logger.log(Method.POST, Target.MAIL_CONFIRM, comment=f"CONFIRM EMAIL {email}",
                   status=Target.SUCCESS,
                   id=0,
                   db=db)
        return {
            'detail': "Đã xác nhận Email thành công"
        }

    def reset_password(self, db: Session, account, admin_id) -> Any:
        data_db = db.query(self.model).filter(
            self.model.account == account,
            self.model.delete_flag == Const.DELETE_FLAG_NORMAL,
            self.model.is_confirmed == Const.IS_CONFIRMED
        ).first()
        if not data_db:
            logger.log(Method.PUT, Target.USER, comment=f"RESET PASSWORD USER {account}",
                       status=Target.FAIL,
                       id=admin_id,
                       db=db)
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f'Không tìm thấy tài khoản #{account}')
        data_db.update_at = datetime.now()
        data_db.update_id = admin_id
        new_password = hash_password(Const.PASSWORD_DEFAULT)
        data_db.password = new_password
        db.add(data_db)
        db.commit()
        db.refresh(data_db)
        logger.log(Method.PUT, Target.USER, comment=f"RESET PASSWORD USER {account}",
                   status=Target.SUCCESS,
                   id=0,
                   db=db)
        return {
            'detail': 'Đặt lại thành công'
        }

    def update_password(self, id, new_password, db: Session):
        user_db = self.get_user_by_id(db=db, id=id)
        new_hashed_password = hash_password(new_password)
        user_db.password = new_hashed_password
        db.add(user_db)
        db.commit()
        db.refresh(user_db)
        logger.log(Method.PUT, Target.USER, comment=f"UPDATE PASSWORD USER ID #{id}",
                   status=Target.SUCCESS,
                   id=id,
                   db=db)
        return {
            'detail': "Đã cập nhật mật khẩu"
        }

    def delete_account(self, id, db: Session):
        user_db = db.query(self.model).filter(
            self.model.id == id,
            self.model.delete_flag == Const.DELETE_FLAG_NORMAL
        ).first()
        if not user_db:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Account ID #{id} Not Found")
        user_db.delete_flag = Const.DELETE_FLAG_DELETED
        db.merge(user_db)
        db.commit()
        return {
            'detail': "Đã xoá"
        }

    def update_info(self, request, db: Session, user_id):

        if not isinstance(request, dict):
            request = request.dict()

        data_db = self.get_user_by_id(db, id=user_id)
        self.update(db=db, db_obj=data_db, obj_in=request, admin_id=user_id)
        logger.log(Method.PUT, Target.USER, comment=f"UPDATE USER INFO FOR USER ID #{user_id}",
                   status=Target.SUCCESS,
                   id=user_id,
                   db=db)
        return {
            'detail': 'Đã cập nhật địa chỉ'
        }

    def confirm_code(self, request, db: Session):
        code = request.code
        account = request.account

        user_db = db.query(User).filter(
            User.account == account,
            User.is_confirmed == Const.IS_CONFIRMED,
            User.delete_flag == Const.DELETE_FLAG_NORMAL
        ).first()

        if not user_db:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Không tìm thấy tài khoản")
        user_id = user_db.id
        code_db = db.query(Code_Confirm).filter(
            Code_Confirm.code == code,
            Code_Confirm.user_id == user_id,
            Code_Confirm.delete_flag == Const.DELETE_FLAG_NORMAL
        ).first()
        if not code_db:
            logger.log(Method.GET, Target.CODE_CONFIRM, comment=f"CONFIRM CODE IN ACCOUNT {account}",
                       status=Target.FAIL,
                       id=user_id,
                       db=db)
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Mã xác thực không chính xác")
        expire_time = code_db.expire_time
        now = datetime.now()
        if expire_time < now:
            logger.log(Method.GET, Target.CODE_CONFIRM, comment=f"CONFIRM CODE IN ACCOUNT {account}",
                       status=Target.FAIL,
                       id=user_id,
                       db=db)
            raise HTTPException(status_code=status.HTTP_408_REQUEST_TIMEOUT, detail="Mã xác thực đã hết hạn")
        code_db.delete_flag = Const.DELETE_FLAG_DELETED
        code_db.delete_at = datetime.now()
        code_db.delete_id = user_id
        db.merge(code_db)
        db.commit()
        db.refresh(code_db)
        logger.log(Method.GET, Target.CODE_CONFIRM, comment=f"CONFIRM CODE IN ACCOUNT {account}",
                   status=Target.SUCCESS,
                   id=user_id,
                   db=db)
        return {
            'detail': "Đã xác thực thành công"
        }

    def user_reset_password(self, account, password, db: Session):
        user_db = db.query(self.model).filter(
            self.model.account == account,
            self.model.delete_flag == Const.DELETE_FLAG_NORMAL
        ).first()
        hashed_password = hash_password(password)
        user_db.password = hashed_password
        user_db.update_at = datetime.now()
        db.merge(user_db)
        db.commit()
        logger.log(Method.GET, Target.USER, comment=f"RESET PASSWORD ACCOUNT {account}",
                   status=Target.SUCCESS,
                   id=user_db.id,
                   db=db)
        return {
            'detail': "Đã đặt lại mật khẩu"
        }

    def get_all_users_by_role(self, db: Session, role_id):
        obj_db = db.query(self.model).filter(
            self.model.role_id == role_id,
            self.model.is_confirmed == Const.IS_CONFIRMED,
            self.model.delete_flag == Const.DELETE_FLAG_NORMAL
        ).all()

        if not obj_db:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Không có người dùng nào")
        result = []

        for item in obj_db:
            user = {
                'id': item.id,
                'name': item.name,
                'phone_number': item.phone_number,
                'account': item.account,
                'email': item.email,
                'role_id': item.role_id,
                'insert_at': item.insert_at
            }

            result.append(user)

        return result

    def lock_account(self, user_id, db: Session, admin_id):
        user_db = db.query(self.model).filter(
            self.model.id == user_id,
            self.model.delete_flag == Const.DELETE_FLAG_NORMAL
        ).first()
        if user_db is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Không tìm thấy tài khoản này")

        if user_db.is_locked == Const.IS_LOCKED:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Tài khoản này đã bị khóa")

        if user_db.role_id == Const.ADMIN_ID:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Không thể khóa tài khoản admin")

        user_db.is_locked = Const.IS_LOCKED
        user_db.update_at = datetime.now()
        user_db.update_id = admin_id

        db.merge(user_db)
        db.commit()

        return {
            'detail': "Đã khóa"
        }

    def unlock_account(self, user_id, db: Session, admin_id):
        user_db = db.query(self.model).filter(
            self.model.id == user_id,
            self.model.is_locked == Const.IS_LOCKED,
            self.model.delete_flag == Const.DELETE_FLAG_NORMAL
        ).first()
        if user_db is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Không tìm thấy tài khoản này")

        user_db.is_locked = Const.IS_NOT_LOCKED
        user_db.update_at = datetime.now()
        user_db.update_id = admin_id

        db.merge(user_db)
        db.commit()

        return {
            'detail': "Đã mở khóa"
        }


crud_user = CRUDUser(User)

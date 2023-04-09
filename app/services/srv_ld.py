import firebase_admin
import jwt
from firebase_admin import credentials, db
from app.core.security import verify_password, get_password_hash
from app.helpers.exception_handler import CustomException
from app.models import User
from app.schemas.sche_base import DataResponse
from app.schemas.sche_ld import DeviceLd, LdUpdate, RegisterRequest
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer
from pydantic import ValidationError
from starlette import status

from app.core.config import settings
from app.schemas.sche_token import TokenPayload

# firebase configs
cred = credentials.Certificate("./ldpro-e59d4-firebase-adminsdk-eonx8-7cc2bfc18b.json")
firebase = firebase_admin.initialize_app(cred, {
    'databaseURL': "https://ldpro-e59d4-default-rtdb.asia-southeast1.firebasedatabase.app"
})


class LdService(object):
    __instance = None

    @classmethod
    def create_new_ld(cls, device_id: str, manager_id: int):
        try:
            device_ref = db.reference(f'device/{device_id}')
            value = device_ref.get()
            if value is not None:
                return DataResponse().success_response(data=value)
            else:
                device_ld = DeviceLd(manager_id=manager_id, device_id=device_id)
                print(device_ld.dict())
                device_ref.update(device_ld.dict())

            return DataResponse().success_response(data=device_ld)
        except Exception as e:
            msg = 'Firebase exception: {}'.format(str(e))
            raise CustomException(message=msg)

    @classmethod
    def update_ld(cls, device_id: str, form_data: LdUpdate):
        try:
            device_ref = db.reference(f'device/{device_id}')
            value = device_ref.get()
            if value is not None:
                device_ld = DeviceLd(**{**value, **form_data.dict()})
                device_ref.update(device_ld.dict())
            else:
                device_ld = DeviceLd(manager_id="1", **form_data.dict())
                device_ref.update(device_ld.dict())

            return DataResponse().success_response(data=device_ld)
        except Exception as e:
            msg = 'Firebase exception: {}'.format(str(e))
            raise CustomException(message=msg)

    @staticmethod
    def authenticate(*, email: str, password: str):
        """
        Check username and password is correct.
        Return object User if correct, else return None
        """
        manager_ref = db.reference('manager')
        manager_dict = manager_ref.get()

        user = None
        for key, value in manager_dict.items():
            if 'user_name' in value and value['user_name'] == email:
                if 'hashed_password' not in value or not value['hashed_password']:
                    value['hashed_password'] = get_password_hash(password)
                    manager_ref.child(key).update(value)
                user = User(id=key, is_active=True, **value)

        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user

    @classmethod
    def update_account(cls, user_id: str, form_data: RegisterRequest):
        try:
            user_ref = db.reference(f'manager/{user_id}')
            value = user_ref.get()

            user = {
                'user_name': form_data.user_name or value['user_name'],
                "full_name": form_data.full_name or value['full_name'],
                "hashed_password": get_password_hash(form_data.password) or value['hashed_password'],
                "role": form_data.role.value or value['role'],
            }

            user_ref.update(user)
            print(user)
            return DataResponse().success_response(data=user)
        except Exception:
            msg = 'Vui lòng điền đầy đủ thông tin'
            raise CustomException(message=msg)

    reusable_oauth2 = HTTPBearer(
        scheme_name='Authorization'
    )

    @staticmethod
    def get_current_user_ld(http_authorization_credentials=Depends(reusable_oauth2)) -> User:
        """
        Decode JWT token to get user_id => return User info from DB query
        """
        try:
            payload = jwt.decode(
                http_authorization_credentials.credentials, settings.SECRET_KEY,
                algorithms=[settings.SECURITY_ALGORITHM]
            )
            token_data = TokenPayload(**payload)

        except(jwt.PyJWTError, ValidationError):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Could not validate credentials",
            )

        user_ref = db.reference(f'manager/{token_data.user_id}')
        value = user_ref.get()

        if not value:
            raise HTTPException(status_code=404, detail="User not found")
        return User(**value)

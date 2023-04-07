import firebase_admin
from firebase_admin import credentials, db

from app.helpers.exception_handler import CustomException
from app.schemas.sche_base import DataResponse
from app.schemas.sche_ld import DeviceLd

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
            device_ref = db.reference(device_id)
            value = device_ref.get()
            if device_ref.get() is not None:
                return DataResponse().success_response(data=value)
            else:
                device_ld = DeviceLd(manager_id=manager_id, device_id=device_id)
                print(device_ld.dict())
                device_ref.update(device_ld.dict())

            return DataResponse().success_response(data=device_ld)
        except Exception as e:
            msg = 'Firebase exception: {}'.format(str(e))
            raise CustomException(message=msg)

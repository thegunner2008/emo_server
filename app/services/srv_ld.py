import time
import firebase_admin
from firebase_admin import credentials, db
from datetime import datetime, timedelta

from app.helpers.exception_handler import CustomException
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
            device_ld = DeviceLd(manager_id=manager_id, device_id=device_id)
            db.reference(device_id).update(device_ld.dict())

        except Exception as e:
            msg = 'Firebase exception: {}'.format(str(e))
            raise CustomException(message=msg)

from fastapi import HTTPException, Depends

from app.models import User
from app.services.srv_ld import LdService
from app.services.srv_user import UserService


def login_required(http_authorization_credentials=Depends(UserService().reusable_oauth2)):
    return UserService().get_current_user(http_authorization_credentials)


def login_required_ld(http_authorization_credentials=Depends(UserService().reusable_oauth2)):
    return LdService.get_current_user_ld(http_authorization_credentials)


class PermissionRequired:
    def __init__(self, *args):
        self.user = None
        self.permissions = args

    def __call__(self, user: User = Depends(login_required)):
        self.user = user
        if self.user.role not in self.permissions and self.permissions:
            raise HTTPException(status_code=400,
                                detail=f'User {self.user.email} can not access this api')


class PermissionRequiredLd:
    def __init__(self, *args):
        self.user = None
        self.permissions = args

    def __call__(self, user=Depends(login_required_ld)):
        self.user = user
        if self.user.get('role', 'guest') not in self.permissions and self.permissions:
            raise HTTPException(status_code=400,
                                detail=f'User {self.user.email} can not access this api')

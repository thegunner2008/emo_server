from fastapi import APIRouter

from app.api import api_user, api_login, api_register, api_healthcheck, api_job, api_withdraw, api_ld, api_transaction

router = APIRouter()

router.include_router(api_healthcheck.router, tags=["health-check"], prefix="/healthcheck")
router.include_router(api_login.router, tags=["login"], prefix="/login")
router.include_router(api_login.router, tags=["logout"], prefix="/logout")
router.include_router(api_register.router, tags=["register"], prefix="/register")
router.include_router(api_user.router, tags=["user"], prefix="/users")
router.include_router(api_job.router, tags=["job"], prefix="/jobs")
router.include_router(api_withdraw.router, tags=["withdraw"], prefix="/withdraws")
router.include_router(api_transaction.router, tags=["transaction"], prefix="/transactions")
router.include_router(api_ld.router, tags=["ld"], prefix="/ld")

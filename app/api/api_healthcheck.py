from fastapi import APIRouter

from app.helpers.time_int import time_int_short_day, time_int_short
from app.schemas.sche_base import ResponseSchemaBase

router = APIRouter()


@router.get("", response_model=ResponseSchemaBase)
async def get():
    return {"message": "Health check success - 08/12 "}

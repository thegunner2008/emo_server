from fastapi import APIRouter

from fastapi import Request, Header
from app.schemas.sche_base import ResponseSchemaBase

router = APIRouter()


@router.get("", response_model=ResponseSchemaBase)
async def get(request: Request, x_real_ip: str = Header(None, alias='X-Real-IP')):
    return {"message": f"Health check success - 28/12 x_real_ip = {x_real_ip} - {request.client}"}

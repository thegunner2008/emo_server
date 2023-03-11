import jwt
from app.core.config import settings
from pydantic import BaseModel


class TokenJob(BaseModel):
    job_id: int
    user_id: int
    current_id: int


def create_token_job(job_id: int, user_id: int, current_id: int, ) -> str:
    to_encode = TokenJob(
        job_id=job_id,
        user_id=user_id,
        current_id=current_id
    )

    encoded_jwt = jwt.encode(to_encode.dict(), settings.SECRET_KEY, algorithm=settings.SECURITY_ALGORITHM)
    return encoded_jwt


def decode_token_job(token: str) -> TokenJob:
    json = jwt.decode(
        token, settings.SECRET_KEY,
        algorithms=[settings.SECURITY_ALGORITHM]
    )
    return TokenJob(**json)

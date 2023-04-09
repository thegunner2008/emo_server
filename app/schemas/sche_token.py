from typing import Optional

from pydantic import BaseModel


class Token(BaseModel):
    accessToken: str
    tokenType: str = 'bearer'
    user: object


class TokenPayload(BaseModel):
    user_id: Optional[int] = None

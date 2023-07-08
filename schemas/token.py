from typing import Optional

from pydantic import BaseModel


class TokenPayload(BaseModel):
    id: Optional[int]
    name: Optional[str]
    address: Optional[str]
    phone_number: Optional[str]
    email: Optional[str]
    role_id: int

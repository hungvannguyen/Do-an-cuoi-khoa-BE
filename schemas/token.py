from typing import Optional

from pydantic import BaseModel


class TokenPayload(BaseModel):
    name: Optional[str]
    address: Optional[str]
    phone_number: Optional[str]
    role_id: int

from typing import Optional

from pydantic import BaseModel
from schemas.Default import Config


class ProductImportCreate(BaseModel):
    data: Optional[str]

from typing import Optional

from pydantic import BaseModel
from schemas.Default import Config


class CategoryBase(BaseModel, Config):
    id: Optional[int]


class CategoryInfo(CategoryBase):
    cat_name: Optional[str]
    cat_description: Optional[str]


class CategoryUpdate(BaseModel):
    cat_name: Optional[str]
    cat_description: Optional[str]


class CategoryCreate(CategoryUpdate):
    pass

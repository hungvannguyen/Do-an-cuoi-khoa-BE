from typing import Optional

from pydantic import BaseModel
from schemas.Default import Config


class SettingCreate(BaseModel, Config):
    banner_1: Optional[str]
    banner_2: Optional[str]
    banner_3: Optional[str]
    banner_4: Optional[str]
    banner_5: Optional[str]
    sale_banner: Optional[str]
    intro_banner: Optional[str]
    intro_text_1: Optional[str]
    intro_text_2: Optional[str]
    intro_text_3: Optional[str]
    intro_text_footer: Optional[str]


class SettingUpdate(SettingCreate):
    pass
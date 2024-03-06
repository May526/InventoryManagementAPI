from typing import Optional
import re

from pydantic import BaseModel, validator

from api.middlewares.http_request_middleware import InvalidParamException

class item(BaseModel):
    name: str
    amount: Optional[int] = 1

    @validator('name')
    def validate_name(cls, v):
        if not re.match(r'^[A-Za-z]{1,8}$', v):
            raise InvalidParamException()
        return v

    @validator('amount')
    def validate_amount(cls, v):
        if not re.match(r'^[1-9]\d*$', str(v)) or v <= 0:
            raise InvalidParamException()
        return v
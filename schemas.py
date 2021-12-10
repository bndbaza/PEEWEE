from typing import Any, List, Optional
from pydantic import BaseModel
from pydantic.utils import GetterDict
import datetime
import peewee

from models import Drawing

class PeeweeGetterDict(GetterDict):
    def get(self, key: Any, default: Any = None):
        res = getattr(self._obj, key, default)
        if isinstance(res, peewee.ModelSelect):
            return list(res)
        return res


class OrderBase(BaseModel):
  id: int
  create_date: datetime.datetime
  cas: str 

  class Config:
    orm_mode = True
    getter_dict = PeeweeGetterDict


class DrawingBase(BaseModel):
  id: int
  create_date: datetime.datetime
  cas: List[int]
  assembly: str
  area: float
  count: int
  weight: float
  more: float
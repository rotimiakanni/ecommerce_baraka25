from pydantic import BaseModel, Field, ConfigDict
from decimal import Decimal
from typing import Annotated, Optional


class ProductBase(BaseModel):
    name: str
    description: str | None = None
    price: Annotated[Decimal, Field(decimal_places=2, max_digits=10)]
    stock: int = 0
    is_active: bool = True


class ProductCreate(ProductBase):
    pass


class ProductRead(ProductBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class ProductUpdate(ProductBase):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[Annotated[Decimal, Field(decimal_places=2, max_digits=10)]] = None
    stock: Optional[int] = None
    is_active: Optional[bool] = None

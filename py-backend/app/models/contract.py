from typing import Optional, Literal
from datetime import datetime
from pydantic import BaseModel, Field, BeforeValidator
from typing_extensions import Annotated

PyObjectId = Annotated[str, BeforeValidator(str)]

class ContractModel(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    name: str
    status: Literal['active', 'draft', 'expired'] = 'draft'
    value: float = 0
    currency: str = 'USD'
    date: datetime = Field(default_factory=datetime.now)
    startDate: Optional[str] = None
    endDate: Optional[str] = None
    renewalPeriod: int = 0
    noticePeriod: int = 0
    autoRenewal: bool = False
    termsAndConditions: Optional[str] = None
    paymentTerms: Optional[str] = None
    contractType: str = 'Service Contract'
    business_id: str

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True

class ContractUpdate(BaseModel):
    name: Optional[str] = None
    status: Optional[str] = None
    value: Optional[float] = None
    currency: Optional[str] = None
    startDate: Optional[str] = None
    endDate: Optional[str] = None
    renewalPeriod: Optional[int] = None
    noticePeriod: Optional[int] = None
    autoRenewal: Optional[bool] = None
    termsAndConditions: Optional[str] = None
    paymentTerms: Optional[str] = None
    contractType: Optional[str] = None

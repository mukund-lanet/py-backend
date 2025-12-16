from typing import Optional, List, Any, Union
from pydantic import BaseModel, Field, BeforeValidator
from typing_extensions import Annotated
from .settings import IdentityVerificationSettings, GlobalDocumentSettings, BrandingSettings
from .document import DocumentModel
from .contract import ContractModel

PyObjectId = Annotated[str, BeforeValidator(str)]

class DocumentsFilters(BaseModel):
    all: int = 0
    draft: int = 0
    waiting: int = 0
    completed: int = 0
    archived: int = 0

class ContractsFilters(BaseModel):
    all: int = 0
    active: int = 0
    expired: int = 0

class Stats(BaseModel):
    totalDocuments: int = 0
    activeContracts: int = 0
    pendingSignatures: int = 0
    contractValue: float = 0

class ContractManagementBase(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    business_id: Optional[str] = "global"
    
    documentsFilters: DocumentsFilters = Field(default_factory=DocumentsFilters)
    contractsFilters: ContractsFilters = Field(default_factory=ContractsFilters)
    stats: Stats = Field(default_factory=Stats)
    
    identityVerificationSettings: IdentityVerificationSettings = Field(default_factory=IdentityVerificationSettings)
    globalDocumentSettings: GlobalDocumentSettings = Field(default_factory=GlobalDocumentSettings)
    brandingCustomizationSettings: BrandingSettings = Field(default_factory=BrandingSettings)

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True

class ContractManagementModel(ContractManagementBase):
    documents: List[PyObjectId] = [] 
    contracts: List[PyObjectId] = []

class ContractManagementPopulated(ContractManagementBase):
    documents: List[DocumentModel] = []
    contracts: List[ContractModel] = []

class ContractManagementUpdate(BaseModel):
    documentsFilters: Optional[DocumentsFilters] = None
    contractsFilters: Optional[ContractsFilters] = None
    stats: Optional[Stats] = None
    identityVerificationSettings: Optional[IdentityVerificationSettings] = None
    globalDocumentSettings: Optional[GlobalDocumentSettings] = None
    brandingCustomizationSettings: Optional[BrandingSettings] = None

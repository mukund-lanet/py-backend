from typing import Optional, List, Dict, Any, Union, Literal
from datetime import datetime
from pydantic import BaseModel, Field, BeforeValidator
from typing_extensions import Annotated
from .common import ISigner, IDocumentVariable, Page, CanvasElement

# Helper for ObjectId
PyObjectId = Annotated[str, BeforeValidator(str)]

class DocumentModel(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    name: str
    status: Literal['draft', 'waiting', 'completed', 'archived'] = 'draft'
    date: datetime = Field(default_factory=datetime.now)
    signers: List[ISigner] = []
    progress: int = 0
    dueDate: Optional[str] = None
    createdBy: Optional[str] = None
    signingOrder: bool = False
    variables: List[IDocumentVariable] = []
    business_id: str
    pages: List[Page] = []
    
    # PDF Editor State
    uploadPath: Optional[str] = None
    totalPages: int = 0
    canvasElements: List[CanvasElement] = []
    pageDimensions: Optional[Dict[str, Dict[str, float]]] = None
    documentType: Optional[Literal['upload-existing', 'new_document']] = 'new_document'

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True


class DocumentCreate(BaseModel):
    name: str = "Untitled Document"
    business_id: Optional[str] = None
    status: Optional[str] = 'draft'
    
    # Optional fields that might be passed on creation
    uploadPath: Optional[str] = None
    documentType: Optional[Literal['upload-existing', 'new_document']] = 'new_document'
    signers: Optional[List[ISigner]] = []
    
    # Editor State (allowing these to be passed on creation)
    pages: Optional[List[Page]] = []
    canvasElements: Optional[List[CanvasElement]] = []
    variables: Optional[List[IDocumentVariable]] = []
    pageDimensions: Optional[Dict[str, Dict[str, float]]] = None
    totalPages: Optional[int] = 0
    
    class Config:
        extra = 'allow' 

class DocumentUploadRequest(BaseModel):
    documentName: str = "Untitled Document"
    signers: Optional[List[ISigner]] = []
    uploadPath: str
    
class DocumentUpdate(BaseModel):
    name: Optional[str] = None
    status: Optional[str] = None
    signers: Optional[List[ISigner]] = None
    signingOrder: Optional[bool] = None
    dueDate: Optional[str] = None
    
    # Editor State
    uploadPath: Optional[str] = None
    canvasElements: Optional[List[CanvasElement]] = None
    pageDimensions: Optional[Dict[str, Dict[str, float]]] = None
    totalPages: Optional[int] = None
    variables: Optional[List[IDocumentVariable]] = None
    pages: Optional[List[Page]] = None

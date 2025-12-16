from typing import Optional, List, Union, Literal
from pydantic import BaseModel, Field

class ISigner(BaseModel):
    name: str
    email: str
    type: Literal['signer', 'approver', 'cc']
    order: Optional[int] = None

class IDocumentVariable(BaseModel):
    name: str
    value: str
    isSystem: Optional[bool] = None

class BoxSpacing(BaseModel):
    top: int = 0
    right: int = 0
    bottom: int = 0
    left: int = 0

# Correction: python uses float or int, no 'number'. Using float for safe measure or int. 
# Typescript number is float.
class BoxSpacing(BaseModel):
    top: float = 0
    right: float = 0
    bottom: float = 0
    left: float = 0

class BlockStyle(BaseModel):
    backgroundColor: Optional[str] = None
    padding: Optional[BoxSpacing] = None
    margin: Optional[BoxSpacing] = None

# Elements
class TextElement(BaseModel):
    type: Literal['text-field']
    id: str
    x: float
    y: float
    width: float
    height: float
    content: str
    page: int
    fontSize: Optional[float] = None
    color: Optional[str] = None
    required: Optional[bool] = None
    placeholder: Optional[str] = None
    # Extra fields from BlockStyle/others not explicitly in interface but maybe needed?
    # Interface says: textDecoration, textAlign, fontStyle, fontWeight
    textDecoration: Optional[str] = None
    textAlign: Optional[str] = None
    fontStyle: Optional[str] = None
    fontWeight: Optional[str] = None

class ImageElement(BlockStyle):
    type: Literal['image']
    id: str
    order: int
    height: float
    width: Optional[float] = None
    imageData: Optional[str] = None
    imageUrl: Optional[str] = None
    page: int
    align: Optional[Literal['left', 'center', 'right']] = None
    imageEffect: Optional[Literal['none', 'grayscale']] = None

class SignatureElement(BaseModel):
    type: Literal['signature']
    id: str
    x: float
    y: float
    width: float
    height: float
    imageData: str
    page: int
    content: Optional[str] = None
    showSignerName: Optional[bool] = None

class DateElement(BaseModel):
    type: Literal['date']
    id: str
    x: float
    y: float
    width: float
    height: float
    value: Optional[str] = None
    page: int
    placeholder: Optional[str] = None
    dateFormat: Optional[str] = None
    availableDates: Optional[str] = None
    required: Optional[bool] = None

class InitialsElement(BaseModel):
    type: Literal['initials']
    id: str
    x: float
    y: float
    width: float
    height: float
    content: str
    page: int

class CheckboxElement(BaseModel):
    type: Literal['checkbox']
    id: str
    x: float
    y: float
    width: float
    height: float
    checked: bool
    page: int
    required: Optional[bool] = None

class HeadingElement(BlockStyle):
    type: Literal['heading']
    id: str
    order: int
    height: float
    content: str
    subtitle: Optional[str] = None
    page: int
    fontSize: Optional[float] = None
    fontWeight: Optional[str] = None
    subtitleFontSize: Optional[float] = None
    subtitleFontWeight: Optional[str] = None
    subtitleColor: Optional[str] = None
    textAlign: Optional[Literal['left', 'center', 'right']] = None
    fontStyle: Optional[Literal['normal', 'italic']] = None
    textDecoration: Optional[Literal['none', 'underline']] = None
    color: Optional[str] = None
    fontFamily: Optional[str] = None
    tagName: Optional[Literal['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p']] = None

class VideoElement(BlockStyle):
    type: Literal['video']
    id: str
    order: int
    height: float
    width: Optional[float] = None
    videoUrl: Optional[str] = None
    page: int

class TableElement(BlockStyle):
    type: Literal['table']
    id: str
    order: int
    height: float
    rows: int
    columns: int
    data: Optional[List[List[str]]] = None
    page: int
    textAlign: Optional[Literal['left', 'center', 'right']] = None
    fontStyle: Optional[Literal['normal', 'italic']] = None
    textDecoration: Optional[Literal['none', 'underline']] = None
    color: Optional[str] = None
    fontSize: Optional[float] = None
    fontWeight: Optional[str] = None
    fontFamily: Optional[str] = None

# Union types
# ICanvasElement = BlockElement | FillableFieldElement
# BlockElement = HeadingElement | ImageElement | VideoElement | TableElement
# FillableFieldElement = TextElement | SignatureElement | DateElement | InitialsElement | CheckboxElement

CanvasElement = Union[
    HeadingElement, ImageElement, VideoElement, TableElement,
    TextElement, SignatureElement, DateElement, InitialsElement, CheckboxElement
]

class Page(BaseModel):
    pageSrc: Optional[str] = None
    fromPdf: bool = False
    imagePath: Optional[str] = None
    layout: List[CanvasElement] = []

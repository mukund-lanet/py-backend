from typing import Optional, Literal
from datetime import datetime
from pydantic import BaseModel, Field, BeforeValidator
from typing_extensions import Annotated

PyObjectId = Annotated[str, BeforeValidator(str)]

class IdentityVerificationSettings(BaseModel):
    isVarifyOn: bool = False
    verificationMethod: str = ""
    isRequireAllSigners: bool = False
    isRequirePhone: bool = False

class GlobalDocumentSettings(BaseModel):
    senderName: str = ""
    senderEmail: str = ""
    emailSubject: str = ""
    emailTemplate: str = "default"
    redirectDateNotification: bool = False
    dueDateNotification: bool = False
    completionNotification: bool = False
    reminderNotification: bool = False
    daysBeforeDueDate: int = 3

class BrandingSettings(BaseModel):
    senderName: str = ""
    senderEmail: str = ""
    emailSubjectLine: str = ""
    emailMessage: str = ""
    ctaButtonText: str = ""
    footerText: str = ""
    companyName: str = ""
    primaryColor: str = ""
    secondaryColor: str = ""
    accentColor: str = ""
    logo: Optional[str] = None

class SettingsModel(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    business_id: str
    identityVerification: IdentityVerificationSettings = Field(default_factory=IdentityVerificationSettings)
    globalDocument: GlobalDocumentSettings = Field(default_factory=GlobalDocumentSettings)
    branding: BrandingSettings = Field(default_factory=BrandingSettings)

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True

class SettingsUpdate(BaseModel):
    # Allow partial updates to nested fields?
    # Usually in a PUT whole object is sent, or we merge.
    # For now, following the mongoose model structure which is just one object.
    # But usually frontend sends the whole updated object.
    identityVerification: Optional[IdentityVerificationSettings] = None
    globalDocument: Optional[GlobalDocumentSettings] = None
    branding: Optional[BrandingSettings] = None

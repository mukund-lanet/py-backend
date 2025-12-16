from fastapi import APIRouter, HTTPException
from app.config.db import db
from app.models.settings import SettingsModel, SettingsUpdate

router = APIRouter(prefix="/api/settings", tags=["settings"])

@router.get("", response_model=SettingsModel)
async def get_settings(business_id: str):
    if not business_id:
        raise HTTPException(status_code=400, detail="business_id is required")
        
    settings = await db.settings.find_one({"business_id": business_id})
    
    if not settings:
        # Create default
        new_settings = SettingsModel(business_id=business_id)
        settings_dict = new_settings.model_dump(by_alias=True, exclude=["id"])
        res = await db.settings.insert_one(settings_dict)
        settings = await db.settings.find_one({"_id": res.inserted_id})
        
    return settings

@router.put("", response_model=SettingsModel)
async def update_settings(business_id: str, settings: SettingsUpdate):
    if not business_id:
        raise HTTPException(status_code=400, detail="business_id is required")
    
    # Using updates directly
    update_data = settings.model_dump(exclude_unset=True)
    
    # Using find_one_and_update with upsert logic as per node controller
    # Node: findOneAndUpdate({business_id}, {...req.body, business_id}, {new: true, upsert: true, setDefaultsOnInsert: true})
    
    # If update_data is nested (e.g. branding.logo), Pydantic dict might be nested. 
    # Mongo $set works fine with nested dicts replacing the whole sub-document unless dot notation is used.
    # Node body-parser usually sends branding[logo] as nested object.
    # Mongoose handles full object replacement for subdocs usually.
    # So `branding: { ... }` in $set will replace the `branding` field.
    # That matches logic.
    
    result = await db.settings.find_one_and_update(
        {"business_id": business_id},
        {"$set": update_data},
        upsert=True,
        return_document=True
    )
    # If upserted, it returns the doc.
    
    return result

from fastapi import APIRouter, HTTPException
from typing import List
from bson import ObjectId
from app.config.db import db
from app.models.contract import ContractModel, ContractUpdate

router = APIRouter(prefix="/api/contracts", tags=["contracts"])

@router.get("", response_model=List[ContractModel])
async def get_contracts(business_id: str):
    if not business_id:
        raise HTTPException(status_code=400, detail="business_id is required")
        
    contracts = await db.contracts.find({"business_id": business_id}).to_list(1000)
    return contracts

@router.get("/{id}", response_model=ContractModel)
async def get_contract_by_id(id: str, business_id: str):
    if not business_id:
        raise HTTPException(status_code=400, detail="business_id is required")
        
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="Invalid ID format")

    contract = await db.contracts.find_one({"_id": ObjectId(id), "business_id": business_id})
    if not contract:
        raise HTTPException(status_code=404, detail="Contract not found")
        
    return contract

@router.post("", response_model=ContractModel, status_code=201)
async def create_contract(contract: ContractModel, business_id: str):
    if not business_id:
        raise HTTPException(status_code=400, detail="business_id is required")
    
    contract_dict = contract.model_dump(by_alias=True, exclude=["id"])
    if contract.business_id != business_id:
        contract_dict['business_id'] = business_id
        
    new_contract = await db.contracts.insert_one(contract_dict)
    created_contract = await db.contracts.find_one({"_id": new_contract.inserted_id})
    return created_contract

@router.put("/{id}", response_model=ContractModel)
async def update_contract(id: str, business_id: str, contract: ContractUpdate):
    if not business_id:
        raise HTTPException(status_code=400, detail="business_id is required")
        
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="Invalid ID format")
        
    update_data = contract.model_dump(exclude_unset=True)
    
    if not update_data:
        pass

    result = await db.contracts.find_one_and_update(
        {"_id": ObjectId(id), "business_id": business_id},
        {"$set": update_data},
        return_document=True
    )
    
    if not result:
        raise HTTPException(status_code=404, detail="Contract not found")
        
    return result

@router.delete("/{id}")
async def delete_contract(id: str, business_id: str):
    if not business_id:
        raise HTTPException(status_code=400, detail="business_id is required")
    
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="Invalid ID format")

    result = await db.contracts.find_one_and_delete({"_id": ObjectId(id), "business_id": business_id})
    
    if not result:
        raise HTTPException(status_code=404, detail="Contract not found")
        
    return {"message": "Contract deleted successfully"}

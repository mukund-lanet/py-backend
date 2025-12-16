from fastapi import APIRouter, HTTPException
from typing import List
from bson import ObjectId
from app.config.db import db
from app.models.contract_management import ContractManagementModel, ContractManagementPopulated, ContractManagementUpdate
# We need to manually populate
from app.models.document import DocumentModel
from app.models.contract import ContractModel

router = APIRouter(prefix="/api/contract-management", tags=["contract_management"])

async def populate_state(state_dict: dict) -> dict:
    # Fetch documents
    doc_ids = state_dict.get("documents", [])
    if doc_ids:
        docs = await db.documents.find({"_id": {"$in": doc_ids}}).to_list(None)
    else:
        docs = []
    
    # Fetch contracts
    contract_ids = state_dict.get("contracts", [])
    if contract_ids:
        contracts = await db.contracts.find({"_id": {"$in": contract_ids}}).to_list(None)
    else:
        contracts = []
        
    state_dict["documents"] = docs
    state_dict["contracts"] = contracts
    return state_dict

@router.get("", response_model=ContractManagementPopulated)
async def get_contract_management_state():
    state = await db.contractmanagements.find_one()
    
    if not state:
        new_state = ContractManagementModel()
        state_dict = new_state.model_dump(by_alias=True, exclude=["id"])
        if "business_id" in state_dict and state_dict["business_id"] is None:
             state_dict["business_id"] = "global"
             
        res = await db.contractmanagements.insert_one(state_dict)
        state = await db.contractmanagements.find_one({"_id": res.inserted_id})
        
    return await populate_state(state)

@router.put("", response_model=ContractManagementPopulated)
async def update_contract_management_state(update: ContractManagementUpdate):
    update_data = update.model_dump(exclude_unset=True)
    
    result = await db.contractmanagements.find_one_and_update(
        {}, 
        {"$set": update_data},
        upsert=True,
        return_document=True
    )
    return await populate_state(result)

@router.post("/sync", response_model=ContractManagementPopulated)
async def sync_documents_list():
    docs_cursor = db.documents.find({}, {"_id": 1})
    docs = await docs_cursor.to_list(None)
    doc_ids = [d["_id"] for d in docs]
    
    contracts_cursor = db.contracts.find({}, {"_id": 1})
    contracts = await contracts_cursor.to_list(None)
    contract_ids = [c["_id"] for c in contracts]
    
    result = await db.contractmanagements.find_one_and_update(
        {},
        {"$set": {"documents": doc_ids, "contracts": contract_ids}},
        return_document=True,
        upsert=True
    )
    
    # Manual populate logic here too, though result contains just IDs.
    # populate_state will read those IDs and fetch objects.
    return await populate_state(result)

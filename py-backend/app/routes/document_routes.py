from fastapi import APIRouter, HTTPException, Request, Form, UploadFile, File, Body
from typing import List, Optional
from bson import ObjectId
from app.config.db import db
from app.models.document import DocumentModel, DocumentCreate, DocumentUpdate, DocumentUploadRequest
import json

router = APIRouter(prefix="/api/documents", tags=["documents"])

@router.get("", response_model=List[DocumentModel], response_model_by_alias=True)
async def get_documents(business_id: str):
    if not business_id:
        raise HTTPException(status_code=400, detail="business_id is required")
    
    documents = await db.documents.find({"business_id": business_id}).to_list(1000)
    return documents

@router.get("/{id}", response_model=DocumentModel, response_model_by_alias=True)
async def get_document_by_id(id: str, business_id: str):
    if not business_id:
        raise HTTPException(status_code=400, detail="business_id is required")
    
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="Invalid ID format")

    document = await db.documents.find_one({"_id": ObjectId(id), "business_id": business_id})
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    
    return document

@router.post("", response_model=DocumentModel, status_code=201, response_model_by_alias=True)
async def create_document(document: DocumentCreate, business_id: str):
    if not business_id:
        raise HTTPException(status_code=400, detail="business_id is required")
    
    doc_dict = document.model_dump(by_alias=True, exclude_none=True)
    
    # Ensure business_id is set from query if not in body (though model requires it)
    # The NodeJS controller takes ...req.body and adds business_id
    if document.business_id != business_id:
        # Override with query param? NodeJS allows body to override?
        # Node: ...req.body, business_id. So query param overwrites body.
        doc_dict['business_id'] = business_id
        
    doc_dict['status'] = 'draft' # Default
    # Add other defaults if needed, but Pydantic handles defaults.
    
    new_doc = await db.documents.insert_one(doc_dict)
    created_doc = await db.documents.find_one({"_id": new_doc.inserted_id})
    return created_doc

@router.put("/{id}", response_model=DocumentModel)
async def update_document(id: str, business_id: str, document: DocumentUpdate):
    if not business_id:
        raise HTTPException(status_code=400, detail="business_id is required")

    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="Invalid ID format")
        
    update_data = document.model_dump(exclude_unset=True)
    
    if not update_data:
         # Just return existing?
         pass

    # Node logic: matches { _id, business_id }
    result = await db.documents.find_one_and_update(
        {"_id": ObjectId(id), "business_id": business_id},
        {"$set": update_data},
        return_document=True
    )
    
    if not result:
        raise HTTPException(status_code=404, detail="Document not found")
        
    return result

@router.delete("/{id}")
async def delete_document(id: str, business_id: str):
    if not business_id:
        raise HTTPException(status_code=400, detail="business_id is required")
        
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="Invalid ID format")

    result = await db.documents.find_one_and_delete({"_id": ObjectId(id), "business_id": business_id})
    
    if not result:
        raise HTTPException(status_code=404, detail="Document not found")
        
    return {"message": "Document deleted successfully"}

@router.post("/upload", response_model=DocumentModel, status_code=201, response_model_by_alias=True)
async def upload_document_pdf(
    business_id: str,
    payload: DocumentUploadRequest = Body(...)
):
    if not business_id:
        raise HTTPException(status_code=400, detail="business_id is required")
    
    new_doc_data = {
        "name": payload.documentName,
        "uploadPath": payload.uploadPath,
        "documentType": "upload-existing",
        "signers": payload.signers,
        "status": "draft",
        "business_id": business_id,
        "totalPages": 0, # Default
        "pages": []
    }
    
    new_doc = await db.documents.insert_one(new_doc_data)
    created_doc = await db.documents.find_one({"_id": new_doc.inserted_id})
    return created_doc

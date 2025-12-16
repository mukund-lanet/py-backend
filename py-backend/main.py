import uvicorn
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from app.routes import document_routes, contract_routes, settings_routes, contract_management_routes

load_dotenv()

app = FastAPI(title="PDF to Image Backend", version="1.0.0")

# CORS Setup
origins = [
    "http://localhost:3000",
    "https://localhost:3000",
    "http://127.0.0.1:3000",
    "https://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers
app.include_router(document_routes.router)
app.include_router(contract_routes.router)
app.include_router(settings_routes.router)
app.include_router(contract_management_routes.router)

@app.get("/")
def read_root():
    return {"message": "Server is running"}

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8080))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)

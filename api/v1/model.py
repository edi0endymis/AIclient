from pydantic import BaseModel
from typing import List, Dict, Optional, Any

class ClientResponseRequest(BaseModel):
    client_id: str
    conversation: List[Dict[str, str]]
    api_key: Optional[str] = None

class ClientInfo(BaseModel):
    id: str
    name: str
    issue: str
    created_at: str
    current_stage: str

class ClientListResponse(BaseModel):
    success: bool
    clients: List[ClientInfo] 
    count: int
    api_version: str = "1.0.0"

class ClientResponse(BaseModel):
    success: bool
    response: str
    client_id: str
    version: str
    updated_state: Dict[str, Any]
    timestamp: str
from pydantic import BaseModel
from uuid import UUID
from typing import Optional, Dict


class AssignUserToPlantRequest(BaseModel):
    user_id: UUID
    plant_id: UUID
    permissions: Optional[Dict] = {"read": True}


class BulkAssignUsersRequest(BaseModel):
    plant_id: UUID
    user_ids: list[UUID]
    permissions: Optional[Dict] = {"read": True}

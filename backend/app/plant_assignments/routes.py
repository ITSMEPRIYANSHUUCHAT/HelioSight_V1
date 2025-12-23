from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.auth.dependencies import require_company_admin
from .schemas import (
    AssignUserToPlantRequest,
    BulkAssignUsersRequest,
)
from .services import (
    assign_user_to_plant,
    bulk_assign_users_to_plant,
)

router = APIRouter(prefix="/plant-assignments", tags=["Plant Assignments"])


@router.post("/assign")
def assign_user(
    payload: AssignUserToPlantRequest,
    db: Session = Depends(get_db),
    _: dict = Depends(require_company_admin),
):
    status = assign_user_to_plant(
        db,
        payload.user_id,
        payload.plant_id,
        payload.permissions,
    )
    return {"status": status}


@router.post("/bulk-assign")
def bulk_assign(
    payload: BulkAssignUsersRequest,
    db: Session = Depends(get_db),
    _: dict = Depends(require_company_admin),
):
    return bulk_assign_users_to_plant(
        db,
        payload.plant_id,
        payload.user_ids,
        payload.permissions,
    )

from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
import csv
import io

from sqlalchemy.orm import Session

from app.database import get_db
from app.auth.dependencies import get_current_user
from app.models.enums import UserRole

from .validators import validate_rows
from .services import process_bulk_upload
from .schemas import BulkUploadPreview, BulkUploadResult

router = APIRouter(prefix="/bulk-upload", tags=["Bulk Upload"])


@router.post("/preview", response_model=BulkUploadPreview)
def preview_csv(
    file: UploadFile = File(...),
):
    content = file.file.read().decode("utf-8")
    reader = csv.DictReader(io.StringIO(content))
    rows = list(reader)

    valid, errors = validate_rows(rows)

    return {
        "total_rows": len(rows),
        "valid_rows": len(valid),
        "invalid_rows": len(errors),
        "errors": errors[:10],
    }


@router.post("/commit", response_model=BulkUploadResult)
def commit_csv(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    if current_user.role != UserRole.company_admin:
        raise HTTPException(status_code=403, detail="Only company admins allowed")

    content = file.file.read().decode("utf-8")
    reader = csv.DictReader(io.StringIO(content))
    rows = list(reader)

    valid_rows, errors = validate_rows(rows)
    if errors:
        raise HTTPException(status_code=400, detail=errors[:10])

    result = process_bulk_upload(
        db=db,
        company_id=current_user.company_id,
        rows=valid_rows,
    )

    return result

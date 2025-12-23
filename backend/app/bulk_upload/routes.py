from fastapi import (
    APIRouter,
    Depends,
    UploadFile,
    File,
    Query,
    HTTPException,
)
from sqlalchemy.orm import Session

from app.database import get_db
from app.auth.dependencies import get_current_user
from app.models.enums import UserRole

from app.bulk_upload.schemas import BulkUploadRequest
from app.bulk_upload.parser import (
    parse_users_csv,
    parse_external_creds_csv,
)
from app.bulk_upload.validators import (
    validate_user_uniqueness,
    validate_external_creds,
    validate_provider_duplicates,
)
from app.bulk_upload.preview import bulk_preview as build_preview
from app.bulk_upload.services import bulk_create_users_and_creds

router = APIRouter(prefix="/bulk-upload", tags=["Bulk Upload"])

@router.get("/_debug-auth")
def debug_auth(user=Depends(get_current_user)):
    return {
        "user_id": str(user.id),
        "role": user.role.value,
        "company_id": str(user.company_id),
    }

@router.post("/users/file")
def bulk_upload_users_from_files(
    users_file: UploadFile = File(...),
    external_creds_file: UploadFile = File(...),
    dry_run: bool = Query(False),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """
    Bulk upload users + external provider credentials via CSV/XLSX files.

    - SYNC execution (for now)
    - ASYNC-ready (service layer reusable)
    - Company-admin only
    """

    # 🔐 Authorization
    if current_user.role != UserRole.company_admin:
        raise HTTPException(
            status_code=403,
            detail="Only company admins can perform bulk uploads",
        )

    # 📥 Parse files
    try:
        users = parse_users_csv(users_file)
        external_creds = parse_external_creds_csv(external_creds_file)
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Failed to parse uploaded files: {str(e)}",
        )

    if not users:
        raise HTTPException(
            status_code=400,
            detail="Users file is empty",
        )

    # ✅ Validations (pure + reusable)
    validate_user_uniqueness(users)
    validate_external_creds(users, external_creds)
    validate_provider_duplicates(external_creds)

    # 🧪 Dry-run mode (NO DB writes)
    if dry_run:
        return build_preview(users, external_creds)

    # 📦 Build payload
    payload = BulkUploadRequest(
        users=users,
        external_credentials=external_creds,
    )

    # 🚀 Execute sync service (async-ready later)
    result = bulk_create_users_and_creds(
        db=db,
        payload=payload,
        company_id=current_user.company_id,
    )

    return {
        "status": "success",
        "users_created": result["users_created"],
        "external_credentials_created": result["external_credentials_created"],
    }

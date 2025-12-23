from pydantic import BaseModel
from typing import List, Optional, Literal


# -------------------------
# USERS CSV
# -------------------------
class BulkUserRow(BaseModel):
    username: str
    email: Optional[str] = None
    fullname: Optional[str] = None
    role: Literal["end_user"] = "end_user"


# -------------------------
# EXTERNAL CREDS CSV
# -------------------------
class BulkExternalCredentialRow(BaseModel):
    username: str
    provider: str
    external_username: str
    external_password: str
    meta: Optional[dict] = None


# -------------------------
# REQUEST
# -------------------------
class BulkUploadRequest(BaseModel):
    users: List[BulkUserRow]
    external_credentials: List[BulkExternalCredentialRow]

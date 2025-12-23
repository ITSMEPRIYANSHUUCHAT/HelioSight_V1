from typing import List, Tuple
from .schemas import BulkUserRow


REQUIRED_FIELDS = [
    "username",
    "provider_type",
    "provider_username",
    "provider_password",
]


def validate_rows(rows: List[dict]) -> Tuple[List[BulkUserRow], List[str]]:
    valid = []
    errors = []

    for idx, row in enumerate(rows):
        missing = [f for f in REQUIRED_FIELDS if not row.get(f)]
        if missing:
            errors.append(f"Row {idx+1}: missing {missing}")
            continue

        try:
            valid.append(BulkUserRow(**row))
        except Exception as e:
            errors.append(f"Row {idx+1}: {str(e)}")

    return valid, errors

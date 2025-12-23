from fastapi import HTTPException
from collections import defaultdict


def validate_user_uniqueness(users):
    seen = set()
    for u in users:
        if u.username in seen:
            raise HTTPException(
                status_code=400,
                detail=f"Duplicate username in users.csv: {u.username}"
            )
        seen.add(u.username)


def validate_external_creds(users, external_creds):
    user_set = {u.username for u in users}

    for row in external_creds:
        if row.username not in user_set:
            raise HTTPException(
                status_code=400,
                detail=f"External credential references unknown user: {row.username}"
            )


def validate_provider_duplicates(external_creds):
    tracker = defaultdict(set)

    for row in external_creds:
        if row.provider in tracker[row.username]:
            raise HTTPException(
                status_code=400,
                detail=f"Duplicate provider '{row.provider}' for user '{row.username}'"
            )
        tracker[row.username].add(row.provider)

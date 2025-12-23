import csv
from io import TextIOWrapper
from typing import List

from app.bulk_upload.schemas import (
    BulkUserRow,
    BulkExternalCredentialRow,
)


def parse_users_csv(file) -> List[BulkUserRow]:
    reader = csv.DictReader(TextIOWrapper(file.file, encoding="utf-8"))
    rows = []

    for row in reader:
        rows.append(BulkUserRow(**row))

    return rows


def parse_external_creds_csv(file) -> List[BulkExternalCredentialRow]:
    reader = csv.DictReader(TextIOWrapper(file.file, encoding="utf-8"))
    rows = []

    for row in reader:
        rows.append(BulkExternalCredentialRow(**row))

    return rows

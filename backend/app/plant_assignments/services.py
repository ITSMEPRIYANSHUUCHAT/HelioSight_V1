from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.models.user_plant_assignment import UserPlantAssignment
from app.models.user import User
from app.models.plant import Plant


def assign_user_to_plant(
    db: Session,
    user_id,
    plant_id,
    permissions,
):
    exists = (
        db.query(UserPlantAssignment)
        .filter(
            UserPlantAssignment.user_id == user_id,
            UserPlantAssignment.plant_id == plant_id,
        )
        .first()
    )

    if exists:
        return "already_assigned"

    assignment = UserPlantAssignment(
        user_id=user_id,
        plant_id=plant_id,
        permissions=permissions,
    )

    db.add(assignment)
    db.commit()
    return "assigned"


def bulk_assign_users_to_plant(
    db: Session,
    plant_id,
    user_ids,
    permissions,
):
    created = 0
    skipped = 0

    for user_id in user_ids:
        exists = (
            db.query(UserPlantAssignment)
            .filter(
                UserPlantAssignment.user_id == user_id,
                UserPlantAssignment.plant_id == plant_id,
            )
            .first()
        )

        if exists:
            skipped += 1
            continue

        db.add(
            UserPlantAssignment(
                user_id=user_id,
                plant_id=plant_id,
                permissions=permissions,
            )
        )
        created += 1

    db.commit()
    return {
        "created": created,
        "skipped": skipped,
    }

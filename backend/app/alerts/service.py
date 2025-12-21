from sqlalchemy.orm import Session
from app.models.alert import Alert
from app.models.alert_recipient import AlertRecipient
from app.models.user import User
from app.models.assignment import PlantUserAssignment
from datetime import datetime


class AlertService:

    @staticmethod
    def raise_alert(db: Session, payload):
        alert = Alert(**payload.dict())
        db.add(alert)
        db.flush()

        # EPC admins first
        epc_admins = db.query(User).filter(
            User.company_id == alert.company_id,
            User.role == "admin"
        ).all()

        for admin in epc_admins:
            db.add(AlertRecipient(
                alert_id=alert.id,
                user_id=admin.id,
                recipient_type="epc"
            ))

        # Assigned users next
        if alert.plant_id:
            assignments = db.query(PlantUserAssignment).filter(
                PlantUserAssignment.plant_id == alert.plant_id
            ).all()

            for assignment in assignments:
                db.add(AlertRecipient(
                    alert_id=alert.id,
                    user_id=assignment.user_id,
                    recipient_type="user"
                ))

        db.commit()
        return alert

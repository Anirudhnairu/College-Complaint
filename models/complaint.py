from . import db


class Complaint(db.Model):

    __tablename__ = "complaints"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    title = db.Column(
        db.String(200),
        nullable=False
    )

    category = db.Column(
        db.String(100),
        nullable=False
    )

    description = db.Column(
        db.Text,
        nullable=False
    )

    status = db.Column(
        db.String(50),
        default="Pending"
    )

    assigned_to = db.Column(
        db.String(100),
        default="Not Assigned"
    )

    remarks = db.Column(
        db.Text,
        default=""
    )

    created_at = db.Column(
        db.DateTime,
        server_default=db.func.now()
    )
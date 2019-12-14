"""This module includes every number model used inside the API."""

from app import app, db

from key_manager import generate_key_digest, check_key


class Number(db.Model):

    """Models a number in the queue."""

    __tablename__ = "number"

    id = db.Column(db.Integer, primary_key=True)
    position = db.Column(db.Integer(), unique=True)
    key_digest = db.Column(db.String())

    def __init__(self, position, plain_key):
        self.position = position
        self.set_key_digest(plain_key)

    def set_key_digest(self, plain_key):
        """Sets secure key digest."""
        self.key_digest = generate_key_digest(plain_key)

    def check_plain_key(self, plain_key):
        """Checks plain key."""
        return check_key(plain_key, self.key_digest)

    def __repr__(self):
        return f"<Number - id {self.id}>"

    def serialize(self):
        """Generates the serialized view of the object."""
        return {
            "id": self.id,
            "position": self.position,
            "key_digest": self.key_digest
        }

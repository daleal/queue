"""
This module includes every model used inside the API to model the counter.
"""

from app import app, db


class Counter(db.Model):

    """Models the counter."""

    __tablename__ = "counter"

    id = db.Column(db.Integer, primary_key=True)
    counter = db.Column(db.Integer())

    def __init__(self):
        self.__counter = 1

    def get(self):
        """Returns the counter."""
        return self.__counter

    def increment(self):
        """Increments the counter."""
        self.__counter += 1

    def reset(self):
        """Resets the counter."""
        self.__counter = 1

    def __repr__(self):
        return f"<Counter - id {self.id}>"

    def serialize(self):
        """Generates the serialized view of the object."""
        return {
            "id": self.id,
            "counter": self.get()
        }

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
        self.counter = 1

    def get(self):
        """Returns the counter."""
        return self.counter

    def increment(self):
        """Increments the counter."""
        self.counter += 1

    def reset(self):
        """Resets the counter."""
        self.counter = 1

    def __repr__(self):
        return f"<Counter - id {self.id}>"

    def serialize(self):
        """Generates the serialized view of the object."""
        return {
            "id": self.id,
            "counter": self.get()
        }

    @staticmethod
    def get_counter():
        """Gets the counter from the database."""
        try:
            # Setup counter in database
            counter = Counter.query.one_or_none()
            if counter is None:
                counter = Counter()
                db.session.add(counter)
                db.session.commit()
            return counter
        except Exception as err:
            app.logger.error(err)

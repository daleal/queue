import os
from flask_script import Server, Manager
from flask_migrate import Migrate, MigrateCommand

from app import app, db


# Create objects
migrate = Migrate(app, db)  # Create migrator
manager = Manager(app)      # Create manager

# Migrations
manager.add_command("db", MigrateCommand)

# Development server
manager.add_command("runserver", Server(
    host="0.0.0.0", port="8000"))


if __name__ == "__main__":
    manager.run()

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
"""
Setup the database object which gets imported into all
required files to avoid circular imports.
"""

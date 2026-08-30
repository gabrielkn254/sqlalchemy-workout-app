from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
db = SQLAlchemy()

class Exercise(db.model):
    __tablename__ = "exercises"

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    category = db.Column(db.String(120), unique=True, nullable=False)
    equipment_needed = db.Column(db.Boolean, default=False, nullable=False)

    def to_dict(self):
        return {
            "id":self.id,
            "name":self.name,
            "category":self.category,
            "equipment_needed":self.equipment_needed
        }
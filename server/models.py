from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
from datetime import date, datetime

# create db
db = SQLAlchemy()

# Exercise model
class Exercise(db.Model):
    __tablename__ = "exercises"

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(120), nullable=False)
    category = db.Column(db.String(60), nullable=False)
    equipment_needed = db.Column(db.Boolean, default=False, nullable=False)

    workout = db.relationship("Workout", secondary="workout_exercise", backref=db.backref("exercises", viewonly=True))

    @validates("category")
    def validate_category(self, key, value):
        allowed_categories = ["Strength", "Cardio", "Flexibility", "Balance"]
        if value not in allowed_categories:
            raise ValueError(f"Category must be one of: {', '.join(allowed_categories)}")
        return value


# Workout model
class Workout(db.Model):
    __tablename__ = "workouts"

    id = db.Column(db.Integer, primary_key = True)
    date = db.Column(db.Date, nullable=False)
    duration_minutes = db.Column(db.Integer)
    notes = db.Column(db.Text)

    @validates("date")
    def validate_date(self, key, value):
        
        input_date = datetime.strptime(value, "%Y-%m-%d").date() if isinstance(value, str) else value
        if input_date > date.today():
            raise ValueError("Workout date cannot be set in the future.")
        return input_date


# WorkoutExercise model
class WorkoutExercises(db.Model):
    __tablename__ = "workout_exercises"

    id = db.Column(db.Integer, primary_key = True)

    workout_id = db.Column(db.Integer, db.ForeignKey("workouts.id"), nullable=False)
    excercise_id = db.Column(db.Integer, db.ForeignKey("exercises.id"), nullable=False)

    reps = db.Column(db.Integer, db.CheckConstraint("reps > 0", name="check_reps_positive"))
    sets = db.Column(db.Integer, db.CheckConstraint("sets > 0", name="check_sets_positive"))
    duration_seconds = db.Column(db.Integer, db.CheckConstraint("duration_seconds >= 0", name="check_duration_positive"))

    workout = db.relationship("Workout", backref=db.backref("workoutexercises", cascade="all, delete-orphan"))
    exercise = db.relationship("Exercise", backref=db.backref("workoutexercises", cascade="all, delete-orphan"))

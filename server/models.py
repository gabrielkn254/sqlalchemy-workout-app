from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
from datetime import datetime

# create db
db = SQLAlchemy()

# Exercise model
class Exercise(db.model):
    __tablename__ = "exercises"

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(120), nullable=False)
    category = db.Column(db.String(60), nullable=False)
    equipment_needed = db.Column(db.Boolean, default=False, nullable=False)

    workout = db.relationship("Workout", secondary="workout_exercise", backref=db.backref("exercises", viewonly=True))


# Workout model
class Workout(db.model):
    __tablename__ = "workouts"

    id = db.Column(db.Integer, primary_key = True)
    date = db.Column(db.Date, nullable=False)
    duration_minutes = db.Column(db.Integer)
    notes = db.Column(db.Text)


# WorkoutExercise model
class WorkoutExercises(db.model):
    __tablename__ = "workout_exercises"

    id = db.Column(db.Integer, primary_key = True)

    workout_id = db.Column(db.Integer, db.ForeignKey("workouts.id"), nullable=False)
    excercise_id = db.Column(db.Integer, db.ForeignKey("exercises.id"), nullable=False)

    reps = db.Column(db.Integer)
    sets = db.Column(db.Integer)
    duration_seconds = db.Column(db.Integer)

    workout = db.relationship("Workout", backref=db.backref("workoutexercises", cascade="all, delete-orphan"))
    exercise = db.relationship("Exercise", backref=db.backref("workoutexercises", cascade="all, delete-orphan"))

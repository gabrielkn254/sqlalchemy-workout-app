from app import app
from models import *

with app.app_context():
	# reset data and add new example data, committing to db
    print("Starting...")

    print("Deleting existing data...")
    WorkoutExercises.query.delete()
    Workout.query.delete()
    Exercise.query.delete()
    print("Existing data deleted.")


    print("Seeding new data...")
    ex1 = Exercise(name="Barbell Back Squat", category="Strength", equipment_needed=True)
    ex2 = Exercise(name="Treadmill Sprint", category="Cardio", equipment_needed=True)
    ex3 = Exercise(name="Bodyweight Lunge", category="Strength", equipment_needed=False)
    ex4 = Exercise(name="Yoga Sun Salutation", category="Flexibility", equipment_needed=False)
    
    db.session.add_all([ex1, ex2, ex3, ex4])
    db.session.commit()

    w1 = Workout(date=date.today(), duration_minutes=45, notes="Leg day focus. Felt strong.")
    w2 = Workout(date=date.today(), duration_minutes=30, notes="Quick morning cardio and stretch.")
    
    db.session.add_all([w1, w2])
    db.session.commit()


    log1 = WorkoutExercises(workout=w1, exercise=ex1, reps=8, sets=4, duration_seconds=0)
    log2 = WorkoutExercises(workout=w1, exercise=ex3, reps=12, sets=3, duration_seconds=0)
    log3 = WorkoutExercises(workout=w2, exercise=ex2, reps=1, sets=5, duration_seconds=900)
    log4 = WorkoutExercises(workout=w2, exercise=ex4, reps=5, sets=1, duration_seconds=600)

    db.session.add_all([log1, log2, log3, log4])
    db.session.commit()

    print("Seeding successfull!")
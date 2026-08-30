from flask import Flask, make_response, jsonify, request
from flask_migrate import Migrate
from schemas import *
from marshmallow import ValidationError
from pathlib import Path
from models import *

BASE_DIR = Path(__file__).resolve().parent

app = Flask(
    __name__,
    instance_path=str(BASE_DIR / "instance")
)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)

db.init_app(app)

# Initialize schema instances
workout_schema = WorkoutSchema()
workouts_schema = WorkoutSchema(many=True)
workout_detail_schema = WorkoutDetailSchema()

exercise_schema = ExerciseSchema()
exercises_schema = ExerciseSchema(many=True)
exercise_detail_schema = ExerciseDetailSchema()

workout_exercise_schema = WorkoutExercisesSchema()


# Workout routes -----------------------

@app.route('/workouts', methods=['GET'])
def get_workouts():
    """List all workouts"""

    workouts = Workout.query.all()

    return make_response(
        jsonify(workouts_schema.dump(workouts)), 200)


@app.route('/workouts/<int:id>', methods=['GET'])
def get_workout_by_id(id):
    """Show a single workout with its associated exercises (and sets/reps metrics)"""

    workout = Workout.query.get(id)
    if not workout:
        return make_response(jsonify({"error": "Workout not found"}), 404)
    
    return make_response(
        jsonify(workout_detail_schema.dump(workout)), 200)


@app.route('/workouts', methods=['POST'])
def create_workout():
    """Create a workout"""

    json_data = request.get_json()
    if not json_data:
        return make_response(jsonify({"error": "No input data provided"}), 400)
    
    try:
        # Validate and deserialize incoming JSON
        data = workout_schema.load(json_data)
        
        new_workout = Workout(
            date=data.get('date'),
            duration_minutes=data.get('duration_minutes'),
            notes=data.get('notes')
        )
        
        db.session.add(new_workout)
        db.session.commit()
        
        return make_response(jsonify(workout_schema.dump(new_workout)), 201)
    
    except ValidationError as err:
        return make_response(jsonify({"errors": err.messages}), 422)
    except ValueError as val_err:
        return make_response(jsonify({"error": str(val_err)}), 422)


@app.route('/workouts/<int:id>', methods=['DELETE'])
def delete_workout(id):
    """Delete a workout (and stretch goal: cascades down to remove associated WorkoutExercises)"""

    workout = Workout.query.get(id)
    if not workout:
        return make_response(jsonify({"error": "Workout not found"}), 404)
    
    # cascade="all, delete-orphan"
    db.session.delete(workout)
    db.session.commit()
    
    return make_response(jsonify({"message": "Workout and its associated records deleted successfully"}), 200)



# Exercise routes -----------------------

@app.route('/exercises', methods=['GET'])
def get_exercises():
    """List all exercises"""

    exercises = Exercise.query.all()
    return make_response(jsonify(exercises_schema.dump(exercises)), 200)


@app.route('/exercises/<int:id>', methods=['GET'])
def get_exercise_by_id(id):
    """Show an exercise and its associated workouts"""

    exercise = Exercise.query.get(id)
    if not exercise:
        return make_response(jsonify({"error": "Exercise not found"}), 404)
    
    return make_response(jsonify(exercise_detail_schema.dump(exercise)), 200)


@app.route('/exercises', methods=['POST'])
def create_exercise():
    """Create an exercise"""

    json_data = request.get_json()
    if not json_data:
        return make_response(jsonify({"error": "No input data provided"}), 400)
    
    try:
        # Validate and deserialize using Marshmallow criteria
        data = exercise_schema.load(json_data)
        
        new_exercise = Exercise(
            name=data.get('name'),
            category=data.get('category'),
            equipment_needed=data.get('equipment_needed', False)
        )
        
        db.session.add(new_exercise)
        db.session.commit()
        
        return make_response(jsonify(exercise_schema.dump(new_exercise)), 201)
        
    except ValidationError as err:
        return make_response(jsonify({"errors": err.messages}), 422)
    except ValueError as val_err:
        return make_response(jsonify({"error": str(val_err)}), 422)


@app.route('/exercises/<int:id>', methods=['DELETE'])
def delete_exercise(id):
    """Delete an exercise (and stretch goal: cascades down to remove associated WorkoutExercises)"""

    exercise = Exercise.query.get(id)
    if not exercise:
        return make_response(jsonify({"error": "Exercise not found"}), 404)
    
    db.session.delete(exercise)
    db.session.commit()
    
    return make_response(jsonify({"message": "Exercise and its log instances deleted successfully"}), 200)



# WorkoutExercises routes -----------------------

@app.route('/workouts/<int:workout_id>/exercises/<int:exercise_id>/workout_exercises', methods=['POST'])
def add_exercise_to_workout(workout_id, exercise_id):
    """Add an exercise to a workout, including reps/sets/duration metrics"""

    # Verify both resource parents exist
    workout = Workout.query.get(workout_id)
    exercise = Exercise.query.get(exercise_id)
    
    if not workout or not exercise:
        return make_response(jsonify({"error": "Parent Workout or Exercise resource not found"}), 404)
    
    json_data = request.get_json() or {}
    
    # Inject URL path IDs into payload data dictionary
    json_data['workout_id'] = workout_id
    json_data['exercise_id'] = exercise_id
    
    try:
        data = workout_exercise_schema.load(json_data)
        
        # Instantiate relationship log record
        new_log = WorkoutExercises(
            workout_id=data.get('workout_id'),
            exercise_id=data.get('exercise_id'),
            reps=data.get('reps'),
            sets=data.get('sets'),
            duration_seconds=data.get('duration_seconds')
        )
        
        db.session.add(new_log)
        db.session.commit()
        
        return make_response(jsonify(workout_exercise_schema.dump(new_log)), 201)
        
    except ValidationError as err:
        return make_response(jsonify({"errors": err.messages}), 422)
    except Exception as db_err:
        db.session.rollback()
        return make_response(jsonify({"error": "Invalid data configuration or duplicate record entry", "details": str(db_err)}), 400)

if __name__ == '__main__':

    # create tables
    with app.app_context():
        db.create_all()
    app.run(port=5555, debug=True)
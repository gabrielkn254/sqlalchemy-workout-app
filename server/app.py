from flask import Flask, make_response, jsonify
from flask_migrate import Migrate
from schemas import *

from models import *

app = Flask(__name__)
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
    # TODO: Deserialize request body with validation, save, and return record
    return make_response(jsonify({"message": "Placeholder: POST create a new workout"}), 201)


@app.route('/workouts/<int:id>', methods=['DELETE'])
def delete_workout(id):
    """Delete a workout (and stretch goal: cascades down to remove associated WorkoutExercises)"""
    # TODO: Query workout, remove it, session.commit(), and return response
    return make_response(jsonify({"message": f"Placeholder: DELETE workout with ID {id}"}), 200)



# Exercise routes -----------------------

@app.route('/exercises', methods=['GET'])
def get_exercises():
    """List all exercises"""
    # TODO: Serialize using ExerciseSchema(many=True)
    return make_response(jsonify({"message": "Placeholder: GET all exercises"}), 200)


@app.route('/exercises/<int:id>', methods=['GET'])
def get_exercise_by_id(id):
    """Show an exercise and its associated workouts"""
    # TODO: Serialize using ExerciseSchema with nested Workouts history data
    return make_response(jsonify({"message": f"Placeholder: GET exercise with ID {id}"}), 200)


@app.route('/exercises', methods=['POST'])
def create_exercise():
    """Create an exercise"""
    # TODO: Deserialize request body with validation, save, and return record
    return make_response(jsonify({"message": "Placeholder: POST create a new exercise"}), 201)


@app.route('/exercises/<int:id>', methods=['DELETE'])
def delete_exercise(id):
    """Delete an exercise (and stretch goal: cascades down to remove associated WorkoutExercises)"""
    # TODO: Query exercise, remove it, session.commit(), and return response
    return make_response(jsonify({"message": f"Placeholder: DELETE exercise with ID {id}"}), 200)



# WorkoutExercises routes -----------------------

@app.route('/workouts/<int:workout_id>/exercises/<int:exercise_id>/workout_exercises', methods=['POST'])
def add_exercise_to_workout(workout_id, exercise_id):
    """Add an exercise to a workout, including reps/sets/duration metrics"""
    # TODO: Create and save a new WorkoutExercises entry referencing both parent IDs
    return make_response(jsonify({
        "message": f"Placeholder: POST linked exercise {exercise_id} to workout {workout_id} successfully"
    }), 201)

if __name__ == '__main__':
    app.run(port=5555, debug=True)
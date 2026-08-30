from marshmallow import Schema, fields, validate


class ExerciseSchema(Schema):
    
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True, validate=validate.Length(min=1, max=100))
    
    # Category validation
    category = fields.Str(
        required=True, 
        validate=validate.OneOf(["Strength", "Cardio", "Flexibility", "Balance"])
    )
    equipment_needed = fields.Bool(load_default=False)


class WorkoutSchema(Schema):
    
    id = fields.Int(dump_only=True)

    # Formats date strings
    
    date = fields.Date(required=True)
    duration_minutes = fields.Int(validate=validate.Range(min=1))
    notes = fields.Str()


class WorkoutExercisesSchema(Schema):

    id = fields.Int(dump_only=True)
    workout_id = fields.Int(required=True)
    exercise_id = fields.Int(required=True)
    reps = fields.Int(validate=validate.Range(min=1))
    sets = fields.Int(validate=validate.Range(min=1))
    duration_seconds = fields.Int(validate=validate.Range(min=0))

    # Nested fields to load parent data cleanly inside the join rows
    workout = fields.Nested("WorkoutSchema", dump_only=True)
    exercise = fields.Nested("ExerciseSchema", dump_only=True)



class WorkoutDetailSchema(WorkoutSchema):

    # Pulls the related metrics via your backref field name
    workoutexercises = fields.Nested("WorkoutExercisesSchema", many=True, dump_only=True)


class ExerciseDetailSchema(ExerciseSchema):
    """Includes direct historical Workout entries inside an Exercise query"""
    workoutexercises = fields.Nested("WorkoutExercisesSchema", many=True, dump_only=True)
from marshmallow import Schema, fields, validate


class ExerciseSchema(Schema):
    
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True, validate=validate.Length(min=1, max=100))
    
    category = fields.Str(
        required=True, 
        validate=validate.OneOf(["Strength", "Cardio", "Flexibility", "Balance"])
    )
    equipment_needed = fields.Bool(load_default=False,)


class WorkoutSchema(Schema):
    
    id = fields.Int(dump_only=True)
    
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

    workout = fields.Nested("WorkoutSchema", dump_only=True)
    exercise = fields.Nested("ExerciseSchema", dump_only=True)



class WorkoutDetailSchema(WorkoutSchema):

    workout_exercises = fields.Nested("WorkoutExercisesSchema", many=True, dump_only=True)


class ExerciseDetailSchema(ExerciseSchema):

    workout_exercises = fields.Nested("WorkoutExercisesSchema", many=True, dump_only=True)
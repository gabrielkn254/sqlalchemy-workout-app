# Summative Lab: Flask SQLAlchemy Workout Application Backend

A comprehensive, backend RESTful API designed to manage physical workouts, track specific exercises, and log complex performance metrics (sets, reps, and durations) across workout sessions. Built entirely with Flask, Flask-SQLAlchemy, and Marshmallow.

This application implements a **Many-to-Many data model** where workouts and exercises are connected through a specialized association join table (`WorkoutExercises`). 

The architecture features structural data integrity at every step of execution:
* **API Entry/Schema Layer:** Handled via `Marshmallow` to filter incoming payloads, transform date formats, and throw explicit user validation exceptions (`ValidationError`).
* **Application/Model Layer:** Handled via Python decorators (`@validates`) to protect core business logic (e.g., preventing future-dated workouts and restricting exercise categories).
* **Database/Table Layer:** Handled via raw SQL constraints (`CheckConstraint` and `UniqueConstraint`) to lock down transactional integrity.


## Technologies Used
### Languages
- Python, Flask

### Package Manager
- Pipenv: Both managing packages and virtual env

### External dependacies
- mashmallow: serialization
- flask-migrate: DB migration
- flask-sqlalchemy: ORM

### Workflow 
- Git: code workflow managing tool
- Github: store remote repo


## Getting started
To run this program you will need to fork this repo, and install on your local machine.

### Installation & Setup Instructions

Follow these exact steps from the **root directory** of the repository to initialize your environment, create the database tables, and seed records.

1. Active and Install Dependencies
This project uses a local virtual environment configuration. Activate it and install dependencies:
```bash
# Activate your local virtual environment
source .venv/bin/activate

# Ensure your required packages are fully installed
pip install Flask Flask-SQLAlchemy Flask-Migrate marshmallow
```

2. Initialize and Synchronize the Database
Because the application configures a relative database path from inside a subdirectory, run your migration scripts directly from the command line while specifying the precise application path:
```bash
# Initialize the migration configuration folder structure
flask --app server/app.py db init

# Generate a clean migration script blueprint matching the models
flask --app server/app.py db migrate -m "initialize fitness tracking schema"

# Physically execute the structural schema changes onto disk (app.db)
flask --app server/app.py db upgrade
```

3. Seed the Target Database
Execute the population utility script from your root directory to clear past tables and inject a group of fresh records cleanly into your active database file:
```bash
python3 server/seed.py
```


### Run Instructions

Start the local development server by executing your main execution file:
```bash
python3 server/app.py
```
The server will bind to port **`5555`**. You can verify that your configuration is running smoothly by visiting `http://localhost:5555/workouts` in your browser or tool of choice (Postman, cURL, etc.).



## API Endpoints

### Workout Endpoints

1. `GET` `/workouts` 
Lists all logged workouts. Array of clean simple workout objects.

2. `GET` `/workouts/<id>`
Shows a single workout with deep details. Includes all related `WorkoutExercises` data (sets, reps, time).

3. `POST` `/workouts` 
Creates a new workout session record. Requires JSON containing `date`, `duration_minutes`, and `notes`.

4. `DELETE` `/workouts/<id>` 
Removes a specific workout from memory. Cascades down automatically to remove child logging relationships safely.


### Exercise Endpoints

1. `GET` `/exercises`
Lists all registered fitness movements. Array of simple exercise objects.

2. `GET` `/exercises/<id>`
Shows a detailed exercise log matrix. Includes history of every workout this item was linked to.

3. `POST` `/exercises`
Creates a new exercise in the master index. Requires `name` and an approved `category` string.

4. `DELETE` `/exercises/<id>` 
Removes an exercise from the index entirely. Sweeps matching relational traces out of the log system.


### Join Table / Association Endpoints

1. `POST` `/workouts/<w_id>/exercises/<ex_id>/workout_exercises`
Assigns an exercise entry straight to an active workout session. 
Requires JSON metrics: `{"reps": 10, "sets": 3, "duration_seconds": 0}`. |



## Active Validations Matrix

1. **Workout Date:** Cannot be set into a future day.
2. **Exercise Category:** Must belong strictly to the approved listing: `["Strength", "Cardio", "Flexibility", "Balance"]`.
3. **Logging Safety:** `reps` and `sets` parameters must be integers greater than zero.
4. **No Duplications:** The system blocks users from logging the exact same exercise item row multiple times into one identical workout instance object.



## Project Structure

```text
sqlalchemy-workout-app/
├── migrations/
├── server/
│   └── instance/
│   │   └── app.db
│   └── app.py
│   └── models.py
│   └── schemas.py
│   └── seed.py
├── .gitignore
├── LICENSE
├── Pipfile
├── Pipfile.lock
└── README.md

```

## License
This project is licensed under the MIT License.
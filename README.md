# TaskFlow

Web application for to-do lists built with Flask.

## Characteristics

- Add tasks (max. 200 characters)
- Delete tasks
- Thread-safe (safe management of concurrent tasks)
- Responsive interface with Tailwind CSS
- Unit tests included

## Project structure

```
taskflow/
├── ar.py              # Main Flask application
└── templates/
    └── index.html      # HTML Template
```

## Requirements

- Python 3.7+
- Flask

## facility

```bash
# Clone repository
git clone https://github.com/LeoBringasAtLife/task-flow.git
cd taskflow

# Create a virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install flask
```

## Use

### Run the server

```bash
python ar.py --run-server
```

The application will be available at `http://127.0.0.1:5000`

### Command line options

```bash
# Server on custom host/port
python ar.py --run-server --host 0.0.0.0 --port 8080

# Run unit tests
python ar.py --test
```

## Tests

The project includes unit tests that verify:

- Correct rendering of the homepage
- Adding valid tasks
- Validation of empty tasks
- Deletion of tasks
- Handling of invalid indexes

Run tests:

```bash
python ar.py --test
```

## Architecture

### TaskManager

Class that manages tasks with thread safety using `Lock`:

- `add_task(task)`: Adds a valid task
- `delete_task(index)`: Deletes a task by index
- `get_tasks()`: Returns a copy of the task list

### Flask Routes

- `GET /`: Main page with task list
- `POST /add`: Add new task
- `GET /delete/<index>`: Delete task by index

## Validations

- Tasks cannot be empty
- Maximum length: 200 characters
- Whitespace is automatically removed

<br>

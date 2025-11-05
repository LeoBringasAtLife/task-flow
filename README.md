# TaskFlow

Web application for to-do lists built with Flask.

## Características

- Add tasks (max. 200 characters)
- Delete tasks
- Thread-safe (safe management of concurrent tasks)
- Responsive interface with Tailwind CSS
- Unit tests included

## Project structure

```
taskflow/
├── app.py              # Main Flask application
└── templates/
    └── index.html      # HTML Template
```

## Requirements

- Python 3.7+
- Flask

## facility

```bash
# Clone repository
git clone <your-repository>
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
python app.py --run-server
```

The application will be available at `http://127.0.0.1:5000`

### Opciones de línea de comandos

```bash
# Servidor en host/puerto personalizado
python app.py --run-server --host 0.0.0.0 --port 8080

# Ejecutar tests unitarios
python app.py --test
```

## Tests

El proyecto incluye tests unitarios que verifican:

- Renderizado correcto de la página principal
- Agregar tareas válidas
- Validación de tareas vacías
- Eliminación de tareas
- Manejo de índices inválidos

Ejecutar tests:

```bash
python app.py --test
```

## Arquitectura

### TaskManager

Clase que gestiona las tareas con thread safety mediante `Lock`:

- `add_task(task)`: Agrega una tarea válida
- `delete_task(index)`: Elimina tarea por índice
- `get_tasks()`: Retorna copia de la lista de tareas

### Rutas Flask

- `GET /`: Página principal con lista de tareas
- `POST /add`: Agregar nueva tarea
- `GET /delete/<index>`: Eliminar tarea por índice

## Validaciones

- Tareas no pueden estar vacías
- Longitud máxima: 200 caracteres
- Espacios en blanco son eliminados automáticamente

## Licencia

MIT

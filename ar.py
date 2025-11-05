from flask import Flask, request, redirect, render_template, session
import argparse
import sys
import unittest
import os
from threading import Lock

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Necesario para sessions

# Storage mejorado con thread safety
class TaskManager:
    def __init__(self):
        self.tasks = []
        self.lock = Lock()
    
    def add_task(self, task):
        with self.lock:
            # Validación básica
            if task and len(task.strip()) > 0 and len(task) <= 200:
                self.tasks.append(task.strip())
                return True
        return False
    
    def delete_task(self, index):
        with self.lock:
            try:
                self.tasks.pop(index)
                return True
            except IndexError:
                return False
    
    def get_tasks(self):
        with self.lock:
            return self.tasks.copy()

task_manager = TaskManager()

# NOTA: Ya no necesitamos la variable HTML aquí

@app.route("/")
def home():
    return render_template('index.html', tasks=task_manager.get_tasks())

@app.route("/add", methods=["POST"])
def add():
    task = request.form.get("task", "").strip()
    if not task_manager.add_task(task):
        from flask import flash
        flash("La tarea no puede estar vacía o exceder 200 caracteres")
    return redirect("/")

@app.route("/delete/<int:index>")
def delete(index):
    if not task_manager.delete_task(index):
        from flask import flash
        flash("No se pudo eliminar la tarea")
    return redirect("/")


# Pruebas básicas (unit tests)

class TaskflowTestCase(unittest.TestCase):
    def setUp(self):
        # Limpia las tareas
        self.client = app.test_client()
        # Vaciar todas las tareas
        while task_manager.get_tasks():
            task_manager.delete_task(0)

    def test_home_status_and_empty(self):
        resp = self.client.get('/')
        self.assertEqual(resp.status_code, 200)
        self.assertIn(b'TaskFlow', resp.data)
        self.assertIn(b'No hay tareas', resp.data)

    def test_add_task(self):
        resp = self.client.post('/add', data={'task': 'Comprar leche'}, follow_redirects=True)
        self.assertEqual(resp.status_code, 200)
        self.assertIn(b'Comprar leche', resp.data)
        self.assertIn('Comprar leche', task_manager.get_tasks())

    def test_add_empty_task(self):
        resp = self.client.post('/add', data={'task': '   '}, follow_redirects=True)
        self.assertEqual(resp.status_code, 200)
        self.assertIn(b'No hay tareas', resp.data)

    def test_delete_task(self):
        task_manager.add_task('Tarea 1')
        task_manager.add_task('Tarea 2')
        resp = self.client.get('/delete/0', follow_redirects=True)
        self.assertEqual(resp.status_code, 200)
        self.assertNotIn(b'Tarea 1', resp.data)
        self.assertIn(b'Tarea 2', resp.data)

    def test_delete_invalid_index(self):
        resp = self.client.get('/delete/99', follow_redirects=True)
        self.assertEqual(resp.status_code, 200)

def main(argv=None):
    if argv is None:
        argv = sys.argv[1:]
        
    parser = argparse.ArgumentParser(description='Flujo de tareas')
    parser.add_argument('--run-server', action='store_true', help='Ejecutar el servidor Flask')
    parser.add_argument('--host', default='127.0.0.1', help='Host para el servidor')
    parser.add_argument('--port', type=int, default=5000, help='Puerto para el servidor')
    parser.add_argument('--test', action='store_true', help='Ejecutar tests unitarios y salir')
    args = parser.parse_args(argv)

    if args.test:
        suite = unittest.defaultTestLoader.loadTestsFromTestCase(TaskflowTestCase)
        runner = unittest.TextTestRunner(verbosity=2)
        result = runner.run(suite)
        sys.exit(0 if result.wasSuccessful() else 1)

    if args.run_server:
        app.run(host=args.host, port=args.port, debug=False, use_reloader=False)
    else:
        print("Nothing to do. Use --run-server to start the app or --test to run unit tests.")

if __name__ == '__main__':
    main()
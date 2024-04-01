'''Módulo utilizado para introdução ao Flask'''
import uuid
from flask import Flask, request, jsonify
from models.task import Task


app = Flask(__name__)

tasks = []


@app.route('/tasks', methods=['POST'])
def create_task():
    data = request.get_json()
    new_task = Task(id=uuid.uuid4(), title=data['title'], description=data.get('description',''))
    tasks.append(new_task)
    return jsonify({"message": "Nova tarefa criada com sucesso"})


@app.route('/tasks', methods=['GET'])
def get_tasks():
    task_list = [task.to_dict() for task in tasks]
    output = {
        "tasks": task_list,
        "total_tasks": len(task_list)
    }
    return jsonify(output)


@app.route('/tasks/<uuid:id>', methods=['GET'])
def get_task(id):
    for task in tasks:
        if task.id == id:
            return jsonify(task.to_dict())
    return jsonify({"message": "Não foi possível encontrar a tarefa"}), 404


app.run(debug=True)

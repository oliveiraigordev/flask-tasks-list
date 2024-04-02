'''Módulo utilizado para estudos de introdução ao Flask'''
import uuid
from flask import Flask, request, jsonify
from models.task import Task


app = Flask(__name__)

tasks = []


@app.route('/tasks', methods=['POST'])
def create_task():
    data = request.get_json()
    new_task = Task(
        id=uuid.uuid4(),
        title=data['title'],
        description=data.get('description', ''))
    tasks.append(new_task)
    return jsonify(
        {"message": "Nova tarefa criada com sucesso!",
         "id": new_task.id}
        )
    

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
    for t in tasks:
        if t.id == id:
            return jsonify(t.to_dict())
    return jsonify({"message": "Não foi possível encontrar a tarefa."}), 404


@app.route('/tasks/<uuid:id>', methods=['PUT'])
def update_task(id):
    task = None
    for t in tasks:
        if t.id == id:
            task = t
            break
    if task is None:
        return jsonify(
            {"message": "Não foi possível encontrar a tarefa."}
            ), 404

    data = request.get_json()
    task.title = data['title']
    task.description = data['description']
    task.completed = data['completed']
    return jsonify({"message": "Tarefa atualizada com sucesso!"})


@app.route('/tasks/<uuid:id>', methods=['DELETE'])
def delete_task(id):
    task = None
    for t in tasks:
        if t.id == id:
            task = t
            break
    if task is None:
        return jsonify(
            {"message": "Não foi possível encontrar a tarefa."}
            ), 404

    tasks.remove(task)
    return jsonify({"message": "Tarefa apagada com sucesso!"})


app.run(debug=True)

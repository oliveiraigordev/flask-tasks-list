'''Testes automatizados'''
import requests


BASE_URL = 'http://127.0.0.1:5000'

tasks = []


def test_create_task():
    new_task_data = {
        "title": "Nova tarefa",
        "description": "Descição da nova tarefa"
    }
    response = requests.post(
        f'{BASE_URL}/tasks', json=new_task_data, timeout=120
        )
    assert response.status_code == 200
    assert "message" in response.json()
    assert "id" in response.json()
    tasks.append(response.json()['id'])


def test_read_tasks():
    response = requests.get(
        f'{BASE_URL}/tasks', timeout=120
        )
    assert response.status_code == 200
    assert "tasks" in response.json()
    assert "total_tasks" in response.json()


def test_get_task():
    if tasks:
        task_id = tasks[0]
        response = requests.get(
            f'{BASE_URL}/tasks/{task_id}', timeout=120
            )
        assert response.status_code == 200
        assert response.json()['id'] == task_id


def test_update_task():
    if tasks:
        task_id = tasks[0]
        payload = {
            "completed": False,
            "description": "Nova descrição",
            "title": "Novo título"
        }
        response = requests.put(
            f'{BASE_URL}/tasks/{task_id}', json=payload, timeout=120
            )
        assert response.status_code == 200
        assert "message" in response.json()

        response = requests.get(
            f'{BASE_URL}/tasks/{task_id}', timeout=120
            )
        assert response.status_code == 200
        assert response.json()['title'] == payload['title']
        assert response.json()['description'] == payload['description']
        assert response.json()['completed'] == payload['completed']


def test_delete_task():
    if tasks:
        task_id = tasks[0]
        response = requests.delete(
            f'{BASE_URL}/tasks/{task_id}', timeout=120
            )
        assert response.status_code == 200

        response = requests.get(
            f'{BASE_URL}/tasks/{task_id}', timeout=120
            )
        assert response.status_code == 404

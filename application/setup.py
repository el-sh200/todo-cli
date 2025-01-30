from application.todo.todo_service import TodoService
from application.assignee.assignee_service import AssigneeService
from infrastructure.json.assignee_storage import init_assignee
from infrastructure.json.todo_storage import init_todo


def setup(_type='json'):
    init_todo()
    init_assignee()
    todo_service = TodoService()
    assignee_service = AssigneeService()
    return todo_service, assignee_service

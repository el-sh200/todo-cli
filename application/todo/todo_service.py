from application.assignee.assignee_interface import AssigneeCrud
from application.todo.todo_interface import TodoCrud
from domain.todo import Todo


class TodoService(TodoCrud):
    def add_todo(self, title, assignee_name):
        error = self.validate_todo(title, assignee_name)
        if not error:
            new_todo = Todo(title, assignee_name)
            self.append(new_todo)
        return error

    def list_todo(self):
        return self.load()

    def get_todo(self, title):
        todos, error = self.load()
        obj = self.get(todos, 'title', title)
        if obj:
            return obj, None
        return None, 'Task not found'

    def complete_todo(self, todo):
        todo['completed'] = True
        return self.update(todo)

    def edit_todo(self, todo, updates):
        error = self.validate_todo(assignee_name=updates.get('new_assignee'))
        if not error:
            if updates.get('new_assignee', False):
                todo['assignee_name'] = updates['new_assignee']
            return self.update(todo)
        return None, error

    def delete_todo(self, title):
        return self.delete('title', title)

    def validate_todo(self, title=None, assignee_name=None):
        assignee_crud = AssigneeCrud()
        assignees, error = assignee_crud.load()
        todos, error = self.load()

        # Duplicate title
        if title and self.get(todos, 'title', title):
            error = 'Duplicate title'

        # valid assignee
        if assignee_name and not self.get(assignees, 'name', assignee_name):
            error = 'no such assignee'
        return error

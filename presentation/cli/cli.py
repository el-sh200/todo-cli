import click


class ClickCLI:
    def __init__(self, todo_service, assignee_service):
        self.todo_service = todo_service
        self.assignee_service = assignee_service

    def start(self):
        """Start the CLI."""

        @click.group()
        def cli():
            """A simple Todo CLI application."""
            pass

        @cli.command()
        @click.option("--title", "-t", prompt="Enter title", help="The title of the todo.")
        @click.option("--assignee", "-a", prompt="Enter assignee name", help="The assignee of the todo.")
        def add_task(title: str, assignee: str):
            """Add a new task."""
            error = self.todo_service.add_todo(title, assignee)
            if not error:
                message_wrapper("Todo added successfully!")
            else:
                message_wrapper(error, 'danger')

        def message_wrapper(msg, level='success'):
            FG_COLORS = {
                'success': 'green',
                'danger': 'red',
                'info': 'blue',
            }
            click.secho(msg, fg=FG_COLORS[level])

        @cli.command()
        def list_tasks():
            """List all tasks."""
            todos, error = self.todo_service.list_todo()
            if not error:
                for todo in todos:
                    status = "Completed" if todo['completed'] else "Pending"
                    message_wrapper(f"{todo['title']} - {todo['assignee_name']} [{status}]", level='info')
            else:
                message_wrapper(error, 'danger')

        @cli.command()
        @click.option("--title", "-t", prompt="Enter title", help="The title of the todo.")
        @click.option("--completed", "-com", type=bool)
        def show_task(title, completed):
            """Show task."""
            todo, error = self.todo_service.get_todo(title)
            if not error and completed:
                todo, error = self.todo_service.complete_todo(todo)
            if not error:
                status = "Completed" if todo['completed'] else "Pending"
                message_wrapper(f"{todo['title']} - {todo['assignee_name']} [{status}]", level='info')
            else:
                message_wrapper(error, 'danger')

        @cli.command()
        @click.option("--title", "-t", prompt="Enter title", help="The title of the todo.")
        def delete_task(title):
            """Delete task."""
            error = self.todo_service.delete_todo(title)
            if not error:
                message_wrapper("Task deleted successfully!")
            else:
                message_wrapper(error, 'danger')

        @cli.command()
        @click.option("--title", "-t", prompt="Enter title", help="The title of the todo.")
        @click.option("--new_assignee", "-na", default=None, help="The assignee of the todo.")
        def edit_task(title, new_assignee):
            """Edit task."""
            todo, error = self.todo_service.get_todo(title)
            if error:
                message_wrapper(error, 'danger')
            else:
                updates = {'new_assignee': new_assignee}
                todo, error = self.todo_service.edit_todo(todo, updates)
                if error:
                    message_wrapper(error, 'danger')
                else:
                    message_wrapper('Todo edited successfully!')

        @cli.command()
        @click.option("--name", "-n", prompt="Enter name", help="The person name.")
        @click.option("--email", "-e", prompt="Enter assignee email", help="The person email.")
        def add_person(name: str, email: str):
            """Add a new assignee."""
            error = self.assignee_service.add_assignee(name, email)
            if not error:
                message_wrapper("Person added successfully!")
            else:
                message_wrapper(error, 'danger')

        @cli.command()
        def list_person():
            """List all persons."""
            persons, error = self.assignee_service.list_person()
            if not error:
                for person in persons:
                    message_wrapper(f"{person['name']} - {person['email']}", level='info')
            else:
                message_wrapper(error, 'danger')

        @cli.command()
        @click.option("--name", "-n", prompt="Enter name", help="The name of the person.")
        def delete_person(name):
            """Delete perosn."""
            deleted = self.assignee_service.delete_person(name)
            if deleted:
                message_wrapper("Person deleted successfully!")
            else:
                message_wrapper('No person found', 'danger')

        @cli.command()
        @click.option("--name", "-n", prompt="Enter name", help="The name of the person.")
        @click.option("--new_email", "-ne", default=None, help="The new email.")
        def edit_person(name, new_email):
            """Edit person."""
            person, error = self.assignee_service.get_person(name)
            if error:
                message_wrapper(error, 'danger')
            else:
                updates = {'new_email': new_email}
                person, error = self.assignee_service.edit_person(person, updates)
                if error:
                    message_wrapper(error, 'danger')
                else:
                    message_wrapper('Person edited successfully!')

        cli()

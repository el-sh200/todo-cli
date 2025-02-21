import flet as ft


class Task(ft.Column):
    def __init__(self, obj, task_service, assignee_service, show_message, task_delete):
        super().__init__()
        self.obj = obj
        self.task_name = obj['title']
        self.assignee_name = obj['assignee_name']
        self.completed = obj['completed']
        self.task_service = task_service
        self.assignee_service = assignee_service
        self.show_message = show_message
        self.task_delete = task_delete

        self.edit_assignee_dropdown = ft.Dropdown(
            hint_text="Select Assignee",
            options=[],
            value=self.assignee_name,
            expand=True,
        )

        self.display_task = ft.Checkbox(
            value=self.completed, label=self.task_name,
            on_change=self.status_changed
        )

        self.assignee_chip = ft.Chip(
            label=ft.Text(self.assignee_name),
            bgcolor=ft.colors.BLUE_100 if self.assignee_name is not None else ft.colors.BLACK,
            disabled_color=ft.colors.BLUE_100,
            check_color=ft.colors.BLUE_100,
            shape=ft.RoundedRectangleBorder(radius=10),
        )

        self.edit_name = ft.TextField(expand=1)
        self.edit_assignee = ft.TextField(
            hint_text="Assignee name",
            value=self.assignee_name,
            expand=True,
        )
        self.display_view = ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Row(
                    controls=[self.display_task, self.assignee_chip],
                    spacing=10,
                ),
                ft.Row(
                    spacing=0,
                    controls=[
                        ft.IconButton(
                            icon=ft.icons.CREATE_OUTLINED,
                            tooltip="Edit To-Do",
                            on_click=self.edit_clicked,
                        ),
                        ft.IconButton(
                            ft.icons.DELETE_OUTLINE,
                            tooltip="Delete To-Do",
                            on_click=self.delete_clicked,
                        ),
                    ],
                ),
            ],
        )

        self.edit_view = ft.Row(
            visible=False,
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                self.edit_assignee_dropdown,
                ft.IconButton(
                    icon=ft.icons.DONE_OUTLINE_OUTLINED,
                    icon_color=ft.colors.GREEN,
                    tooltip="Update Assignee",
                    on_click=self.save_clicked,
                ),
            ],
        )
        self.controls = [self.display_view, self.edit_view]

    def did_mount(self):
        self.load_assignees()

    def load_assignees(self):
        assignees, error = self.assignee_service.list_person()
        if error:
            self.show_message(f"Error loading assignees: {error}")
            return

        self.edit_assignee_dropdown.options = [
            ft.dropdown.Option(assignee["name"]) for assignee in assignees
        ]
        self.update()

    def edit_clicked(self, e):
        self.edit_assignee_dropdown.value = self.assignee_name
        self.display_view.visible = False
        self.edit_view.visible = True
        self.update()

    def save_clicked(self, e):
        new_assignee = self.edit_assignee_dropdown.value or None
        data, error = self.task_service.edit_todo(self.obj, updates={'new_assignee': new_assignee})
        if not error:
            self.assignee_name = data['assignee_name']
            self.assignee_chip.label = ft.Text(self.assignee_name)
            self.assignee_chip.bgcolor = ft.colors.BLUE_100 if self.assignee_name is not None else ft.colors.BLACK
            self.show_message(f'Task {self.task_name} assigned to {self.assignee_name}', level='success')
            self.display_view.visible = True
            self.edit_view.visible = False
        else:
            self.show_message(error)
        self.update()

    def task_status_change(self):
        self.task_service.complete_todo(self.obj, completed=self.completed)
        self.update()

    def status_changed(self, e):
        self.completed = self.display_task.value
        self.task_status_change()

    def delete_clicked(self, e):
        self.task_delete(self)


class TodoApp(ft.Column):
    def __init__(self, task_service, assignee_service):
        super().__init__()
        self.task_service = task_service
        self.assignee_service = assignee_service

        self.new_assignee_name = ft.TextField(hint_text="Enter assignee name", expand=True)
        self.new_assignee_email = ft.TextField(hint_text="Enter assignee email", expand=True)
        self.add_assignee_dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Add New Assignee"),
            content=ft.Column(
                controls=[self.new_assignee_name, self.new_assignee_email],
                tight=True,
            ),
            actions=[
                ft.TextButton("Add", on_click=self.add_assignee),
                ft.TextButton("Cancel", on_click=self.close_assignee_dialog),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )

        self.add_assignee_button = ft.IconButton(
            icon=ft.icons.PERSON_ADD,
            tooltip="Add New Assignee",
            on_click=lambda e: self.page.open(self.add_assignee_dialog),
        )

        self.assignee_dropdown = ft.Dropdown(
            hint_text="Select Assignee",
            options=[],
            expand=True,
        )

        self.new_task = ft.TextField(
            hint_text="What needs to be done?", on_submit=self.add_clicked, expand=True
        )

        self.error_banner = ft.Container(
            content=ft.Text("", color=ft.colors.WHITE),
            bgcolor=ft.colors.RED_400,
            padding=10,
            border_radius=10,
            visible=False,
            alignment=ft.alignment.center,
        )

        self.tasks = ft.Column()

        self.load_tasks()

        self.filter = ft.Tabs(
            scrollable=False,
            selected_index=0,
            on_change=self.tabs_changed,
            tabs=[ft.Tab(text="all"), ft.Tab(text="active"), ft.Tab(text="completed")],
        )

        self.items_left = ft.Text("0 items left")

        self.width = 600
        self.controls = [
            ft.Row(
                [ft.Text(value="Todos", theme_style=ft.TextThemeStyle.HEADLINE_MEDIUM)],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            ft.Row(
                controls=[
                    self.new_task,
                    self.assignee_dropdown,
                    self.add_assignee_button,
                    ft.FloatingActionButton(
                        icon=ft.icons.ADD, on_click=self.add_clicked
                    ),
                ],
            ),
            self.error_banner,
            ft.Column(
                spacing=25,
                controls=[
                    self.filter,
                    self.tasks,
                    ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                        controls=[
                            self.items_left,
                            ft.OutlinedButton(
                                text="Clear completed", on_click=self.clear_clicked
                            ),
                        ],
                    ),
                ],
            ),
        ]

    def did_mount(self):
        self.load_assignees()

    def load_assignees(self):
        assignees, error = self.assignee_service.list_person()
        if error:
            self.show_message(f"Error loading assignees: {error}")
            return

        self.assignee_dropdown.options = [
            ft.dropdown.Option(assignee["name"]) for assignee in assignees
        ]
        self.update()

    def open_assignee_dialog(self, e):
        self.new_assignee_name.value = ""
        self.new_assignee_email.value = ""
        self.add_assignee_dialog.open = True
        self.update()

    def close_assignee_dialog(self, e):
        self.page.close(self.add_assignee_dialog)
        self.update()

    def add_assignee(self, e):
        new_assignee_name = self.new_assignee_name.value.strip()
        new_assignee_email = self.new_assignee_email.value.strip()
        if new_assignee_name and new_assignee_email:
            error = self.assignee_service.add_assignee(new_assignee_name, new_assignee_email)
            if not error:
                self.show_message(f'Assignee {new_assignee_name} added', level='success')
                self.load_assignees()
                self.close_assignee_dialog()
            else:
                self.show_message(error)
        else:
            self.show_message("Assignee name cannot be empty")

    def show_message(self, message, level='danger'):
        self.error_banner.content.value = message
        if level == 'success':
            self.error_banner.bgcolor = ft.colors.GREEN_400
        else:
            self.error_banner.bgcolor = ft.colors.RED_400
        self.error_banner.visible = True
        self.update()

    def load_tasks(self):
        tasks_data, error = self.task_service.list_todo()
        if error:
            self.show_message(f"Error loading tasks: {error}")
            return

        self.tasks.controls.clear()

        for task_data in tasks_data:
            task = Task(
                obj=task_data,
                task_delete=self.task_delete,
                task_service=self.task_service,
                assignee_service=self.assignee_service,
                show_message=self.show_message,
            )
            task.completed = task_data.get("completed")
            self.tasks.controls.append(task)

    def add_clicked(self, e):
        if self.new_task.value:
            assignee_name = self.assignee_dropdown.value or None

            task_data = {"title": self.new_task.value, "assignee_name": assignee_name}
            error = self.task_service.add_todo(**task_data)
            if not error:
                self.show_message(f'Task {self.new_task.value} added', level='success')
                self.load_tasks()
                self.new_task.value = ""
                self.assignee_dropdown.value = None
                self.new_task.focus()
                self.update()
            else:
                self.show_message(error)

    def task_delete(self, task):
        is_deleted = self.task_service.delete_todo(task.task_name)
        if is_deleted:
            self.show_message('Task deleted successfully', level='success')
        else:
            self.show_message('Failed to delete task')
        self.load_tasks()
        self.update()

    def tabs_changed(self, e):
        self.update()

    def clear_clicked(self, e):
        for task in self.tasks.controls[:]:
            if task.completed:
                self.task_delete(task)

    def before_update(self):
        status = self.filter.tabs[self.filter.selected_index].text
        count = 0
        for task in self.tasks.controls:
            task.visible = (
                    status == "all"
                    or (status == "active" and task.completed == False)
                    or (status == "completed" and task.completed)
            )
            if not task.completed:
                count += 1
        self.items_left.value = f"{count} active item(s) left"


def main(page: ft.Page, task_service, assignee_service):
    page.title = "Todo App"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.scroll = ft.ScrollMode.ADAPTIVE

    todo_app = TodoApp(task_service, assignee_service)

    page.add(todo_app)


def build(task_service, assignee_service):
    ft.app(target=lambda page: main(page, task_service, assignee_service))

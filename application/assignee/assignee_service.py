import re

from application.assignee.assignee_interface import AssigneeInterface
from domain.assignee import Assignee


class AssigneeService(AssigneeInterface):
    def add_assignee(self, name, email):
        error = self.validate_assignee(name, email)
        if not error:
            new_assignee = Assignee(name, email)
            self.append(new_assignee)
        return error

    def validate_assignee(self, name, email):
        assignees, error = self.load()

        # Invalid email
        if not self.validate_email(email):
            error = 'Email invalid'

        # Duplicate title
        if self.get(assignees, 'name', name):
            error = 'Duplicate name'

        return error

    def validate_email(self, email):
        """
        Validates the email format.
        """
        pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        return re.match(pattern, email) is not None

    def list_person(self):
        return self.load()

    def delete_person(self, name):
        return self.delete('name', name)

    def get_person(self, name):
        persons, error = self.load()
        obj = self.get(persons, 'name', name)
        if obj:
            return obj, None
        return None, 'Person not found'

    def edit_person(self, perosn, updates):
        if updates.get('new_email'):
            is_valid = self.validate_email(updates.get('new_email'))
            if is_valid:
                perosn['email'] = updates['new_email']
                return self.update(perosn)
            return None, 'Email not valid'
        return None, None

from dataclasses import dataclass, asdict
from datetime import datetime


@dataclass
class Todo:
    title: str
    assignee_name: str
    completed: bool = False
    created_at: datetime = datetime.now()

    def to_dict(self):
        data = asdict(self)
        data['created_at'] = self.created_at.isoformat()
        return data


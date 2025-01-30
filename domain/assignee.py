from dataclasses import dataclass, asdict
from datetime import datetime


@dataclass
class Assignee:
    name: str
    email: str
    created_at: datetime = datetime.now()

    def to_dict(self):
        data = asdict(self)
        data['created_at'] = self.created_at.isoformat()
        return data

from dataclasses import dataclass
from datetime import datetime

@dataclass
class Task:
    id: int=1
    task_name: str = ""
    start_time: datetime = datetime.now()
    end_time: datetime = datetime.now()
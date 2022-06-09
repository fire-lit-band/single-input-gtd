import UI
from dataclasses import dataclass
from datetime import date, time,datetime

@dataclass
class Task:
    id:int
    task_name: str
    start_time: datetime
    end_time: datetime


def main(command):
    if command.isdigit():
        pass
    if command=='q':
        pass
    elif command=='ok':
        pass
    elif command=='p':
        pass
    elif command=="!":
        pass
    elif command=='~':
        pass





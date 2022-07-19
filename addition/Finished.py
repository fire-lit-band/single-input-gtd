from dataclasses import dataclass
from datetime import datetime

@dataclass
class Finished:
    name: str
    subname: str
    actuall_start_time: datetime
    actuall_end_time: datetime
    actlength: int
    actshift: int
    reason: str

    def format(self):
        return tuple(vars(self).values())

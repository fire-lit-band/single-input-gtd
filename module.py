import pandas as pd

import UI
from dataclasses import dataclass
from datetime import date, time,datetime
import pandas as pd
import read_todo

@dataclass
class Task:
    id:int
    task_name: str
    start_time: datetime
    end_time: datetime

@dataclass
class Finished:
    name:str
    subname:str
    actuall_start_time:datetime
    actlength:int
    actshift:int
    reason:str

def main(command):
    data=read_todo.display_todo("todo.csv")
    if len(data)==0:
        print("当前没有数据，请添加数据")
        return False
    if command.isdigit():
        if 0<=int(command)<=len(data):
            pass
        else:
            print("输入错误")
            return pass
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





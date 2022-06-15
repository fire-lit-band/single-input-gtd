import pandas as pd
import to_todo
import UI
from dataclasses import dataclass
from datetime import  time,datetime
import pandas as pd
import read_todo
import to_todo

@dataclass
class Task:
    id:int
    task_name: str= ''
    start_time: datetime=datetime.now()
    end_time: datetime=datetime.now()

@dataclass
class Finished:
    name:str
    subname:str
    actuall_start_time:datetime
    actuall_end_time:datetime
    actlength:int
    actshift:int
    reason:str
    def format(self):
        return (self.name,self.subname,self.actuall_start_time,self.actuall_end_time,self.actlength,self.actshift,self.reason)

current_task=Task

def pause_task(current_task,command):
    if current_task.task_name == '':
        print("当前没有任务")
    else:
        current_task.end_time = datetime.now()

        if command=="!":
            current_task= end_task(current_task,'紧急事情')
            current_task.task_name=input("请输入当前的紧急事项")
            current_task=begin_task(current_task,current_task.task_name)
        elif command=='~':
            current_task = end_task(current_task,'休息')
        elif command=='p':
            current_task = end_task(current_task, '休息')
            current_task.task_name = ''
    return current_task

def finished_task(current_task,command):
    if current_task.task_name == '':
        if command=='ok':
            print("当前没有任务")
    else:
        current_task.end_time = datetime.now()
        current_task= end_task(current_task,'finished')
        current_task.task_name = ''
    return current_task

def begin_task(current_task,task_name):
    current_task.task_name=task_name
    print(f"开始执行: {current_task.task_name}")
    current_task.start_time = datetime.now()
    return current_task

def end_task(current_tasks,reason):
    current_tasks.end_time=datetime.now()
    subname=input("请输入你完成的内容")
    record=Finished(current_tasks.task_name,subname,current_tasks.start_time,current_tasks.end_time,0,0,reason)
    to_todo.add_record(record)
    return current_tasks

def main(command):
    global current_task
    data=read_todo.today_todo()
    if len(data)==0:
        print("当前没有数据，请添加数据")
        return "end"
    if command.isdigit():
        if current_task.task_name!='':
            print("当前有任务")
        if 0<=int(command)<=len(data)-1:
            num=int(command)
            current_task=begin_task(current_task,data.loc[num])
        else:
            print("输入错误")
        return "doing"
    if command=='q':
        current_task=finished_task(current_task,command)
        return "end"
    elif command=='ok':
        current_task=finished_task(current_task,command)
        return "done"
    elif command=='p':
        current_task=pause_task(current_task, command)
        return "done"
    elif command=="!":
        current_task=pause_task(current_task,command)
        return "done"
    elif command=='~':
        current_task=pause_task(current_task, command)
        return "done"
    elif command==' ':
        return "done"
    else:
        print("输入错误")
        return True





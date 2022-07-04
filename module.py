
from datetime import datetime, time
from Finished import Finished
from Task import Task
import pandas as pd


import read_todo
import to_todo




def pause_task(current_task: Task, command: str):
    if current_task.task_name == "":
        print("当前没有任务")
    else:
        current_task.end_time = datetime.now()

        if command == "!":
            current_task = end_task(current_task, "紧急事情")
            current_task.task_name = input("请输入当前的紧急事项")
            current_task = begin_task(current_task, current_task.task_name)
        elif command == "~":
            current_task = end_task(current_task, "休息")
        elif command == "p":
            current_task = end_task(current_task, "休息")
            current_task.task_name = ""
    return current_task


def finished_task(current_task: Task, command: str):
    if current_task.task_name == "":
        if command == "ok":
            print("当前没有任务")
    else:
        current_task.end_time = datetime.now()
        current_task = end_task(current_task, "finished")
        current_task.task_name = ""
    return current_task


def begin_task(current_task: Task, task_name: str):
    current_task.task_name = task_name
    print(f"开始执行: {current_task.task_name}")
    current_task.start_time = datetime.now()
    return current_task


def end_task(current_tasks: Task, reason: str):
    current_tasks.end_time = datetime.now()
    subname = input("请输入你完成的内容")
    record = Finished(
        name=current_tasks.task_name,
        subname=subname,
        actuall_start_time=current_tasks.start_time,
        actuall_end_time=current_tasks.end_time,
        actlength=0,
        actshift=0,
        reason=reason,
    )
    to_todo.add_record(record)
    return current_tasks


def main(command: str,current_task:Task):

    data=pd.read_csv("todo.csv")
    if len(data) == 0:
        print("当前没有数据，请添加数据")
        return "end",current_task
    if command.isdigit():
        if current_task.task_name != "":
            print("当前有任务")
        elif 0 <= int(command) <= len(data) - 1:
            num = int(command)
            current_task = begin_task(current_task, data.loc[num])
        else:
            print("输入错误")
        return "doing",current_task
    if command ==" ": # 这个是用来刷新内容的
        return "done",current_task
    elif command == "ok":
        to_todo.delete_todo(current_task.task_name)
        current_task = finished_task(current_task, command)
        return "done",current_task
    elif command in {"p", "!", "~"}:
        current_task = pause_task(current_task, command)
        return "done",current_task
    elif command == "q":
        to_todo.delete_todo(current_task.task_name)
        current_task = finished_task(current_task, command)
        return "end",current_task
    else:
        print("输入错误")
        return True,current_task

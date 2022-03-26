import os
import time
from dataclasses import dataclass
from datetime import date, datetime
from pathlib import Path
from typing import List, Union

import pandas as pd

FilePath = Union[str, bytes, os.PathLike]

TodoList = List[str]
PATH = Path(__file__).parent.absolute()

FILE_NAME = PATH / "plan.md"
ddl_name = PATH / "ddl.csv"

TODO_PREFIX = "- [ ] "

HINT = '输入任务标号以开始对应任务，输入 "ok" 以结束任务： '

orignal: List[str] = []


@dataclass
class Record:
    task_name: str
    start_time: datetime
    end_time: datetime


@dataclass
class Read_from_file:
    """用三元组分别记录todo_list,源文件的开头和源文件的结尾"""

    task_names: List[str]
    start_index: int
    end_index: int


def process(keyword: str):
    global orignal
    start = orignal.index(keyword)
    start += 2
    end = start
    while "##" not in orignal[end]:
        end += 1
    end -= 2
    # start 存list的开头在源文件的位置
    # end 存list结尾在源文件的位置
    text_position = slice(6, None)
    return Read_from_file(
        task_names=[i[text_position] for i in orignal[start:end]],
        start_index=start,
        end_index=end,
    )  # '- [ ]'代表todo列表


def read_todos():
    global orignal
    with open(FILE_NAME, encoding="utf-8") as f:
        orignal = f.readlines()
    todo_list = process("## to do\n")
    return todo_list


def save_todos(listrecord: Read_from_file, current_task: str):
    # 更改原文件里面的todolist
    global orignal
    todolist = listrecord.task_names
    start = listrecord.start_index
    end = listrecord.end_index
    todolist = [i.removesuffix("\n") for i in todolist]
    # print(todolist)
    current_task = current_task.removesuffix("\n")
    # print(current_task)
    print(f"{todolist = }, {current_task = }")
    todolist.remove(current_task)
    # print(orignal[:start + 2])
    # print(orignal[end:])
    orignal = (
        orignal[:start]
        + ["- [ ] " + i + "\n" for i in todolist]
        + orignal[end:]
    )
    with open("plan.md", "w", encoding="utf-8") as f:
        for i in orignal:
            print(i, file=f, end="")


def save_record(Record: Record):
    a = Record.task_name
    b = Record.start_time
    c = Record.end_time
    d=c-b
    return a[:-1] + "," + b.strftime("%X") + "," + c.strftime("%X") +','+str(d)+"\n"


def print_todos(todo_list: TodoList):
    todo_list = [i[:-1] for i in todo_list]
    for i, todo in enumerate(todo_list):
        print(f"{i}. {todo}")


def print_and_return_ddl(keyword: FilePath, ifinitial: bool = True):
    ddl = pd.read_csv(keyword)  # type: ignore
    if ifinitial:
        length = len(ddl.index)
        minus = [
            date(
                ddl.iloc[i].year, ddl.iloc[i].month, ddl.iloc[i].day
            ).toordinal()
            - date.today().toordinal()
            for i in range(length)
        ]
        sorted_id = sorted(range(len(minus)), key=lambda k: minus[k])
        for i in range(len(minus)):
            if minus[sorted_id[i]] > 0:
                print(
                    ddl.project.iloc[i], "还剩下：", str(minus[sorted_id[i]]), "天"
                )
            elif minus[sorted_id[i]] == 0:
                print(ddl.project.iloc[i], "是今天")
            else:
                pass
    else:
        for i, dd in enumerate(ddl.project):
            print(f"{i}. {dd}")
        return ddl.project


def save_new_ddl(keyword: FilePath, current: str):
    ddl = pd.read_csv(keyword)  # type: ignore
    ddl.drop(current)
    ddl.to_csv(keyword)


def main():
    todo_listrecord: Read_from_file = read_todos()
    todo_list = todo_listrecord.task_names
    task_finished: List[Record] = []
    current_task = ""
    start_time = None
    is_ddl = False

    print_todos(todo_list)
    print_and_return_ddl(ddl_name)

    while True:
        if len(todo_list) == 0:
            print("没任务了，块点添加吧")
            break
        command = input(HINT)
        if command.isdigit():
            if current_task:
                print(f"正在执行{current_task}")
                continue
            num = int(command)
            if 0 <= num <= len(todo_list) - 1:
                current_task = todo_list[num]
                print(f"开始执行: {current_task[:-1]}")
                start_time = datetime.now()
            else:
                print("任务不在列表里")
        elif command == "ok":
            if not current_task:
                print("没有任务在执行")
                continue
            if start_time is not None:
                end_time = datetime.now()
                task_finished.append(Record(current_task, start_time, end_time))
                save_todos(todo_listrecord, current_task)
                todo_list.remove(current_task)
                print(f"完成任务: {current_task}, 用时{(end_time - start_time)}")
                if is_ddl:
                    save_new_ddl(ddl_name, current_task)
                    is_ddl = False
                current_task = ""
                print_todos(todo_list)
                print_and_return_ddl(ddl_name)
        elif command == "q":
            if not current_task:
                print("没有任务在执行")
                break
            end_time = datetime.now()
            if start_time is not None:
                task_finished.append(Record(current_task, start_time, end_time))
                save_todos(todo_listrecord, current_task)
                print(f"完成任务: {current_task}, 用时{(end_time - start_time)}")
                break
        elif command == "b":
            if current_task:
                print(f"撤回成功")
                current_task = ""
            else:
                print(f"当前无任务，请重新输入")
        elif command == "due":
            ddllist: List = print_and_return_ddl(ddl_name, False)  # type: ignore
            command = input("选择你要进行的ddl")
            is_ddl = True

            if command.isdigit():
                num = int(command)
                if 0 <= num <= len(ddllist) - 1:
                    todo_list.append(ddllist[num])
                    current_task = ddllist[num]
                    print(f"开始执行: {current_task}")
                    start_time = datetime.now()
                else:
                    print("任务不在列表里")
            else:
                print("无效指令")
        elif command == "wait":
            if not current_task:
                print("没有任务在执行")
                continue
            end_time = datetime.now()
            if start_time is not None:
                task_finished.append(Record(current_task, start_time, end_time))
                todo_list.remove(current_task)
                print(f"暂时用时: {current_task}, 用时{(end_time - start_time)}")
                is_ddl = False
                current_task = ""
                print_todos(todo_list)
                print_and_return_ddl(ddl_name)
        else:
            print("无效指令")
    newtime = time.localtime(time.time())
    recording = f"{newtime[1]}.{newtime[2]}"
    with open(str(recording) + ".csv", "a") as record:
        for i in task_finished:
            record.write(save_record(i))


if __name__ == "__main__":
    main()

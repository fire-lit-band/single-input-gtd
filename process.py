import re
import time
from dataclasses import dataclass
from datetime import date
from datetime import datetime
import pandas
import pandas as pd

FILE_NAME = 'plan.md'
ddl_name = 'ddl.csv'

TODO_PREFIX = '- [ ] '

HINT = '输入任务标号以开始对应任务，输入 "ok" 以结束任务： '

orignal = []


@dataclass
class Record:
    task_name: str
    start_time: datetime
    end_time: datetime


def process(keyword):
    global orignal
    start = orignal.index(keyword)
    start = start + 2
    end = start
    while '##' not in orignal[end]:
        end = end + 1
    end = end - 2
    # start 存list的开头在源文件的位置
    # end 存list结尾在源文件的位置
    return [[i[6:] for i in orignal[start:end]], start, end]  # '- [ ]'代表todo列表


def read_todos():
    global orignal
    with open(FILE_NAME, encoding='utf-8') as f:
        orignal = f.readlines()
    todo_list = process('## to do\n')
    return todo_list


def save_todos(listrecord, current_task):
    # 讲原文件里面的todolist进行更改
    global orignal
    todolist = listrecord[0]
    start = listrecord[1]
    end = listrecord[2]
    todolist = [i[:-1] for i in todolist]
    # print(todolist)
    current_task = current_task[0:-1]
    # print(current_task)
    todolist.remove(current_task)
    # print(orignal[:start + 2])
    # print(orignal[end:])
    orignal = orignal[:start] + ['- [ ] ' + i + '\n' for i in todolist] + orignal[end:]
    with open('plan.md', 'w', encoding='utf-8') as f:
        for i in orignal:
            f.write(i)


def save_record(Record):
    a = Record.task_name
    b = Record.start_time
    c = Record.end_time
    return a[:-1] + "," + b.strftime("%X") + "," + c.strftime("%X") +','+str(d)+"\n"


def print_todos(todo_list):
    todo_list = [i[:-1] for i in todo_list]
    for i, todo in enumerate(todo_list):
        print(f'{i}. {todo}')


def print_ddl(keyword, ifinitial=True):
    ddl = pd.read_csv(keyword)
    if ifinitial:
        length = len(ddl.index)
        minus = [date(ddl.iloc[i].year, ddl.iloc[i].month, ddl.iloc[i].day).toordinal() - date.today().toordinal() for i
                 in range(length)]
        sorted_id = sorted(range(len(minus)), key=lambda k: minus[k])
        for i in range(len(minus)):
            if minus[sorted_id[i]] > 0:
                print(ddl.project.iloc[i] + '  还剩下：' + str(minus[sorted_id[i]]) + '天')
            elif minus[sorted_id[i]] == 0:
                print(ddl.project.iloc[i] + '是今天')
            else:
                pass
    else:
        for i, dd in enumerate(ddl.project):
            print(f'{i}. {dd}')
        return ddl.project


def save_new_ddl(keyword, current):
    ddl = pd.read_csv(keyword)
    ddl.drop(current)
    ddl.to_csv(keyword)


def main():
    todo_listrecord = read_todos()  # 用三元组分别记录todo_list,源文件的开头和源文件的结尾
    todo_list = todo_listrecord[0]
    task_finished: list[Record] = []
    current_task = ''
    start_time = None
    is_ddl = False

    print_todos(todo_list)
    print_ddl(ddl_name)

    while True:
        if len(todo_list) == 0:
            print("没任务了，块点添加吧")
            break
        command = input(HINT)
        if command.isdigit():
            if current_task:
                print(f'正在执行{current_task}')
                continue
            num = int(command)
            if 0 <= num <= len(todo_list) - 1:
                current_task = todo_list[num]
                print(f'开始执行: {current_task[:-1]}')
                start_time = datetime.now()
            else:
                print('任务不在列表里')
        elif command == 'ok':
            if not current_task:
                print('没有任务在执行')
                continue
            end_time = datetime.now()
            task_finished.append(Record(current_task, start_time, end_time))
            save_todos(todo_listrecord, current_task)
            todo_list.remove(current_task)
            print(f'完成任务: {current_task}, 用时{(end_time - start_time)}')
            if is_ddl:
                save_new_ddl(ddl_name, current_task)
                is_ddl = False
            current_task = ''
            print_todos(todo_list)
            print_ddl(ddl_name)
        elif command == 'q':
            if not current_task:
                print('没有任务在执行')
                break
            end_time = datetime.now()
            task_finished.append(Record(current_task, start_time, end_time))
            save_todos(todo_listrecord, current_task)
            todo_list.remove(current_task)
            print(f'完成任务: {current_task}, 用时{(end_time - start_time)}')
            break
        elif command == 'b':
            if current_task:
                print(f'撤回成功')
                current_task = ''
            else:
                print(f'当前无任务，请重新输入')
        elif command == 'due':
            ddllist = print_ddl(ddl_name, False)
            command = input("选择你要进行的ddl")
            is_ddl = True

            if command.isdigit():
                num = int(command)
                if 0 <= num <= len(ddllist) - 1:
                    todo_list.append(ddllist[num])
                    current_task = ddllist[num]
                    print(f'开始执行: {current_task}')
                    start_time = datetime.now()
                else:
                    print('任务不在列表里')
            else:
                print('无效指令')
        elif command == 'wait':
            if not current_task:
                print('没有任务在执行')
                continue
            end_time = datetime.now()
            task_finished.append(Record(current_task, start_time, end_time))
            todo_list.remove(current_task)
            print(f'暂时用时: {current_task}, 用时{(end_time - start_time)}')
            if is_ddl:
                is_ddl = False
            current_task = ''
            print_todos(todo_list)
            print_ddl(ddl_name)
        else:
            print('无效指令')
    newtime = time.localtime(time.time())
    recording = str(newtime[1]) + '.' + str(newtime[2])
    with open(str(recording) + '.csv', 'a') as record:
        for i in range(len(task_finished)):
            record.write(save_record(task_finished[i]))


main()

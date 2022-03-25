import re
from dataclasses import dataclass
from datetime import datetime

FILE_NAME = 'plan.md'

TODOS = re.compile(r'(?<=## to do\n\n)(?P<todos>(.|\n)+)(?=\n##)')  # 放进 regex101.com 看看就好了
TODO_PREFIX = '- [ ] '

HINT = '输入任务标号以开始对应任务，输入 "ok" 以结束任务： '


@dataclass
class Record:
    task_name: str
    start_time: datetime
    end_time: datetime


def read_todos():
    with open(FILE_NAME, 'r') as f:
        text = f.read()
        todos = TODOS.search(text)['todos'].split('\n')
        todo_list = [todo.removeprefix(TODO_PREFIX) for todo in todos if todo]
        return todo_list


def save_todos(todo_list):
    with open(FILE_NAME, 'r+') as f:
        todo_text = ''.join([f'{TODO_PREFIX}{todo}\n' for todo in todo_list]) if todo_list else ''
        file_content = TODOS.sub(todo_text, f.read())
        print(file_content)
        f.truncate(0)  # clear file content
        f.seek(0)  # put pointer at the start of the file
        f.write(file_content)


def print_todos(todo_list):
    for i, todo in enumerate(todo_list):
        print(f'{i}. {todo}')


def main():
    todo_list = read_todos()
    tasks_finished: list[Record] = []
    current_task = ''
    start_time = None

    while True:
        if len(todo_list) == 0:
            print('所有任务都完成了！')
            break
        print('当前任务: ')
        print_todos(todo_list)

        command = input(HINT)

        if command.isdigit():
            if current_task:
                print(f'正在执行{current_task}')
                continue

            num = int(command)
            if 0 <= num <= len(todo_list) - 1:
                current_task = todo_list[num]
                print(f'开始执行: {current_task}')
                start_time = datetime.now()
            else:
                print('任务不在列表里')
        elif command == 'ok':
            if not current_task:
                print('没有任务在执行')
                continue
            end_time = datetime.now()
            tasks_finished.append(Record(current_task, start_time, end_time))
            todo_list.remove(current_task)
            print(f'完成任务: {current_task}, 用时{end_time - start_time}')
            current_task = ''
        elif command == 'q':
            break
        else:
            print('无效指令')

    print(tasks_finished)
    save_todos(todo_list)


main()

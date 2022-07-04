import read_todo
import to_todo


def main():
    print("1、加入ddl")
    print("2、加入新项目")
    while command := input("请输入指令"):
        command = int(command)
        if command == 1:
            print(read_todo.today_inbox_todo())
            index = int(input("请输入内容"))
            to_todo.set_deadline(index)
        else:
            to_todo.inbox()
        print("1、加入ddl")
        print("2、加入新项目")


if __name__ == '__main__':
    main()

import read_todo
import to_todo
import pd



def main():
    print("1、加入ddl")
    print("2、加入新项目")
    file="../todo.csv"
    while command := input("请输入指令\n"):
        todo=pd.read_csv(file)
        command = int(command)
        if command == 1:
            read_todo.today_inbox_todo('../todo.csv')
            index = int(input("请输入内容\n"))
            to_todo.set_deadline(index,file)
        else:
            to_todo.inbox(todo,file)
        print("1、加入ddl")
        print("2、加入新项目")


if __name__ == '__main__':
    main()

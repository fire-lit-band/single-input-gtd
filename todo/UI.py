import module
import read_todo
from Task import Task

def main():
    current_task = Task()
    result = "done"
    while result != "end":
        if result == "done":
            read_todo.display_todo()
        else:
            print("开始计时！！")
        newinput = input("请输入指令：\n")
        result,current_task = module.main(newinput,current_task)


if __name__ == "__main__":
    main()

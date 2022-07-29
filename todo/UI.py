import pandas as pd

import module
import read_todo
from Task import Task

def main():
    current_task = Task()
    result = "done"
    todo=pd.read_csv("../todo.csv")
    while result != "end":
        if result == "done":
            read_todo.display_todo(todo)
        else:
            print("开始计时！！")
        newinput = input("请输入指令：\n")
        result,current_task = module.main(newinput,current_task,todo)


if __name__ == "__main__":
    main()

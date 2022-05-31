

import pandas as pd

def to_todo(todo):
    data=pd.DataFrame(todo)
    data.to_csv("todo.csv")

def add_todo(todo):
    column_name=todo.columns
    new_task={}
    for i in column_name:
        content=input(i+":")
        new_task[i]=content
    todo=todo.append(pd.Series(new_task),ignore_index=True)
    return todo

if __name__=="__main__":
    todo=pd.read_csv("todo.csv")
    new_todo=add_todo(todo)
    new_todo.to_csv("todo.csv",index=False)
    print(new_todo)
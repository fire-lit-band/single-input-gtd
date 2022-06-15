

import pandas as pd
import os
from datetime import date

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

def add_record(Record):
    file_name='./time_record/' + date.today().isoformat() + ".csv"
    if not os.path.exists(file_name):
        column_names=pd.read_csv("record_sample.csv")
        column_names.to_csv(file_name,index=False)
    else:
        new_record={}
        column_names=pd.read_csv(file_name)
        record=list(Record.format())
        print(record)
        for i,j in enumerate(column_names):
            new_record[j]=record[i]
        column_names = column_names.append(pd.Series(new_record), ignore_index=True)
        column_names.to_csv(file_name,index=False)






if __name__=="__main__":
    todo=pd.read_csv("todo.csv")
    new_todo=add_todo(todo)
    new_todo.to_csv("todo.csv",index=False)
    print(new_todo)
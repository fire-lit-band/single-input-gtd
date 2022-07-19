import json
import numpy as np
import pandas as pd
import time
from datetime import datetime
import to_todo


def read_all_content(file="todo.csv"):
    return pd.read_csv(file)


def today_inbox_todo(file="todo.csv"):
    todo = pd.read_csv(file)
    todo=todo[todo.father.isnull() & todo.start_time.isnull()]
    for i in todo.index:
        print_child(i,0,todo)


def display_all_task(file="todo.csv"):
    todo = pd.read_csv(file)
    return todo["name"]

def today_ddl(file="todo.csv"):
    todo=pd.read_csv(file)
    ddl=todo[todo.father.isnull() & (~todo.start_time.isnull())]
    for i in ddl.index:
        print_child(i,0,todo)

def remain_time(ddl):
    remain_time_stamp=ddl-time.time()
    if remain_time_stamp<=0:
        return "已经过时"
    else:
        remain=datetime.fromtimestamp(remain_time_stamp)
        remain_tuple=(remain.year-1970,remain.month,remain.day,remain.hour-8,remain.minute)
        if remain_tuple[2]==0:
            return "还剩下天数："+str(remain_tuple[2])
        else:
            return "还剩下"+str(remain_tuple[3])+"小时,"+str(remain_tuple[4])+"分钟"

def display_todo():
    today_inbox_todo()
    today_ddl()


def print_child(i,incident,todo):
    leaf=eval(todo.at[i,'leaf'])
    if not np.isnan(todo.loc[i].start_time):
        print(" " * incident + str(i) + " " + todo.at[i, 'name']+" "+remain_time(todo.at[i,'start_time']))
    else:
        print(" " * incident + str(i) + " " + todo.at[i, 'name'] )
    if not leaf==[]:
        for j in leaf:
            print_child(to_todo.find('id',j)[0],incident+2,todo)


if __name__ == "__main__":
    today_ddl()

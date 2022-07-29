import json
import numpy as np
import pandas as pd
import time
from datetime import datetime
import to_todo
from treelib import Tree
from math import isnan


def read_all_content(file="todo.csv"):
    return pd.read_csv(file)


def today_inbox_todo(todo):
    tree=Tree()
    for i in todo.index:
        tree.create_node(todo.at[i,'name'],todo.at[i,'id'],parent=todo.at[i,'father'])
    tree.show()


def display_all_task(todo):
    return todo["name"]

def today_ddl(todo):
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

def display_todo(todo):
    print_child(todo)


def print_child(todo):
    tree = Tree()
    tree.create_node('root','root')
    for i in todo.index:
        if isnan(todo.at[i, 'father']):
            tree.create_node(str(i)+' '+todo.at[i, 'name'], todo.at[i, 'id'],'root')
        else:
            tree.create_node(str(i)+' '+todo.at[i, 'name'], todo.at[i, 'id'], parent=todo.at[i, 'father'])
    tree.show()

if __name__ == "__main__":
    today_ddl()

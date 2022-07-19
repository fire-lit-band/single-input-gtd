import datetime
import os
from datetime import date
from pathlib import Path
import time

import pandas as pd

from Finished import Finished
import read_todo
from datetime import date,datetime




def add_todo(todo: pd.DataFrame):
    column_name = todo.columns
    new_task = {}
    for i in column_name:
        content = input(i + ":")
        new_task[i] = content
    todo = todo.append(pd.Series(new_task), ignore_index=True)
    return todo




def delete_todo(content):
    # try:
    exist_todo = pd.read_csv("todo.csv")
    df=exist_todo
    content_isin = exist_todo["name"].isin([content])  # 返回是否含有content的表
    #print(content)

    if content_isin.any():  # 先判断一下有没有这一行，如果没有提早报错
        index_with_content=df[df.name==content].index.tolist()[0]
        num_of_sub=exist_todo.num.loc[index_with_content]
        if num_of_sub == 0:  # 0就是无穷次
            remain_todo = exist_todo
        elif num_of_sub == 1:
            remain_todo = exist_todo[~content_isin]  # 也就是直接删了
        else:  # 数量减少一次
            remain_todo = exist_todo
            remain_todo.loc[
                remain_todo["name"] == content, ["num"]
            ] -= 1
        remain_todo.to_csv("todo.csv", index=False)
    else:
        print("wrong")
        return False
    # except:
    # print("wrong")

def inbox():
    df=read_todo.read_all_content()
    print(read_todo.display_all_task())
    fatherpoint=''
    while command:=input("command"):
        if command=='add':
            content = input("你要加入什么内容")
            timestamp=time.time()
            new_task = {'name': content, 'id': timestamp, 'father':fatherpoint,'leaf': [],'num':0}
            df = df.append(pd.Series(new_task), ignore_index=True)
            df.to_csv("todo.csv", index=False)
            if not fatherpoint=='':
                index=find('id',fatherpoint)[0]
                df.at[index, 'leaf'] = eval(df.at[index, 'leaf']) + [timestamp]

            break
        else:
            if command.isdigit():
                # try:
                command_num=int(command)
                print(df.iloc[find('id',fatherpoint)].name)
                fatherpoint = df.at[command_num, 'id']
                # except:
                #     print("wrong")
    output_csv(df)



def output_csv(df,file="todo.csv"):
    df.to_csv(file,index=False)



def find(column_name,content):
    exist_todo = read_todo.read_all_content()
    df = exist_todo
    index_with_content = df[df[column_name] == content].index.tolist()
    return index_with_content


def set_deadline(index):
    year=input("请输入年份")
    if year=='':
        year=date.today().year
    else:
        year=int(year)
    month=input("请输入月份")
    if month=='':
        month=date.today().month
    else:
        month=int(month)
    day=input("请输入日期")
    if day=='':
        day=date.today().day
    else:
        day=int(day)
    hour=input("请输入小时")
    if hour=='':
        hour=23
        minute=59
        second=59
    else:
        hour=int(hour)
        minute=input("请输入分钟")
        if minute=='':
            minute=0
            second=0
        else:
            minute=int(minute)
            second=0
    ddl=datetime(year,month, day, hour, minute, second).timestamp()
    df=read_todo.read_all_content()
    df.at[index,'start_time']=ddl
    output_csv()


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

def delete_todo(content):
    #try:
    exist_todo=pd.read_csv("todo.csv")
    content_isin=exist_todo['name'].isin([content]) #返回是否含有content的表
    if content_isin.any():  #先判断一下有没有这一行，如果没有提早报错
        row_with_column = exist_todo[content_isin]
        num_of_sub=row_with_column.at[0,'sub_tasks_count']
        if num_of_sub==0: #0就是无穷次
            remain_todo=exist_todo
        elif num_of_sub==1:
            remain_todo = exist_todo[~content_isin] # 也就是直接删了
        else:   #数量减少一次
            remain_todo=exist_todo
            remain_todo.loc[remain_todo['name']==content,['sub_tasks_count']]-=1
        remain_todo.to_csv("todo.csv",index=False)
    else:
        print("wrong")
        return False
    #except:
        #print("wrong")





if __name__=="__main__":
    delete_todo('数学分析')
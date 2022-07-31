import PySimpleGUI as sg
import numpy as np
import pandas as pd
import function.calendarUItest as cl
import function.clockUI as clock
import time
from datetime import date,datetime
from classes.Finished import Finished
from classes.Task import Task
from pathlib import Path
import time

def find(column_name,content,todo):
    exist_todo = todo
    df = exist_todo
    index_with_content = df[df[column_name] == content].index.tolist()
    return index_with_content


def add_record(Record: Finished,file="record_sample.csv"):
    file_name = Path("./time_record", date.today().isoformat()).with_suffix(
        ".csv"
    )
    if not file_name.exists():
        column_names = pd.read_csv(file)
        column_names.to_csv(file_name,index=False)
    column_names = pd.read_csv(file_name)
    record = list(Record.format())
    print(record)
    new_record = dict(zip(column_names, record))
    column_names = column_names.append(
        pd.Series(new_record), ignore_index=True
    )
    column_names.to_csv(file_name, index=False)

def set_default(key,values,datetuple,content,havecontent):
    if not havecontent:
        if key==[]:
            key=[""]
        values['father']=key[0]
        values['id'] = time.time()
    else:
        content.update(values)
        values=content
    if datetuple == None:

        if values['hour'].isdigit():
            todays=date.today()
            datetuple=[todays.year,todays.month,todays.day]
            if 0<=int(values['hour'])<=24:
                if values['minute'].isdigit():
                    if 0<=int(values['minute'])<=60:
                        values['start_time']=time.mktime((*datetuple, int(values['hour']), int(values['minute']), 0, 0,0,0))
                    else:
                        sg.Popup('输入错误')
                        raise TypeError
                elif values['minute']=='':
                    values['minute']=0
                    values['start_time'] = time.mktime(
                        (*datetuple, int(values['hour']), int(values['minute']), 0, 0, 0, 0))
                else:
                    sg.Popup('输入错误')
                    raise TypeError
        elif values['hour']=='':
            values['start_time']=np.nan
        else:
            sg.Popup('输入错误')
            raise TypeError
    else:
        if values['hour']=='':
            values['hour']=0
            values['minute']=0
            values['start_time'] = time.mktime((*datetuple, int(values['hour']), int(values['minute']), 0, 0, 0, 0))
        elif values['hour'].isdigit():
            if 0<=int(values['hour'])<=24:
                if values['minute'].isdigit():
                    if 0<=int(values['minute'])<=60:
                        values['start_time']=time.mktime((*datetuple, int(values['hour']), int(values['minute']), 0, 0,0,0))
                    else:
                        sg.Popup('输入错误')
                        raise TypeError
                elif values['minute'] == '':
                    values['minute'] = 0
                    values['start_time'] = time.mktime(
                        (*datetuple, int(values['hour']), int(values['minute']), 0, 0, 0, 0))
                else:
                    sg.Popup('输入错误')
                    raise TypeError
        else:
            sg.Popup('输入错误')
            raise TypeError





    del values['hour'],values['minute']
    return values

def todo_content(key,todoTree,df,file,content=None):
    if content==None:
        content={'name':'','num':'','hour':'','minute':'','repetition_gap':'','task_value':''}
        datetuple = None
        havecontent=False
    else:
        havecontent=True
        if not np.isnan(content['start_time']):
            struct_times=time.localtime(content['start_time'])
            datetuple=[struct_times.year,struct_times.month,struct_times.day]
            content['hour']=struct_times.hour
            content['minute'] = struct_times.minute
        else:
            datetuple=None
    layout = [[sg.Text('名字')], [sg.Input(content['name'],key='name')],
              [sg.Text('重复次数')], [sg.Input(content['num'],key='num')],
              [sg.Text('截止时间')],
              [sg.Button('年月日', key='date')],
              [sg.Text(datetuple, key='date_tuple')],
              [sg.Text('时')], [sg.Input(content['hour'],key='hour')],
              [sg.Text('分')], [sg.Input(content['minute'],key='minute')],
              [sg.Text('间隔天数')], [sg.Input(content['repetition_gap'],key='repetition_gap')],
              [sg.Text('个人感官价值')], [sg.Input(content['task_value'],key='task_value')],

              [sg.Button('cancel'), sg.Button('ok')]]
    windowadd = sg.Window('add', layout)

    while True:  # Event Loop
        event, values = windowadd.read()
        if event in (sg.WIN_CLOSED, 'cancel'):
            windowadd.close()
            return todoTree
        if event == 'ok':
            break
        if event == 'date':
            datetuple = cl.popup_get_date()
            windowadd['date_tuple'].update(str(datetuple))
    windowadd.close()
    try:
        values = set_default(key, values, datetuple,content,havecontent)
    except TypeError:
        return todoTree
    if havecontent:
        df=df.drop([find('id',key[0],df)[0]])

    df = pd.concat([df, pd.Series(values).to_frame().T], ignore_index=True)
    df.to_csv(file, index=False)
    return todoTree


def readcsv(file):
    todoTree = sg.TreeData()
    df = pd.read_csv(file)
    for i in df.index:
        key = df.at[i, "id"]
        text = df.at[i, "name"]
        todoTree.insert('',key,text,[])
    for i in df.index:
        parent = df.at[i, "father"]
        key = df.at[i, "id"]
        text = df.at[i, "name"]
        if np.isnan(parent):
            parent = ""
        todoTree.tree_dict[todoTree.tree_dict[key].parent].children.remove(todoTree.tree_dict[key])
        todoTree.tree_dict[key].parent=parent
        todoTree.tree_dict[parent].children.append(todoTree.tree_dict[key])



    layout = [
        [sg.Button('cancel')],
        [sg.Tree(data=todoTree, headings=['Size', ],
                 auto_size_columns=True,
                 select_mode=sg.TABLE_SELECT_MODE_EXTENDED,
                 num_rows=20,
                 col0_width=40,
                 key='TREE',
                 show_expanded=False,
                 enable_events=True,
                 expand_x=True,
                 expand_y=True)],
        [sg.Button('add'),sg.Button('clear')],
        [sg.Button('delete'),sg.Button('revise')],
        [sg.Button('start')]
    ]
    return df,todoTree,layout

def delete_in_tree(df,file,values,window):
    df = tododelete(df, file, values['TREE'])
    df.to_csv(file, index=False)
    df, todoTree, layout = readcsv(file)
    window['TREE'].update(todoTree)
    return df,file,window

def tododelete(df,file,key):
    df=df[df.id!=key[0]]

    if not df[df.father==key[0]].empty:
        for i in df[df.father==key[0]].id:
            df=tododelete(df, file, [i])
    df=df[df.father!=key[0]]
    return df

def finished_delete(todo,file,window,values):
    # try:
    exist_todo = todo
    df=exist_todo
    content=values['TREE'][0]
    content_isin = exist_todo["id"].isin([content])  # 返回是否含有content的表
    #print(content)

    if content_isin.any():  # 先判断一下有没有这一行，如果没有提早报错
        index_with_content=df[df.id==content].index.tolist()[0]
        num_of_sub=exist_todo.num.loc[index_with_content]
        if num_of_sub == 0:  # 0就是无穷次
            remain_todo = exist_todo
        elif num_of_sub == 1:
            remain_todo = exist_todo[~content_isin]  # 也就是直接删了
        else:  # 数量减少一次
            remain_todo = exist_todo
            remain_todo.loc[
                remain_todo["id"] == content, ["num"]
            ] -= 1
        df=remain_todo
        df.to_csv(file, index=False)
        df, todoTree, layout = readcsv(file)
        window['TREE'].update(todoTree)
        return df, file,  window
    else:
        print("wrong")
        return False

def pause_task(current_task: Task, command: str):
    if current_task.task_name == "":
        sg.Text('当前没有任务')
    else:
        current_task.end_time = datetime.now()

        if command == "!":
            current_task = end_task(current_task, "紧急事情")
            current_task.task_name = input("请输入当前的紧急事项")
            current_task = begin_task(current_task, current_task.task_name)
        elif command == "~":
            current_task = end_task(current_task, "休息")
        elif command == "p":
            current_task = end_task(current_task, "休息")
            current_task.task_name = ""
    return current_task

def finished_task(current_task: Task, command: str):
    if current_task.task_name == "":
        if command == "ok":
            sg.Popup('当前没有任务')
    else:
        current_task.end_time = datetime.now()
        current_task = end_task(current_task, "finished")
        current_task.task_name = ""
    return current_task


def begin_task(current_task: Task, task_name: str):
    current_task.task_name = task_name
    print(f"开始执行: {current_task.task_name}")
    current_task.start_time = datetime.now()
    return current_task


def end_task(current_tasks: Task, reason: str):
    current_tasks.end_time = datetime.now()
    layout=[[sg.Text("请输入你完成的内容")],[sg.Input()],[sg.Button('ok')]]
    window=sg.Window("请输入你完成的内容",layout)
    event,subname=window.read()
    subname=subname[0]
    if event=='ok':
        window.close()
    record = Finished(
        name=current_tasks.task_name,
        subname=subname,
        actuall_start_time=current_tasks.start_time,
        actuall_end_time=current_tasks.end_time,
        actlength=0,
        actshift=0,
        reason=reason,
    )
    add_record(record,'./data/record_sample.csv')
    return current_tasks



def main():
    file='./data/todo.csv'
    df,todoTree,layout=readcsv(file)


    window = sg.Window('用户输入部分', layout,finalize=True)
    current_task=Task()


    while True:     # Event Loop

        event, values = window.read()

        if event in (sg.WIN_CLOSED, 'cancel'):
            break
        if event =='add':

            todo_content(values['TREE'],todoTree,df,file)
            df, todoTree, layout = readcsv(file)
            window['TREE'].update(todoTree)
        if event=='clear':
            window['TREE'].update(todoTree)
        if event=='delete':
            df,file,window=delete_in_tree(df,file,values,window)
        if event=='revise':
            content=dict(df.loc[find('id',values['TREE'][0],df)[0]])
            content['hour']=''
            content['minute']=''
            todo_content(values['TREE'], todoTree, df, file,content)
            df, todoTree, layout = readcsv(file)
            window['TREE'].update(todoTree)
        if event=='start':
            current_task = begin_task(current_task, df.at[find('id',values['TREE'][0],df)[0], 'name'])
            start_time,endtime,clockevent,paused=clock.main(current_task.task_name)
            if clockevent=='-Finished-':
                current_task = finished_task(current_task, 'q')
                df,file,window=finished_delete(df,file,window,values)
            if clockevent in (sg.WIN_CLOSED, 'Exit','-RUN-PAUSE-'):
                if paused==True:
                    current_task = pause_task(current_task, 'p')





    window.close()


if __name__=="__main__":
    main()
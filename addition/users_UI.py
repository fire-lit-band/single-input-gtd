import PySimpleGUI as sg
import numpy as np
import pandas as pd
import calendarUItest as cl
import time
import sys
sys.path.append('../todo')
import to_todo
from datetime import date

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
        df=tododelete(df, file, [values['id']], df)

    df = pd.concat([df, pd.Series(values).to_frame().T], ignore_index=True)
    df.to_csv(file, index=False)
    return todoTree


def readcsv(file):
    todoTree = sg.TreeData()
    df = pd.read_csv(file)
    for i in df.index:
        parent = df.at[i, "father"]
        if np.isnan(parent):
            parent = ""
        key = df.at[i, "id"]
        text = df.at[i, "name"]
        todoTree.insert(parent, key, text, [])

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
        [sg.Button('delete'),sg.Button('revise')]
    ]
    return df,todoTree,layout



def tododelete(df,file,key,todo):
    df=df.drop([to_todo.find('id',key[0],todo)[0]])
    return df

def main():
    file='../todo.csv'
    df,todoTree,layout=readcsv(file)


    window = sg.Window('用户输入部分', layout,finalize=True)


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
            df=tododelete(df,file,values['TREE'],df)
            df.to_csv(file,index=False)
            df, todoTree, layout = readcsv(file)
            window['TREE'].update(todoTree)
        if event=='revise':
            content=dict(df.loc[to_todo.find('id',values['TREE'][0],df)[0]])
            content['hour']=''
            content['minute']=''
            todo_content(values['TREE'], todoTree, df, file,content)
            df, todoTree, layout = readcsv(file)
            window['TREE'].update(todoTree)




    window.close()


if __name__=="__main__":
    main()
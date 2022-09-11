import PySimpleGUI as sg
import numpy as np
import pandas as pd
import function.calendarUItest as cl
import function.clockUI as clock
import time
from datetime import date,datetime,timedelta
from classes.Finished import Finished
from classes.Task import Task
from pathlib import Path
import time
import function.init_daily as daily

QT_ENTER_KEY1 = 'special 16777220'
QT_ENTER_KEY2 = 'special 16777221'

def find(column_name,content,df):
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
    column_names = pd.concat([column_names, pd.Series(new_record).to_frame().T], ignore_index=True)
    column_names.to_csv(file_name, index=False)

def set_default(key,values,datetuple,content): # 设置日期的时候的一些默认选项
    if key==[]:
        key=[""]
    values['id'] = time.time()
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
def revise_content(key,df,file,content):
    df=pd.read_csv(file)
    if not np.isnan(content['start_time']):
        struct_times = time.localtime(content['start_time'])
        print(struct_times)
        datetuple = [struct_times.tm_year, struct_times.tm_mon, struct_times.tm_mday]
        content['hour'] = struct_times.tm_hour
        content['minute'] = struct_times.tm_min
    else:
        datetuple = None
    values,check=content_interface(key, content, datetuple)
    #print(find('id',key[0],df)[0])
    if check:
        df.loc[find('id',key[0],df)[0]]=values

        df.to_csv(file, index=False)


def add_content(key,df,file,todo_daily):  #
    # if content==None:
    content={'name':'','num':1,'hour':'','minute':'','repetition_gap':0,'task_value':''}
    datetuple = None
    havecontent=False
    # else:
    #     havecontent=True
    #     if not np.isnan(content['start_time']):
    #         struct_times=time.localtime(content['start_time'])
    #         print(struct_times)
    #         datetuple=[struct_times.tm_year,struct_times.tm_mon,struct_times.tm_mday]
    #         content['hour']=struct_times.tm_hour
    #         content['minute'] = struct_times.tm_min
    #     else:
    #         datetuple=None
    values,check=content_interface(key,content,datetuple)
    print(key)
    values['father']=key[0]
    if check:
        df = pd.read_csv(file)
        df = pd.concat([ pd.Series(values).to_frame().T,df], ignore_index=True)
        df.to_csv(file, index=False)


def content_interface(key,content,datetuple):
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
    windowadd = sg.Window('add', layout,return_keyboard_events=True)

    while True:  # Event Loop
        event, values = windowadd.read()
        if event in (sg.WIN_CLOSED, 'cancel','Escape:27'):
            windowadd.close()
            return values,False
        if event in  ('ok','\r', QT_ENTER_KEY1, QT_ENTER_KEY2):
            break
        if event == 'date':
            datetuple = cl.popup_get_date()
            windowadd['date_tuple'].update(str(datetuple))
    windowadd.close()
    values['id']=key
    values = set_default(key, values, datetuple,content)
    return values,True

def cauculate_ddl(start_time):
    now=datetime.now()
    #print((now-start_time)//(24*60*60))

    if np.isnan(start_time):
        return ''

    else:
        delta1 =  datetime.fromtimestamp(int(start_time))-now
        if delta1<timedelta(0):
            return '已经超时'
        else:
        #print(type(datetime.fromtimestamp(int(start_time))))

        #if now-start_time>float(time.mktime(datetime(1970,1,1,0,0,0,0).timetuple())):
            print(delta1)
            if delta1.days>=1:
                return str(delta1.days)+'天'
            else:
                print(delta1)
                return str(delta1.seconds//3600) + '时'+str((delta1.seconds//60)%60)+'分'


def option(df):
    return df.sort_values(by='start_time',inplace=False)


def readcsv(file,todo_daily_file,isexpand=False): #读文件 ，并生成树状结构
    todoTree = sg.TreeData()
    df = daily.init(file,todo_daily_file)
    df=option(df)
    df1=df[pd.isna(df['father'])]
    while not df1.empty:
        keyset=[]
        for i in df1.index:
            parent = df.at[i, "father"]
            key = df.at[i, "id"]
            keyset.append(key)
            text = df.at[i, "name"]
            ddl = cauculate_ddl(df.at[i, 'start_time'])
            if np.isnan(parent):
                todoTree.insert('', key, text, [ddl])
            else:
                todoTree.insert(parent, key, text, [ddl])
        df1= pd.DataFrame()
        for k in keyset:
            df2=df[df["father"]==k]
            df1=pd.concat([df1,df2],axis=0)



    #
    # print(todoTree)
    # for i in df2.index:
    #
    #     key = df.at[i, "id"]
    #     text = df.at[i, "name"]
    #     ddl = cauculate_ddl(df.at[i, 'start_time'])
    #     #todoTree.tree_dict[todoTree.tree_dict[key].parent].children.remove(todoTree.tree_dict[key])
    #     # todoTree.tree_dict[key].parent=parent
    #     # todoTree.tree_dict[parent].children.append(todoTree.tree_dict[key])
    #     print(parent)
    #     todoTree.insert(parent, key, text, [ddl])



    layout = [
        [sg.Button('cancel')],
        [sg.Tree(data=todoTree, headings=['截止日期', ],
                 auto_size_columns=True,
                 select_mode=sg.TABLE_SELECT_MODE_BROWSE,
                 num_rows=20,
                 col0_width=40,
                 key='TREE',
                 show_expanded=isexpand,
                 enable_events=True,
                 expand_x=True,
                 expand_y=True,right_click_menu=sg.MENU_RIGHT_CLICK_EDITME_EXIT)],
        [sg.Input(key='IN')],
        [sg.Button('add'),sg.Button('clear'),sg.Button('clear all')],
        [sg.Button('delete'),sg.Button('revise')],
        [sg.Button('start')]
    ]
    return df,todoTree,layout

def delete_in_tree(df,file,values,window): #直接删除主todo里的内容
    df=pd.read_csv(file)# 删除树状图里面的内容
    df = tododelete(df, file, values['TREE'])
    df.to_csv(file, index=False)

def tododelete(df,file,key):  # 删除数据里面的内容
    df=df[df.id!=key[0]]

    if not df[df.father==key[0]].empty:
        for i in df[df.father==key[0]].id:
            df=tododelete(df, file, [i])
    df=df[df.father!=key[0]]
    return df

def finished_delete(df,file,values,todo_daily): # 任务结束后删除内容
    # try:
    df
    content=values['TREE'][0]
    content_isin = df["id"].isin([content])  # 返回是否含有content的表
    # daily_name = Path(todo_daily, date.today().isoformat()).with_suffix(".csv")
    # today=pd.read_csv(daily_name)
    # today.drop(index=today[today['id']==values].index.tolist()[0])
    # today.read_csv(daily_name,index=False)
    #print(content)

    if content_isin.any():  # 先判断一下有没有这一行，如果没有提早报错
        index_with_content=df[df.id==content].index.tolist()[0]
        num_of_sub=df.at[index_with_content,'num']
        gap=df.at[index_with_content,'repetition_gap']
        start_time=df.at[index_with_content,'start_time']
        if num_of_sub==1:
            df= df[~content_isin]
        else :  # 0就是无穷次
            if np.isnan(start_time):
                start_time=time.time()
            if np.isnan(gap):
                start_time=np.nan
            if not np.isnan(start_time):
                # update,start_time
                start_time=time.mktime((datetime.fromtimestamp(start_time)+timedelta(days=gap)).timetuple())
                df.at[index_with_content,'start_time']=start_time
            if np.isnan(num_of_sub) or num_of_sub==0:
                df=df
            if num_of_sub >=2:
                df.at[index_with_content,'num']-=1

        df.to_csv(file, index=False)


    else:
        print("wrong")
        return False

def pause_task(current_task: Task, command: str): # 任务暂停
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

def finished_task(current_task: Task, command: str): # 任务结束
    if current_task.task_name == "":
        if command == "ok":
            sg.Popup('当前没有任务')
    else:
        current_task.end_time = datetime.now()
        current_task = end_task(current_task, "finished")
        current_task.task_name = ""
    return current_task


def begin_task(current_task: Task, task_name: str): # 任务开始
    current_task.task_name = task_name
    print(f"开始执行: {current_task.task_name}")
    current_task.start_time = datetime.now()
    return current_task


def end_task(current_tasks: Task, reason: str): # 任务结束记录
    current_tasks.end_time = datetime.now()
    layout=[[sg.Text("请输入你完成的内容")],[sg.Input()],[sg.Button('ok')]]
    window=sg.Window("请输入你完成的内容",layout,return_keyboard_events=True)
    while True:
        event,subname=window.read()
        subname=subname[0]
        if event in ('ok','\r', QT_ENTER_KEY1, QT_ENTER_KEY2):
            window.close()
            break
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
    todo_tempalate='./data/todo_tempalate.csv'
    todo_daily_file='./dailytodo'
    Path('./dailytodo').mkdir(parents=True, exist_ok=True)
    daily_name = Path(todo_daily_file, date.today().isoformat()).with_suffix(".csv")

    df,todoTree,layout=readcsv(file,todo_daily_file)


    window = sg.Window('用户输入部分', layout,finalize=True,return_keyboard_events=True,resizable=True,auto_size_text=True)
    current_task=Task()


    while True:     # Event Loop

        event, values = window.read()
        element=window.find_element_with_focus()
        print(event,values,element)

        if event in (sg.WIN_CLOSED, 'cancel','Escape:27'):
            break
        if event =='add':
            if values['TREE']==[]:
                values['TREE']=['']
            add_content(values['TREE'],df,file,daily_name)
            df, todoTree, layout = readcsv(file,todo_daily_file)
            window['TREE'].update(todoTree)
        if event=='clear':
            window['TREE'].update(todoTree)
        if event=='delete':
            delete_in_tree(df,file,values,window)
            df, todoTree, layout = readcsv(file,todo_daily_file)
            window['TREE'].update(todoTree)
        if event=='revise':
            content=dict(df.loc[find('id',values['TREE'][0],df)[0]])
            content['hour']=''
            content['minute']=''
            revise_content(values['TREE'], df, file,content)
            df, todoTree, layout = readcsv(file,todo_daily_file)
            window['TREE'].update(todoTree)
        if event=='clear all':
            df=pd.read_csv(todo_tempalate)
            df.to_csv(file,index=False)
            df, todoTree, layout = readcsv(file,todo_daily_file)
            window['TREE'].update(todoTree)
        if event in ('start',' '):
            if type(element)==type(window['TREE']):
                current_task = begin_task(current_task, df.at[find('id',values['TREE'][0],df)[0], 'name'])
                start_time,endtime,clockevent,paused=clock.main(current_task.task_name)
                if clockevent=='-Finished-':
                    current_task = finished_task(current_task, 'q')
                    finished_delete(df,file,values,todo_daily_file)
                    df, todoTree, layout = readcsv(file,todo_daily_file)
                    window['TREE'].update(todoTree)

                if clockevent in (sg.WIN_CLOSED, 'Exit','-RUN-PAUSE-'):
                    current_task = pause_task(current_task, 'p')

        # 下面是键盘映射

        if event in ('\r', QT_ENTER_KEY1, QT_ENTER_KEY2):
            if not type(element)==type(window['TREE']):
                newcontent={'name':values['IN'],'id':time.time(),'num':1,'fixed':'False'}
                df = pd.concat([ pd.Series(newcontent).to_frame().T,df], ignore_index=True)
                df.to_csv(file, index=False)
                df, todoTree, layout = readcsv(file,todo_daily_file)
                window['TREE'].update(todoTree)
                window['IN'].update('')
            if values['IN']=='':
                if values['TREE']:
                    content = dict(df.loc[find('id', values['TREE'][0], df)[0]])
                    content['hour'] = ''
                    content['minute'] = ''
                    revise_content(values['TREE'], df, file, content)
                    df, todoTree, layout = readcsv(file,todo_daily_file)
                    window['TREE'].update(todoTree)
        if event=='Edit Me':
            if values['TREE']:
                content = dict(df.loc[find('id', values['TREE'][0], df)[0]])
                content['hour'] = ''
                content['minute'] = ''
                revise_content(values['TREE'], df, file, content)
                df, todoTree, layout = readcsv(file,todo_daily_file)
                window['TREE'].update(todoTree)
        if event=='Delete:46':
            delete_in_tree(df, file, values, window)
            df, todoTree, layout = readcsv(file,todo_daily_file)
            window['TREE'].update(todoTree)
        if event in ('Down:40'):
            if values['TREE']==[]:
                # tree=window['TREE']
                # tree.widget.selection_set(key=df.at[0,'id'])
                values['TREE']=df.at[0,'id']
                window['TREE'].update(todoTree)
        if event in ('+'):
            add_content(values['TREE'], df, file,daily_name)
            df, todoTree, layout = readcsv(file,todo_daily_file)
            window['TREE'].update(todoTree)








    window.close()

if __name__=="__main__":
    main()
    # 0.00003 bug更新（比如框格大小可以调整，以及添加子项目的一些问题）
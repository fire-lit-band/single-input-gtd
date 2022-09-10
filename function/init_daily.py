from pathlib import Path
from datetime import date,datetime,timedelta
import pandas as pd
import numpy as np



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



def init(file,todo_daily):
    daily_name = Path(todo_daily,date.today().isoformat()).with_suffix(".csv")
    if not daily_name.exists():
        column_names = pd.read_csv('./data/daily_todo.csv')
        column_names.to_csv(daily_name, index=False)
    yesterday_name = Path(todo_daily, (date.today()+timedelta(days=-1)).isoformat()).with_suffix(".csv")
    if not yesterday_name.exists():
        column_names = pd.read_csv('./data/daily_todo.csv')
        column_names.to_csv(yesterday_name, index=False)
    df=pd.read_csv(file)

    yesterday=pd.read_csv(yesterday_name)
    todaylist=[]
    droplist=[]
    processdf=df.copy()
    # for i in df.index:
    #     if not yesterday[yesterday['id']==key].isna: #是昨天的任务
    #         if np.isnan(df.at[i,'start_time']): #如果没有明确标注时间
    #             key=df.at[i,'id']
    #             index=yesterday[yesterday['id']==key].index.tolist()[0]
    #             num=df.at[index,'num']
    #             if yesterday[yesterday['id'] == key]['status'] == 'done':  # 是否做完
    #                 if num!=1 or np.isnan(num):# 不是无数次
    #                     todaylist.append(i)
    #                     if num>=2:
    #                         df.at[i,'num']-=1
    #                 else:
    #                     droplist.append(i)
    #         else:
    #             now = datetime.now()
    #             start_time=df.at[i,'start_time']
    #             delta1 = datetime.fromtimestamp(int(start_time)) - now
    #             if delta1 <= timedelta(0): #也就是已经超过时间了
    #                 if not (np.isnan(num) or num==0): #也就是不是无数次（这时候才有进行时间的安排）
    #
    #                     for j in range(num):
    #                         if delta1==timedelta(j):
    #                             todaylist.append(i)
    #                             break
    #                         else:
    #                             if timedelta(j)<(-delta)<timedelta(j+1): #在两个之间
    #
    #                 if not yesterday[yesterday['id'] == key].isna:  # 如果昨天做了的话
    #                     index = yesterday[yesterday['id'] == key].indextolist()[0]
    #                     num = df.at[index, 'num']
    #                     if num != 1 or :
    #                         todaylist.append(i)
    #                         if num >= 2:
    #                             df.at[i, 'num'] -= 1
    #                         if df.at[i,'fixed']=='True':
    #                             droplist.append(i)
    #                     else:
    #                         droplist.append(i)
    #                 else:
    #                     if df.at[i, 'fixed'] == 'True':
    #                         droplist.append(i)
    for i in yesterday.index:
        if not np.isnan(yesterday.at[i, 'start_time']):
            if (yesterday.at[i,'status']=='done') or \
                    (datetime.fromtimestamp(int(yesterday.at[i,'start_time'])) -datetime.now()<=timedelta(0) and yesterday.at[i,'fixed']=='True'):
                key = df.at[i, 'id']
                index = df[df['id'] == key].index.tolist()[0]
                num = df.at[index, 'num']
                if np.isnan(num) or num != 1 :
                    todaylist.append(index)
                    if num >= 2:
                        df.at[i, 'num'] -= 1
                else:
                    df.drop(index=index)

    for i in df.index: #先看有时间的这些
        if not np.isnan(df.at[i, 'start_time']):
            now = datetime.now()
            start_time=df.at[i,'start_time']
            delta1 = datetime.fromtimestamp(int(start_time)) - now
            if delta1 <= timedelta(0): #也就是已经超过时间了
                num=df.at[i,'num']
                if np.isnan(num) or num==0:
                    todaylist.append(i)
                else:

                    for j in range(int(num)+1):
                        if delta1==timedelta(j):
                            todaylist.append(i)
                            break
            else:
                todaylist.append(i)
        else:
            todaylist.append(i)
    df.to_csv(file,index=False)
    today=df.loc[todaylist]
    if 'status' not in today.columns:
        today.insert(loc=len(today.columns),column='status',value=['unfinished' for i in range(len(today.index))])
    today.to_csv(daily_name,index=False)
    return today





# init('./data/todo.csv','./dailytodo')
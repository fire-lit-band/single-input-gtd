def process_time(string):
    a=string.split(":")
    return int(a[0])*3600+int(a[1])*60+int(a[2])
def basetime():
    g=datetime.combine(datetime.today(),time(hour=7, minute=0, second=0))
    while g<=datetime.combine(datetime.today(),time(hour=23, minute=59, second=59)):
        yield g
        g= g + timedelta(seconds=1)
def resulttime(start,end):
    g = datetime.combine(datetime.today(), time(hour=7, minute=0, second=0))
    control=0
    while g <= datetime.combine(datetime.today(), time(hour=23, minute=59, second=59)):
        if g in start or g in end:
            control=1-control
        if control==0:
            yield 0
        else:
            yield 1
        g=g+timedelta(seconds=1)



import pandas as pd
import matplotlib.pyplot as pl
import matplotlib.dates as mdates
from datetime import timedelta
from datetime import time
from datetime import date
from datetime import datetime

g=pd.read_csv('./time_record/' + date.today().isoformat() + ".csv")
start_time=g.start_time
end_time=g.end_time
base=[*basetime()]
transfer_start=[datetime.strptime(datetime.strftime(datetime.today(),"%Y-%m-%d ")+i,"%Y-%m-%d %X") for i in start_time]
transfer_end=[datetime.strptime(datetime.strftime(datetime.today(),"%Y-%m-%d ")+i,"%Y-%m-%d %X") for i in end_time]
result=[*resulttime(transfer_start,transfer_end)]
#print(transfer_end)
#for i in range(len(transfer_start)):
    #result = [1 for j in [*basetime()] if ]
fig = pl.figure()
ax = fig.add_subplot(1,1,1)
    #result=result[:transfer_start[i]]+[1 for i in range(transfer_end[i]-transfer_start[i]+1)]+result[transfer_end[i]+1:]
ax.xaxis.set_major_formatter(mdates.DateFormatter('%X'))
#X轴的间隔为小时
ax.xaxis.set_major_locator(mdates.HourLocator(interval=4))
pl.fill(base,result)
ax.set_aspect(0.05)
pl.rcParams['figure.figsize'] = (200.0, 200.0)
pl.savefig('./time_record/' + date.today().isoformat() + ".jpg")
pl.show()


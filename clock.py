from tkinter import *
from datetime import *
from tkinter.messagebox import *


class TestTime(object):
    def __init__(self, current,expect,master=None):
        self.current_task = current
        self.expect_time = expect
        self.old_time=datetime.now()
        self.root = master
        self.root.geometry('400x200')
        self.root.resizable(width=False, height=False)
        self.label_a = Label(self.root, text='当前本地时间为：\t\t')
        self.label_a.pack()
        self.label_b = Label(self.root, text="")
        self.label_b.pack()
        self.label_c = Label(self.root, text=f'\n距离{self.current_task}完成还有\t\t')
        self.label_c.pack()
        self.label_d = Label(self.root, text="")
        self.label_d.pack()
        self.update_time()


    def update_time(self):
        self.update_a()
        self.update_b()

    def update_a(self):
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.label_b.configure(text=now)
        self.root.after(1000, self.update_a)

    def update_b(self):
        # 获取当日日期，不包含时间，str
        # 字符串拼接，组成当日12点
        selfhour=self.expect_time//60
        selfminute=self.expect_time%60
        t = self.old_time + timedelta(hours=selfhour,minutes=selfminute)- datetime.now()
        t=str(t)
        t=t[:-7]
        self.label_d.configure(text=t)
        self.root.after(1000, self.update_b)

def clock(current,expect):
    try:
        root = Tk()
        root.title('计时小界面')
    # 窗口置顶.
        root.wm_attributes('-topmost', 1)
        TestTime(current,expect,root)
        root.mainloop()
    except KeyboardInterrupt:
        return 'end'

if __name__ == '__main__':
    current = input()
    window = Tk()
    hint = Label(window, text='请输入时间（单位为分钟）：')
    hint.pack()
    var = 0
    entry = Entry(window, width=20)
    entry.pack()


    def change_state():
        global var
        var = entry.get()
        window.quit()  # 调用get()方法，将Entry中的内容获取出来


    Button(window, text='获取信息', command=change_state).pack()

    window.mainloop()
    expect = int(var)
    clock(current, expect)





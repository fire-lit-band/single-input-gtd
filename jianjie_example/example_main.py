from pickletools import uint1
from typing import Generic, TypeVar
T=TypeVar('T')

#task类
class Task(object):
    name:str=""
    timeLimit:str=""
    
class Todo(Task):
    activity="reading"
    def DoTask(self):
        print(self.name+" "+self.timeLimit+self.activity)

class ddl(Task):
    activity="exam"
    def Cram(self):
        print(self.name+" "+self.timeLimit+self.activity)

class UI():
    command:str=None
    def isShow(self):
        pass
    def Show(self):
        while True:
            fsm

            command = input(HINT)
            
            
class fsm():
    #创建即进入初始状态
    def __init__(self) -> None:
        u=UI()
        u.command=input()
        u.Show()
        result=
        self.StateTransfer(self)
    def StateTransfer(self,fsm:fsm,lastResult)
     #状态机
    pass           
    



def main():
    f=fsm()

from typing import List
from typing_extensions import Self
from scene import scene,Task


class UI:
    '''
    将 UI 视作一个类，用来控制当前的语句，以及输入。它会作为一个单例传给fsm和scene，以后可以在这里扩充其他功能。
    当前的 UI 是命令行，因此相关的控制逻辑写在此处。
    注意：这种简易的单例模式可能会在多线程下出现问题。
    '''
    TaskList:List[Task]=None
    currentCommand = None
    currentScene:scene=None

    def __new__(cls: type[Self]) -> Self:
        '''覆盖掉init，不允许 new，只允许getInstance'''
        pass
    def __init__(self) -> None:
        print("初始化")
        
    def ShowHint(self,hint):
        print(hint)

    def GetInput(self, Input, ) : 
        '''获取输入。理论上应该再定义一个 scene 给定的解析策略类，但我觉得你会打我。所以我不搞了'''
        
        return self.parse(input())
    def _parse(self):
        return 

    @classmethod #类方法，不需要实例化就能调用 「小百科」 cls 代表类本身，而 self 是实例本身；_instance是自带的属性。
    def getInstance(cls, *args, **kwargs):
        '''
        定义一个类方法，用来返回单例
        '''
        if not hasattr(UI, "_instance"): #如果 UI 类没有实例
            UI._instance = UI(*args, **kwargs)
        return UI._instance

#example:
ui = UI.getInstance()
ui.ShowHint("")


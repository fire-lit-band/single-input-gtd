from abc import abstractmethod
from enum import Enum
from sre_parse import State
from typing import Generic, TypeVar,List,Union
from UI import UI
T=TypeVar('T')
'''scene 域
'''


#上下文类。这里用了泛型的context类，比如context[scene_ddl]，理论上，每一个场景，都要配一个对应的上下文类。因为每一个场景需要调用不同的上下文

class context(Generic[T]):
    #传上下文的时候，把 UI 整体也传入。方便函数调用看板等
    ui:UI=None
    currentCommand=None
    TaskList:'List[Task]'=None
    def __init__(self,UI:UI) -> None:
        self.ui=UI
        currentCommand =UI.c
    pass


class result(object):
    scene:scene=None
    State=None
    def __init__(self,success:bool):
        self.scene=scene
        self.success=success
    
    #scene 的抽象类
class scene(object):
    #场景中的上下文，比如一个 task，或者 stream，上下文的定义应由子类而定。
    _context:context[T]=None
    _supportedCommand:List[str]=
    #初始化的时候传入上下文
    def __init__(self,context) -> None:
        self._context= context
    
    def tryExecute(self,input_:str)->result:
        '''与状态机的约定：它只调用你scene的 tryExecute 函数，并传入 当前的 Context，暴露给外调用的函数，你可以在这里对具体执行进行装饰，
        比如进入真正逻辑之前先验证当前的 UI 是否打开，或许你可以用 decorator'''
        r:result=None
        try:
            assert input == str
            assert self._context.ui.isShow()==True #
            r = self._execute(self,input)
        except:
            raise Exception()
        return r
    @abstractmethod
    def _execute(self,input_:str)->result:
        #此处这里写你要的逻辑, 由子类重载。
        return result()

    def Serialize(self,data):
        #此处写你的csv输入逻辑
        return
    def undo(self):
        return
class inputScene(scene):
    def uiCommand(self) -> str:
        return super().uiCommand()
    def execute(self, input_: str):
        return super().execute(input_)
    pass    



    

#task类
class Task(object):
    name:str=""
    timeLimit:str=""
    supportcommand:'SupportCommand'=""
    
class Todo(Task):
    activity="reading"
    def DoTask(self):
        print(self.name+" "+self.timeLimit+self.activity)

class ddl(Task):
    activity="exam"
    def Cramming(self):
        print(self.name+" "+self.timeLimit+self.activity)

class SupportCommand(Enum):
    BREAK=0
    WAIT=1
    REST=2
    EMERGENCY=3




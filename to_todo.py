import json

import pandas as pd
def to_todo(todo):
    data=pd.DataFrame(todo)
    data.to_csv("todo.csv")
if __name__=="__main__":
    with open("todo.json",'r') as file:
         todo=json.load(file)
    to_todo(todo)
    print(todo)
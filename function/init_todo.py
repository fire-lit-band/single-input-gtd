from pathlib import Path

import pandas as pd

file_name = Path('./data/todo.csv')
if not file_name.exists():
    df=pd.read_csv('./data/todo_tempalate.csv')
    df.to_csv(file_name,index=False)

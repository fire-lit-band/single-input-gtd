import json
import numpy as np
import pandas as pd


def read_all_content(file="todo.csv"):
    return pd.read_csv(file)


def today_inbox_todo(file="todo.csv"):
    todo = pd.read_csv(file)
    return todo[todo.father.isnull()].name


def display_all_task(file="todo.csv"):
    todo = pd.read_csv(file)
    return todo["name"]


if __name__ == "__main__":
    print(today_todo())

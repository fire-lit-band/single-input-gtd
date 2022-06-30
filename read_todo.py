import json

import pandas as pd


def read_todo(file="todo.csv"):
    return pd.read_csv(file)


def today_todo(file="todo.csv"):
    todo = pd.read_csv(file)
    return todo["name"]


def display_all_task(file="todo.csv"):
    todo = pd.read_csv(file)
    return todo["name"]


if __name__ == "__main__":
    print(display_todo())

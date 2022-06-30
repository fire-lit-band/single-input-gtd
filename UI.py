import module
import read_todo


def main():
    result = "done"
    while result != "end":
        today_todo = read_todo.display_all_task()
        if result == "done":
            print(today_todo)
        else:
            print("开始计时！！")
        newinput = input("请输入指令")
        result = module.main(newinput)


if __name__ == "__main__":
    main()

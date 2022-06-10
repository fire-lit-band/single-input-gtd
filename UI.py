import module
import read_todo
def main():
    result=True
    while result:
        today_todo = read_todo.display_all_task()
        print(today_todo)
        newinput = input("请输入内容")
        result = module.main(newinput)

    


if __name__ == "__main__":
    main()
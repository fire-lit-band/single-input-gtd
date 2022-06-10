import module
import read_todo
def main():
    result=True
    while result:
        today_todo=read_todo.display_todo()
        print(today_todo)
        newinput=input("请输入内容")
        result=yield module.main(newinput)


if __name__=="__main__":
    main()
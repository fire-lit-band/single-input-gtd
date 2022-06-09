import module
import read_todo
def main():
    result=True
    while result:
        print(read_todo.display_todo())
        newinput=input("请输入内容")
        result=yield module(newinput)


if __name__=="__main__":
    main()
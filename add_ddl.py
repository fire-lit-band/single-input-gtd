from datetime import date
import calendar

def isLeapYear(year):
    if year % 4 == 0 and year % 100 != 0:
        return True
    if year % 400 == 0:
        return True
    return False


def getMaxDay(month, year = -1):
    MaxDays = [-1, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    if month < 1 or month > 12:
        print('error month')
        return -1
    maxDay = MaxDays[month]
    # 判断2月天数
    if year != -1 and month == 2:
        if isLeapYear(year):
            maxDay += 1
    return maxDay

def myfind(anlist,target):
    for i in anlist:
        if i==target:
            return i
    return 0


def main():
    year=0
    month=0
    date1=0
    ddl_list=''
    while True:
        if not ddl_list:
            ddl_list = input("请输入ddl名称：")
        if not ddl_list:
            break
        if not year:
            year=input("请输入年份：")
        if not year:
            year=date.today().year
        elif (not year.isdigit()) or int(year)<date.today().year or len(year)>4:
            print("输入错误，请重新输入")
            year=''
            continue
        else:
            pass

        year = str(int(year))
        if not month:
            month = input("请输入月份：")
        if not month:
            month = date.today().month
        elif month.isdigit():
            if 1<=int(month) <= 12:
                month=int(month)
            else:
                print("输入错误，请重新输入")
                continue
        elif myfind(list(calendar.month_abbr),month):
            month=myfind(list(calendar.month_abbr),month)
        elif myfind(list(calendar.month_name),month):
            month = myfind(list(calendar.month_name),month)
        else:
            print("输入错误，请重新输入")
            month=0
            continue
        month=str(month)
        if not date1:
            date1 = input("请输入日期：")
        if (not date1.isdigit()) or (not 1<=int(date1) <= getMaxDay(int(month), int(year))):
            print("输入错误，请重新输入")
            date1=0
            continue
        ddl_write='{0},{1},{2:0>2},{3:0>2}\n'.format(ddl_list,str(year),str(month),str(date1))
        with open('ddl.csv','a',encoding='utf-8') as f:
            f.write(ddl_write)
        print(f"输入成功 {ddl_write}")
        year = 0
        month = 0
        date1 = 0
        ddl_list = ''


if __name__ == "__main__":
    main()
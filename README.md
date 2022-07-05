# single-input-gtd 1.0

这里对当前项目的内容进行使用的说明

本项目主要运行两个文件，一个是UI.py,一个是user_input.py。运行后者可以为我们加入项目(或者todolist)，设置截止日期等，而运行前者可以帮助我们对时间进行统计

接下来我将对两个文件的使用进行说明

# UI.py

1.显示任务内容后，你可以输入项目前面的序号，开始执行该项目

2.在执行中，你可以输入

"ok"：表示已经完成这个项目，可以进行下一个任务

"q"：完成这个项目后退出程序

"p":暂停该项目

"!":因为紧急原因暂停该项目，并进行下一个项目

"~"：因为休息暂停该项目

" "：刷新任务清单

# use_input.py

根据显示页面，输入序号前面的内容

1、输入ddl

选择项目前面的序号，并按照提示输入他的截止时间

2、加入新项目

你可以输入项目前面的序号，进入项目所含有的子菜单

或者是输入add命令，你可以在当前菜单下建立一个平级的任务

# 未来的规划

1.加入gui
2.将append移除
3，加入value权重
4，加入重复次数的判定
5，加入倒计时
6.引入排序的算法
7.自动推荐明天的形成
8.显示所有子项目，并且表现出它们的层级关系


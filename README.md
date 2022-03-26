# single-input-gtd
目前来看windows版本是可用的，然后linux也是可以的，mac版本估计应该也可以
# 用前提醒
main.py是主程序  
plan.md的使用需要结合obsidain的看板功能，且to do那一行不能修改标题（以后应该会出plan.md的使用方法）  
ddl.csv是用于ddl的记录的（以后应该会另外出一个程序用于记录ddl的时间和内容，目前只支持自己手动输入，而且记住要用记事本打开，excel打开容易出问题）
另外每一天会生成一个当天日期的文件）
# 目前有的功能是
main.py  
进入界面显示你今天的todo项目和即将到来的ddl  
输入due进行ddl事项的任务（输入due后输入ddl的序号进行序号对应项目的内容） 
输入todo项目的序号可以进行序号对应项目的内容 
输入ok表示完成该项目 
输入wait表示还未完成该项目 
！（中英文都可以）表示有紧急事情要补充 
输入q表示结束本程序 
输入rest表示进行休息（可以补充休息的内容，如游戏，吃饭等） 
# 未来打算增加的功能
1. 进行项目时的comment（附带在项目上） 
2. 灵感的记录（memo式），把零碎的点子和未来要做但不紧急的事情记录下来 
3. code reconstruct 目前的代码的效率和可读性都太差，很多地方都可以code reuse，在后续版本中将进行相关的升级 
4. 增加一个addddl.py专门用于增加你未来的ddl 
5. 不使用obsidian照样能阅览的看板模式 
6. 增加每日习惯的记录和打卡 
7. 根据你现有的数据进行分析，可视化，并且能够提出意见 
8. sm plan的导入
9. 所有内容的交互界面的优化

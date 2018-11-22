#RTV through and back speed comparsion
#首先扫描文件(只扫描rtv文件)并检测所有的碰撞点，分析相应的手柄运动坐标值，
#判断当时是以什么方式运动的（through or back）,并计算距离上一次的点击所用时间，输入文件。
#格式：Participant_ID,Dimension,Block,Through_or_Back,Angle,Width,Distance,X,Y,Z,Time

#11.22当前问题：碰撞中的时间并不能完全和手柄运动轨迹中的时间吻合，需要一点模糊的解决方式。
#找到在碰撞文件中的时间，在手柄轨迹中的时间中寻找差值最小的一个，根据它当前坐标和前一帧的坐标运动方向来判断是朝着什么方向运动的。

#每次同时打开控制器的轨迹文件和碰撞点文件，只进行RTV文件部分的计算。
import os
import math
import inspect
import re

allFileNum=0
Controller_time=[]

def printPath(PID,Dimension,experiment_num,experiment_type,level,path,outputpath):
    global allFileNum
    #打印目录下所有子文件夹和文件
    #所有的文件
    dirList=[]
    #所有文件
    fileList=[]
    files=os.listdir(path)
    dirList.append(str(level))
    for f in files:
        if(os.path.isdir(path+'/'+f)):
            #过滤隐藏文件夹
            if(f[0]=='.'):
                pass
            else:
                #添加非隐藏的文件夹
                dirList.append(f)
        if((os.path.isfile(path+'/'+f))and(experiment_num in f)and('controller' in f)):
            #只添加当前实验的点击或穿过的数据文件
            fileList.append(f)
            #在传入文件时，同时传入文件夹信息，生成error的文件。
            read_file(PID,Dimension,experiment_num,path+'/'+f,path)
            #添加文件
                
    i_dl=0
    for dl in dirList:
        if(i_dl==0):
            i_dl=i_dl+1
        else:
           # print ('-' * (int(dirList[0])), dl)
            printPath(PID,Dimension,experiment_num,experiment_type,(int(dirList[0]) + 1), path + '/' + dl)
    for fl in fileList:
        print ('-' * (int(dirList[0])), path+'/'+fl)
        #print(path+'/'+fl)
        allFileNum = allFileNum + 1

#读取控制器文件部分
def readfile(filepath):
    f=open(filepath)
    line=f.readline()
    while line:
        linelist=line.split(',')
        Controller_time.append(linelist[3].strip('\n'))
        line=f.readline()
    f.close()


def read_file(PID,Dimension,experiment_num,filepath,outputpath):
    #如果當前檢測的是豎直方向，則參數為90
    #如果當前是水平方向，則參數為0
    f=open(filepath)
    if('practice' in filepath):
        BL='0'
    if('1-block' in filepath):
        BL='1'
    if('2-block' in filepath):
        BL='2'
    if('direct-touch' in filepath):
        OT='1'
    if('RTV' in filepath):
        OT='2'
    #在文件末尾追加内容
    #---------------------
    #需要将此处的文件追加变成创建文件
    f2=open(errorfilepath+'/Experiment1_error_info.txt','a')
    #---------------------
    #控制器中只有坐标和时间
    line=f.readline()
    while line:
        #使用动态创建变量的方式来创建变量，否则列举太过复杂
        if('miss' in line):
            #使用split函数将当前角度等信息分离出来
            scentencelist=line.split('!')
            #0中为just missed
            xyz_and_time=scentencelist[1]
            xyz_and_time=xyz_and_time.strip('(')

            xyz_and_time_list=xyz_and_time.split(',')
            
            x=xyz_and_time_list[0].strip(' ')
            y=xyz_and_time_list[1].strip(' ')
            z=xyz_and_time_list[2].strip(')')
            z=z.strip(' ')
            time=xyz_and_time_list[3]
            #格式：Participant_ID,Dimension,Operation_type,Block,X,Y,Z,Time
            f2.write(PID+','+Dimension+','+OT+','+BL+','+x+','+y+','+z+','+time)
        line=f.readline()
    f.close()
    f2.close()

#找到碰撞點對應時間的最近時間，並返回手柄對應時間的index值。
def find_closest_time(Collider_time,Controller_time,Time_range):
    if(str(Collider_time) in Controller_time):
        return Controller_time.index(Collider_time)
    elif(str((float(Collider_time)-Time_range)) in Controller_time):
        return Controller_time.index(Collider_time-Time_range)
    elif(str((float(Collider_time)-2*Time_range)) in Controller_time):
        return Controller_time.index(Collider_time-2*Time_range)

#位置1是位置2的前一個位置
def Judge_Direction(Orientation,Controller_location1,Controller_location2):
    direction=0
    #定义0为离开用户的方向，1为朝向用户的方向
    #对于一维的竖直情况，x值变化说明方向的变化：朝向用户运动时x变大，远离用户时x变小。
    #对于45度的情况时，可以暂时只考虑使用少数数据，既然角度本身没有太大影响。
    #一维的水平情况，y值变化说明方向变化：朝向用户时y变大，远离用户时y变小。
    #二維中的xy變化方式一樣。
    if(Orientation==90):
        if(Controller_location1.x<Controller_location2.x):
            direction=1
    if(Orientation==0):
        if(Controller_location1.y<Controller_location2.y):
            direction=1
    return direction


if __name__ == "__main__":
    namelist=['wangchen','kavous','hanzengyi','yuga','liujingxin','fitra','wuanran','jiangxinhui','liyang','zhanghongtao','lizhen','linzhengwei']
    for i in range(12):
        printPath(str(i),'1','Experiment1','0',1,'/Users/jasonhanyi/Downloads/ocb-data/'+namelist[i],'/Users/jasonhanyi/Downloads/11.22-TABdata.txt')
        printPath(str(i),'2','Experiment2','0',1,'/Users/jasonhanyi/Downloads/ocb-data/'+namelist[i],'/Users/jasonhanyi/Downloads/11.22-TABdata.txt')
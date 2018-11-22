#测试找到最近的
import os
import math
import inspect
import re


Controller_time=['25.67','25.69','25.70']


#将所有行都读入，时间和坐标分别存放
def readfile(filepath):
    f=open(filepath)
    line=f.readline()
    while line:
        linelist=line.split(',')
        Controller_time.append(linelist[3].strip('\n'))
        line=f.readline()
    f.close()

def find_closest_time(Collider_time,Controller_time,Time_range):
    if(str(Collider_time) in Controller_time):
        return Controller_time.index(Collider_time)
    elif(str((float(Collider_time)-Time_range)) in Controller_time):
        return Controller_time.index(Collider_time-Time_range)
    elif(str((float(Collider_time)-2*Time_range)) in Controller_time):
        return Controller_time.index(Collider_time-2*Time_range)

if __name__ == "__main__":
    #readfile('/Users/jasonhanyi/Downloads/ocb-data/hanzengyi/1-block/RTV/Experiment1-right-controller.txt')
    #print(Controller_time)
    print(find_closest_time('25.70',Controller_time,0.01))

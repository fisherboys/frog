# _*_ coding:utf-8 _*_
import os
import time
import re

# === 思路 ===
# 将系统时间设置到很久之前，每隔三个小时收割一次三叶草，直至当前真正时间
# 
# === 前提 ===
# 1.Android手机，且已经root
# 2.需要电脑，电脑端已经安装好adb驱动及python
#
# === 操作步骤 ===
# 1.将系统时间设置为很久以前
# 2.安装青蛙旅行app及手动完成教学
# 3.将手机与电脑相连，且在cmd命令行输入adb devices可现实设备
# 4.启动青蛙旅行app，在主界面
# 5.运行此脚本：python frog.py

def main():
    # 读取旅行青蛙app的包名
    activity_name = get_activity_name()
    
    # 读取当前真正的时间
    real_time = int(time.time())

    # 当前手机的时间
    now_time = 0

    # 获取屏幕尺寸
    width = int(get_screensize()[0])
    height = int(get_screensize()[1])
    if width > height:
        width, height = height, width

    while now_time < real_time:
        # 读取手机当前的时间
        now_time = int(os.popen('adb shell date +%s').readlines()[0])
    
        # 增加三个小时
        now_time+=3*3600
    
        # 设置系统时间
        set_time(now_time)

        # 启动青蛙旅行app
        os.system('adb shell input keyevent 3')
        time.sleep(0.2)
        os.system('adb shell am start -n %s'%activity_name)

        # 获取三叶草
        get_clover(width, height)

def get_activity_name():
    # 获取显示在界面上的Activity完整名
    f = os.popen('adb shell dumpsys activity top | find "ACTIVITY"')
    str = f.readlines()[0]
    return re.findall(r'ACTIVITY (.+?) ', str)[0]

def get_screensize():
    size = os.popen('adb shell wm size').readlines()[0]
    return re.findall(r'(\d{3,4})',size)

def set_time(t):
    # 设置系统时间
    date = time.strftime("%Y%m%d.%H%M%S", time.localtime(t))
    os.system('adb shell "su 0 toolbox date -s %s"'%date)


def get_clover(w, h):
    # 点击屏幕，防止出现提示框
    os.system('adb shell input tap %d %d'%(w/2,h/5))
    os.system('adb shell input tap %d %d'%(w/2,h/5))

    # 滑动屏幕到最左侧 
    os.system('adb shell input swipe 10 %d %d %d 100'%(h/4, 2*w, h/4))
    
    # 收割三叶草,划三行，每划一行点击空白处，防止弹出提示框
    os.system('adb shell input swipe 5 %d %d %d 200'%(11*h/20, w, 11*h/20))
    os.system('adb shell input tap %d %d'%(w/2,h/5))
    os.system('adb shell input swipe 5 %d %d %d 200'%(12*h/20, w, 12*h/20))
    os.system('adb shell input tap %d %d'%(w/2,h/5))
    os.system('adb shell input swipe 5 %d %d %d 200'%(13*h/20, w, 13*h/20))



if __name__ == '__main__':
    main()
